"""
Gradio prototype interface for Window Treatment Visualizer.

Run with: python app.py
Access at: http://localhost:7860
"""

import gradio as gr
import numpy as np
from PIL import Image
import cv2
from pathlib import Path
import time
from typing import Optional, Tuple

from pipeline import WindowDetector, WindowSegmenter, DepthEstimator, calculate_treatment_geometry, unload_models
from classical_renderer import ClassicalRenderer, load_swatch


# Global state
detector = None
segmenter = None
depth_estimator = None
renderer = None

# Session state
current_image = None
current_detections = None
current_segmentation = None
current_depth = None
current_geometry = None


def initialize_models():
    """Initialize AI models on startup."""
    global detector, segmenter, depth_estimator, renderer
    
    print("\n🚀 Initializing models...")
    
    try:
        detector = WindowDetector()
        segmenter = WindowSegmenter()
        depth_estimator = DepthEstimator()
        renderer = ClassicalRenderer()
        
        print("✅ All models initialized successfully!\n")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize models: {e}")
        print("   Please run: python download_models.py")
        return False


def process_upload(image: np.ndarray) -> Tuple[np.ndarray, str]:
    """Process uploaded image."""
    global current_image
    
    if image is None:
        return None, "No image uploaded"
    
    # Resize if too large
    max_size = 1024
    h, w = image.shape[:2]
    
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        image = cv2.resize(image, (new_w, new_h))
    
    current_image = image
    
    return image, f"✓ Image loaded: {image.shape[1]}x{image.shape[0]}"


