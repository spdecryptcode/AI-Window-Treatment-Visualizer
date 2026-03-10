"""
Core AI pipeline for window treatment visualization.

Implements:
- Window detection (YOLOv8)
- Window segmentation (FastSAM)
- Depth estimation (MiDaS)
- Treatment geometry calculation
"""

import torch
import numpy as np
from PIL import Image
import cv2
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import time


class WindowDetector:
    """YOLOv8-based window detection."""
    
    def __init__(self, model_path: str = "models/yolov8/yolov8n.pt"):
        """Initialize YOLO model."""
        from ultralytics import YOLO
        
        self.model = YOLO(model_path)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        
        # Warm up model
        dummy = torch.zeros((1, 3, 640, 640)).to(self.device)
        self.model(dummy)
        
        print(f"✓ WindowDetector loaded on {self.device}")
    
    def detect(self, image: np.ndarray, confidence: float = 0.5) -> List[Dict]:
        """
        Detect windows in image.
        
        Args:
            image: RGB image as numpy array
            confidence: Confidence threshold (0-1)
            
        Returns:
            List of detections with bbox, confidence, class
        """
        start_time = time.time()
        
        # Run inference
        results = self.model(image, conf=confidence, verbose=False)
        
        detections = []
        all_detections = []  # For debugging
        
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Get class name
                cls_id = int(box.cls[0])
                cls_name = result.names[cls_id]
                
                # Get bounding box
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0])
                
                detection = {
                    'bbox': [int(x1), int(y1), int(x2 - x1), int(y2 - y1)],  # x, y, w, h
                    'confidence': conf,
                    'class': cls_name,
                    'center': [int((x1 + x2) / 2), int((y1 + y2) / 2)]
                }
                
                all_detections.append(detection)
                
                # Filter for window-related classes (COCO doesn't have 'window', so this will be empty)
                # NOTE: Pre-trained YOLO doesn't detect interior windows - needs fine-tuning
                if cls_name.lower() in ['window', 'door', 'tv']:  # tv/monitor often near windows
                    detections.append(detection)
        
        elapsed = time.time() - start_time
        
        # Debug: show what was actually detected
        if not detections and all_detections:
            print(f"  Detection: 0 windows found, but detected {len(all_detections)} objects:")
            for det in all_detections[:5]:  # Show first 5
                print(f"    - {det['class']} (conf: {det['confidence']:.2f})")
        else:
            print(f"  Detection: {len(detections)} windows found in {elapsed:.2f}s")
        
        return detections


class WindowSegmenter:
    """FastSAM-based window segmentation."""
    
    def __init__(self, model_path: str = "models/fastsam/FastSAM-s.pt"):
        """Initialize FastSAM model."""
        from ultralytics import YOLO
        
        self.model = YOLO(model_path)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        print(f"✓ WindowSegmenter loaded on {self.device}")
    
    def segment(self, image: np.ndarray, bbox: List[int]) -> Dict:
        """
        Segment window using bounding box prompt.
        
        Args:
            image: RGB image as numpy array
            bbox: [x, y, width, height]
            
        Returns:
            Dictionary with masks and metadata
        """
        start_time = time.time()
        
        # Convert bbox to xyxy format for SAM
        x, y, w, h = bbox
        prompt_box = [x, y, x + w, y + h]
        
        # Run FastSAM
        results = self.model(
            image,
            device=self.device,
            retina_masks=True,
            imgsz=1024,
            conf=0.4,
            iou=0.9,
        )
        
        # Get masks
        if len(results) == 0 or results[0].masks is None:
            # Fallback: create mask from bbox
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            mask[y:y+h, x:x+w] = 255
            
            return {
                'glass_mask': mask,
                'frame_mask': np.zeros_like(mask),
                'combined_mask': mask,
                'quality_score': 0.3,
                'method': 'fallback_bbox'
            }
        
        # Find mask that best overlaps with bbox
        masks = results[0].masks.data.cpu().numpy()
        
        # Calculate IoU with prompt box
        best_mask_idx = 0
        best_iou = 0
        
        for idx, mask in enumerate(masks):
            mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
            mask_in_box = mask_resized[y:y+h, x:x+w].sum()
            box_area = w * h
            iou = mask_in_box / box_area
            
            if iou > best_iou:
                best_iou = iou
                best_mask_idx = idx
        
        # Get best mask
        mask = masks[best_mask_idx]
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]))
        mask = (mask > 0.5).astype(np.uint8) * 255
        
        # Refine mask
        mask = self._refine_mask(mask)
        
        elapsed = time.time() - start_time
        print(f"  Segmentation: quality {best_iou:.2f} in {elapsed:.2f}s")
        
        return {
            'glass_mask': mask,
            'frame_mask': self._extract_frame(mask),
            'combined_mask': mask,
            'quality_score': float(best_iou),
            'method': 'fastsam'
        }
    
    def _refine_mask(self, mask: np.ndarray) -> np.ndarray:
        """Refine mask with morphological operations."""
        # Remove noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Smooth edges
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        mask = (mask > 127).astype(np.uint8) * 255
        
        return mask
    
    def _extract_frame(self, mask: np.ndarray) -> np.ndarray:
        """Extract window frame from mask (border region)."""
        # Erode to get inner glass area
        kernel = np.ones((10, 10), np.uint8)
        inner = cv2.erode(mask, kernel, iterations=1)
        
        # Frame = full mask - inner glass
        frame = cv2.subtract(mask, inner)
        
        return frame


class DepthEstimator:
    """MiDaS-based depth estimation."""
    
    def __init__(self, model_path: str = "models/midas"):
        """Initialize MiDaS model."""
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        try:
            # Try to load MiDaS from torch hub
            self.model = torch.hub.load("intel-isl/MiDaS", "DPT_SwinV2_T_256")
            self.transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform
            
        except Exception as e:
            print(f"  Warning: Could not load MiDaS: {e}")
            print(f"  Using fallback depth estimation")
            self.model = None
            self.transform = None
        
        if self.model is not None:
            self.model.to(self.device)
            self.model.eval()
            print(f"✓ DepthEstimator loaded on {self.device}")
    
    def estimate(self, image: np.ndarray, bbox: Optional[List[int]] = None) -> Dict:
        """
        Estimate depth map.
        
        Args:
            image: RGB image as numpy array
            bbox: Optional [x, y, w, h] to process only region
            
        Returns:
            Dictionary with depth map and metadata
        """
        start_time = time.time()
        
        if self.model is None:
            # Fallback: simple center-focused depth
            return self._fallback_depth(image, bbox)
        
        # Process region of interest if bbox provided
        if bbox is not None:
            x, y, w, h = bbox
            # Expand region by 20%
            pad = int(max(w, h) * 0.2)
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(image.shape[1], x + w + pad)
            y2 = min(image.shape[0], y + h + pad)
            
            roi = image[y1:y2, x1:x2]
        else:
            roi = image
        
        # Prepare input
        input_batch = self.transform(roi).to(self.device)
        
        # Predict
        with torch.no_grad():
            prediction = self.model(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=roi.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        
        depth = prediction.cpu().numpy()
        
        # Normalize  to 0-1
        depth = (depth - depth.min()) / (depth.max() - depth.min())
        
        # If we processed ROI, place back into full image
        if bbox is not None:
            full_depth = np.zeros(image.shape[:2], dtype=np.float32)
            full_depth[y1:y2, x1:x2] = depth
            depth = full_depth
        Elapsed = time.time() - start_time
        print(f"  Depth estimation: {elapsed:.2f}s")
        
        return {
            'depth_map': depth,
            'min_depth': float(depth.min()),
            'max_depth': float(depth.max()),
            'method': 'midas'
        }
    
    def _fallback_depth(self, image: np.ndarray, bbox: Optional[List[int]]) -> Dict:
        """Fallback depth estimation (simple gradient)."""
        h, w = image.shape[:2]
        
        # Create simple depth gradient (further = darker for windows)
        y_coords = np.linspace(0, 1, h)
        x_coords = np.linspace(0, 1, w)
        
        # Radial gradient from center
        yy, xx = np.meshgrid(y_coords, x_coords, indexing='ij')
        center_y, center_x = 0.5, 0.5
        
        depth = np.sqrt((xx - center_x)**2 + (yy - center_y)**2)
        depth = 1 - (depth / depth.max())  # Invert
        
        return {
            'depth_map': depth.astype(np.float32),
            'min_depth': 0.0,
            'max_depth': 1.0,
            'method': 'fallback'
        }


def calculate_treatment_geometry(
    mask: np.ndarray,
    depth_map: np.ndarray,
    treatment_type: str = 'curtains'
) -> Dict:
    """
    Calculate treatment placement geometry.
    
    Args:
        mask: Window mask (binary)
        depth_map: Depth map (0-1)
        treatment_type: Type of treatment
        
    Returns:
        Dictionary with mounting points, dimensions, etc.
    """
    # Find window boundaries
    coords = np.column_stack(np.where(mask > 127))
    
    if len(coords) == 0:
        return {
            'valid': False,
            'message': 'Empty mask'
        }
    
    # Bounding box of window
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    
    # Calculate mounting rail position (above window)
    mount_offset = int((y_max - y_min) * 0.05)  # 5% of window height
    mount_y = max(0, y_min - mount_offset)
    
    # Treatment dimensions
    if treatment_type == 'curtains':
        # Curtains extend bottom to floor or sill
        treatment_height = y_max - mount_y + int((y_max - y_min) * 0.1)
        treatment_width = int((x_max - x_min) * 1.2)  # 20% wider for fullness
    elif treatment_type == 'blinds':
        # Blinds match window exactly
        treatment_height = y_max - mount_y
        treatment_width = x_max - x_min
    else:  # shades
        treatment_height = y_max - mount_y
        treatment_width = x_max - x_min
    
    # Sample depth at window center for recess depth
    center_y = (y_min + y_max) // 2
    center_x = (x_min + x_max) // 2
    window_depth = depth_map[center_y, center_x]
    
    return {
        'valid': True,
        'mount_point': [int(x_min), int(mount_y)],
        'window_bbox': [int(x_min), int(y_min), int(x_max - x_min), int(y_max - y_min)],
        'treatment_bbox': [
            int(x_min - (treatment_width - (x_max - x_min)) / 2),
            int(mount_y),
            int(treatment_width),
            int(treatment_height)
        ],
        'window_depth': float(window_depth),
        'treatment_type': treatment_type
    }


def unload_models(*models):
    """Unload models from GPU to free VRAM."""
    import gc
    
    for model in models:
        if hasattr(model, 'model'):
            del model.model
        del model
    
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    gc.collect()
    print("  GPU memory freed")