def detect_windows(
    image: np.ndarray,
    confidence: float = 0.5
) -> Tuple[np.ndarray, str]:
    """Detect windows in image."""
    global current_detections
    
    if image is None:
        return None, "Please upload an image first"
    
    if detector is None:
        return None, "Models not initialized"
    
    try:
        # Run detection
        detections = detector.detect(image, confidence=confidence)
        current_detections = detections
        
        # Draw detections on image
        viz_image = image.copy()
        
        for det in detections:
            x, y, w, h = det['bbox']
            conf = det['confidence']
            
            # Color based on confidence
            if conf > 0.7:
                color = (0, 255, 0)  # Green
            elif conf > 0.5:
                color = (255, 255, 0)  # Yellow
            else:
                color = (255, 0, 0)  # Red
            
            # Draw box
            cv2.rectangle(viz_image, (x, y), (x+w, y+h), color, 3)
            
            # Draw label
            label = f"{det['class']}: {conf:.2f}"
            cv2.putText(
                viz_image, label, (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
            )
        
        message = f"✓ Found {len(detections)} window(s)"
        return viz_image, message
        
    except Exception as e:
        return None, f"❌ Detection failed: {str(e)}"


def segment_window(
    image: np.ndarray,
    detection_idx: int = 0,
    use_manual: bool = False,
    manual_x: int = 200,
    manual_y: int = 100,
    manual_w: int = 400,
    manual_h: int = 500
) -> Tuple[Optional[np.ndarray], str]:
    """Segment selected window."""
    global current_segmentation, current_depth, current_geometry
    
    if image is None:
        return None, "Please upload an image first"
    
    # Determine bbox
    if use_manual or current_detections is None or len(current_detections) == 0:
        # Use manual selection
        bbox = [int(manual_x), int(manual_y), int(manual_w), int(manual_h)]
        message_prefix = "Manual selection:"
    else:
        # Use detected window
        if detection_idx >= len(current_detections):
            return None, f"Invalid selection (only {len(current_detections)} windows detected)"
        
        det = current_detections[detection_idx]
        bbox = det['bbox']
        message_prefix = "Auto-detected:"
        det = current_detections[detection_idx]
        bbox = det['bbox']
        message_prefix = "Auto-detected:"
    
    try:
        # Segment window
        seg_result = segmenter.segment(image, bbox)
        current_segmentation = seg_result
        
        # Estimate depth
        depth_result = depth_estimator.estimate(image, bbox)
        current_depth = depth_result
        
        # Calculate geometry
        geometry = calculate_treatment_geometry(
            seg_result['combined_mask'],
            depth_result['depth_map'],
            treatment_type='curtains'
        )
        current_geometry = geometry
        
        # Visualize segmentation
        viz_image = image.copy()
        
        # Overlay mask in blue
        mask = seg_result['combined_mask']
        blue_overlay = np.zeros_like(image)
        blue_overlay[:, :, 2] = mask  # Blue channel
        
        # Alpha blend
        alpha = 0.4
        viz_image = cv2.addWeighted(viz_image, 1-alpha, blue_overlay, alpha, 0)
        
        # Draw bbox
        x, y, w, h = bbox
        cv2.rectangle(viz_image, (x, y), (x+w, y+h), (255, 255, 0), 2)
        
        # Draw treatment bbox
        if geometry['valid']:
            tx, ty, tw, th = geometry['treatment_bbox']
            cv2.rectangle(viz_image, (tx, ty), (tx+tw, ty+th), (255, 0, 255), 2)
        
        message = f"{message_prefix} ✓ Segmentation complete (quality: {seg_result['quality_score']:.2f})\n"
        message += f"Geometry valid: {geometry['valid']}\n"
        message += "✅ Ready to render - go to Tab 3!"
        return viz_image, message
        
    except Exception as e:
        return None, f"❌ Segmentation failed: {str(e)}"


def render_treatment(
    treatment_type: str,
    swatch_name: str,
    fullness: str = "standard",
    length: str = "floor"
) -> Tuple[Optional[np.ndarray], str]:
    """Render treatment on window."""
    global current_image, current_segmentation, current_depth, current_geometry
    
    # Debug info
    debug_info = []
    debug_info.append(f"Image: {'✓' if current_image is not None else '✗'}")
    debug_info.append(f"Segmentation: {'✓' if current_segmentation is not None else '✗'}")
    debug_info.append(f"Depth: {'✓' if current_depth is not None else '✗'}")
    debug_info.append(f"Geometry: {'✓' if current_geometry is not None else '✗'}")
    
    if current_image is None:
        return None, "❌ Please upload image first (Tab 1)"
    
    if current_segmentation is None:
        return None, "❌ Please segment window first (Tab 2)\n" + "\n".join(debug_info)
    
    if current_geometry is None or not current_geometry.get('valid', False):
        return None, f"❌ Invalid window geometry\n" + "\n".join(debug_info)
    
    try:
        # Load swatch
        swatch_path = Path("..") / "swatches" / treatment_type / f"{swatch_name}.jpg"
        
        print(f"  Attempting to load swatch: {swatch_path}")
        print(f"  Swatch exists: {swatch_path.exists()}")
        
        if not swatch_path.exists():
            # Try to find any swatch in that category
            swatch_dir = Path("..") / "swatches" / treatment_type
            if swatch_dir.exists():
                swatches = list(swatch_dir.glob("*.jpg"))
                print(f"  Found {len(swatches)} swatches in {swatch_dir}")
                if swatches:
                    swatch_path = swatches[0]
                    print(f"  Using first swatch: {swatch_path}")
                else:
                    return None, f"No swatches found in {treatment_type}/"
            else:
                return None, f"Swatch directory not found: {treatment_type}/"
        
        swatch = load_swatch(str(swatch_path))
        print(f"  ✓ Loaded swatch: {swatch.shape}")
        
        # Prepare settings
        settings = {
            'fullness': fullness,
            'length': length,
            'opacity': 0.9 if treatment_type == 'shades' else 1.0,
            'shade_type': 'roller' if treatment_type == 'shades' else None
        }
        
        # Update geometry for treatment type
        geometry = calculate_treatment_geometry(
            current_segmentation['combined_mask'],
            current_depth['depth_map'],
            treatment_type=treatment_type
        )
        
        # Render
        result = renderer.render(
            current_image,
            current_segmentation['combined_mask'],
            swatch,
            geometry,
            current_depth['depth_map'],
            treatment_type=treatment_type,
            settings=settings
        )
        
        message = f"✓ Rendered {treatment_type} with {swatch_name}"
        return result, message
        
    except Exception as e:
        return None, f"❌ Rendering failed: {str(e)}"


def create_interface():
    """Create Gradio interface."""
    
    # Initialize models
    if not initialize_models():
        return None
    
    # Create swatch directories if they don't exist
    swatches_root = Path("..") / "swatches"  # Parent directory
    for treatment in ['curtains', 'blinds', 'shades']:
        (swatches_root / treatment).mkdir(parents=True, exist_ok=True)
    
    # Scan for available swatches
    swatches = {}
    for treatment in ['curtains', 'blinds', 'shades']:
        swatch_dir = swatches_root / treatment
        swatch_files = list(swatch_dir.glob("*.jpg")) + list(swatch_dir.glob("*.png"))
        swatches[treatment] = [f.stem for f in swatch_files] if swatch_files else ['no_swatches_found']
    
    print(f"\n📋 Available swatches:")
    for t, s in swatches.items():
        print(f"  {t}: {len(s)} swatches - {s[:3]}")
    
    with gr.Blocks(title="Window Treatment Visualizer - Prototype") as demo:
        gr.Markdown("""
        # 🪟 AI Window Treatment Visualizer - Prototype
        
        **Week 1 Validation Phase** - Test pre-trained models to determine production path.
        
        ### Workflow:
        1. **Upload** a room photo
        2. **Detect** windows automatically
        3. **Segment** the selected window
        4. **Render** treatment with chosen swatch
        5. **Compare** before/after
        """)
        
        # Tab 1: Upload & Detect
        with gr.Tab("1. Upload & Detect"):
            gr.Markdown("""
            **Note:** Pre-trained YOLO doesn't detect interior windows reliably. 
            If auto-detection fails, you can manually select the window area in the next tab.
            """)
            
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(label="Upload Room Photo", type="numpy")
                    confidence_slider = gr.Slider(
                        0.3, 0.9, value=0.3, step=0.1,
                        label="Detection Confidence Threshold"
                    )
                    detect_btn = gr.Button("🔍 Detect Windows (Auto)", variant="primary")
                
                with gr.Column():
                    detection_output = gr.Image(label="Detected Windows")
                    detection_status = gr.Textbox(label="Status", lines=3)
            
            input_image.change(
                process_upload,
                inputs=[input_image],
                outputs=[detection_output, detection_status]
            )
            
            detect_btn.click(
                detect_windows,
                inputs=[input_image, confidence_slider],
                outputs=[detection_output, detection_status]
            )
        
        # Tab 2: Segment Window
        with gr.Tab("2. Segment Window"):
            gr.Markdown("""
            **Manual Mode:** If detection failed, enter window coordinates manually below.
            Check the "Use Manual Selection" box and adjust coordinates.
            """)
            
            with gr.Row():
                with gr.Column():
                    window_selector = gr.Number(
                        value=0, precision=0,
                        label="Window Index (0 = first detected)"
                    )
                    
                    gr.Markdown("### Manual Window Selection")
                    manual_mode = gr.Checkbox(
                        label="☑️ Use Manual Selection (if auto-detection failed)",
                        value=False
                    )
                    manual_x = gr.Number(label="X (left edge)", value=200, precision=0)
                    manual_y = gr.Number(label="Y (top edge)", value=100, precision=0)
                    manual_w = gr.Number(label="Width", value=400, precision=0)
                    manual_h = gr.Number(label="Height", value=500, precision=0)
                    
                    segment_btn = gr.Button("✂️ Segment Window", variant="primary")
                
                with gr.Column():
                    segmentation_output = gr.Image(label="Window Segmentation")
                    segmentation_status = gr.Textbox(label="Status", lines=3)
            
            segment_btn.click(
                segment_window,
                inputs=[input_image, window_selector, manual_mode, manual_x, manual_y, manual_w, manual_h],
                outputs=[segmentation_output, segmentation_status]
            )
        
        # Tab 3: Render Treatment
        with gr.Tab("3. Render Treatment"):
            with gr.Row():
                with gr.Column():
                    treatment_type = gr.Radio(
                        choices=['curtains', 'blinds', 'shades'],
                        value='curtains',
                        label="Treatment Type"
                    )
                    
                    swatch_selector = gr.Dropdown(
                        choices=swatches['curtains'],
                        value=swatches['curtains'][0],
                        label="Fabric Swatch"
                    )
                    
                    fullness = gr.Radio(
                        choices=['minimal', 'standard', 'extra'],
                        value='standard',
                        label="Fullness (curtains only)"
                    )
                    
                    length = gr.Radio(
                        choices=['sill', 'below_sill', 'floor'],
                        value='floor',
                        label="Length"
                    )
                    
                    render_btn = gr.Button("🎨 Render Preview", variant="primary")
                
                with gr.Column():
                    render_output = gr.Image(label="Rendered Preview")
                    render_status = gr.Textbox(label="Status", lines=2)
            
            # Update swatch list when treatment type changes
            def update_swatches(treatment):
                return gr.Dropdown(choices=swatches.get(treatment, []))
            
            treatment_type.change(
                update_swatches,
                inputs=[treatment_type],
                outputs=[swatch_selector]
            )
            
            render_btn.click(
                render_treatment,
                inputs=[treatment_type, swatch_selector, fullness, length],
                outputs=[render_output, render_status]
            )
        
        # Tab 4: Compare (simple before/after)
        with gr.Tab("4. Before / After"):
            gr.Markdown("### Compare original vs rendered")
            
            with gr.Row():
                before_display = gr.Image(label="Before", value=None)
                after_display = gr.Image(label="After", value=None)
            
            compare_btn = gr.Button("📊 Update Comparison")
            
            def update_comparison():
                return current_image, render_output.value
            
            render_btn.click(
                lambda x: (current_image, x),
                inputs=[render_output],
                outputs=[before_display, after_display]
            )
        
        # Tab 5: Info
        with gr.Tab("ℹ️ Info"):
            gr.Markdown("""
            ### About This Prototype
            
            **Purpose:** Validate whether pre-trained AI models produce acceptable quality 
            before committing to full production architecture.
            
            **Models Used:**
            - **YOLOv8n**: Window detection
            - **FastSAM-s**: Window segmentation
            - **MiDaS Small**: Depth estimation
            - **Classical Rendering**: Computer graphics (no AI)
            
            **Next Steps:**
            - Test with 20-30 room images
            - Collect sales rep feedback
            - Decide: Classical rendering OR SDXL fine-tuning
            
            **Performance:**
            - Classical mode: ~6-8 seconds
            - Expected quality: 6-7/10 (realistic but some "CG" look)
            
            **Hardware:**
            - GPU: NVIDIA RTX 3060+ (12GB VRAM)
            - RAM: 16GB minimum
            - Storage: 50GB for models
            
            **Support:** See README.md and TEST_CASES.md
            """)
    
    return demo


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Window Treatment Visualizer - Prototype")
    print("=" * 60 + "\n")
    
    demo = create_interface()
    
    if demo is not None:
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False
        )
    else:
        print("\n❌ Failed to initialize. Please run: python download_models.py")
