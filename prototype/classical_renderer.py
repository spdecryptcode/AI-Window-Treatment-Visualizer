"""
Classical rendering engine for window treatments.

Uses computer graphics techniques (no AI) for deterministic, fast rendering.
"""

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from typing import Dict, Tuple, Optional
import time


class ClassicalRenderer:
    """Non-AI rendering using classical computer graphics."""
    
    def __init__(self):
        """Initialize renderer."""
        print("✓ ClassicalRenderer initialized")
    
    def render(
        self,
        image: np.ndarray,
        mask: np.ndarray,
        swatch: np.ndarray,
        geometry: Dict,
        depth_map: Optional[np.ndarray] = None,
        treatment_type: str = 'curtains',
        settings: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Render window treatment using classical graphics.
        
        Args:
            image: Original room image (RGB)
            mask: Window mask (binary, 0-255)
            swatch: Fabric texture (RGB)
            geometry: Treatment geometry from calculate_treatment_geometry()
            depth_map: Optional depth map
            treatment_type: 'curtains', 'blinds', or 'shades'
            settings: Optional rendering settings
            
        Returns:
            Rendered image with treatment
        """
        start_time = time.time()
        
        settings = settings or {}
        
        # Create treatment overlay
        if treatment_type == 'curtains':
            treatment = self._create_curtain(geometry, swatch, settings)
        elif treatment_type == 'blinds':
            treatment = self._create_blinds(geometry, swatch, settings)
        else:  # shades
            treatment = self._create_shade(geometry, swatch, settings)
        
        # Generate shadows
        shadow = self._create_shadows(mask, depth_map, geometry)
        
        # Color match to room lighting
        treatment = self._match_room_lighting(treatment, image, mask)
        
        # Composite onto original image
        result = self._composite(image, treatment, shadow, mask, geometry)
        
        elapsed = time.time() - start_time
        print(f"  Classical rendering: {elapsed:.2f}s")
        
        return result
    
    def _create_curtain(
        self,
        geometry: Dict,
        swatch: np.ndarray,
        settings: Dict
    ) -> np.ndarray:
        """Create curtain with vertical pleats."""
        bbox = geometry['treatment_bbox']
        x, y, w, h = bbox
        
        # Create canvas
        curtain = np.zeros((h, w, 4), dtype=np.uint8)  # RGBA
        
        # Tile swatch texture
        texture = self._tile_texture(swatch, (w, h))
        curtain[:, :, :3] = texture
        curtain[:, :, 3] = 255  # Fully opaque
        
        # Add vertical pleats (sine wave deformation)
        fullness = settings.get('fullness', 'standard')
        
        if fullness == 'extra':
            num_pleats = w // 15
        elif fullness == 'minimal':
            num_pleats = w // 30
        else:  # standard
            num_pleats = w // 20
        
        # Create pleat displacement map
        x_coords = np.arange(w)
        pleat_wave = np.sin(x_coords * 2 * np.pi / (w / num_pleats)) * 3
        
        # Apply subtle displacement
        for y_coord in range(h):
            shift = int(pleat_wave[y_coord % w] * (1 - y_coord / h))  # Reduce toward bottom
            if shift != 0:
                curtain[y_coord] = np.roll(curtain[y_coord], shift, axis=0)
        
        # Add shading for depth of pleats
        shading = self._create_pleat_shading(w, h, num_pleats)
        curtain[:, :, :3] = (curtain[:, :, :3] * shading[:, :, None]).astype(np.uint8)
        
        return curtain
    
    def _create_blinds(
        self,
        geometry: Dict,
        swatch: np.ndarray,
        settings: Dict
    ) -> np.ndarray:
        """Create horizontal blinds with slats."""
        bbox = geometry['treatment_bbox']
        x, y, w, h = bbox
        
        # Slat parameters
        slat_width = 50  # pixels
        slat_spacing = 2
        slat_angle = settings.get('slat_angle', 0)  # 0-90 degrees
        
        num_slats = h // (slat_width + slat_spacing)
        
        # Create canvas
        blinds = np.zeros((h, w, 4), dtype=np.uint8)  # RGBA
        
        # Tile texture for single slat
        slat_texture = self._tile_texture(swatch, (w, slat_width))
        
        # Draw each slat
        for i in range(num_slats):
            slat_y = i * (slat_width + slat_spacing)
            
            if slat_y + slat_width > h:
                break
            
            # Place slat
            blinds[slat_y:slat_y + slat_width, :, :3] = slat_texture
            blinds[slat_y:slat_y + slat_width, :, 3] = 255
            
            # Add highlight/shadow based on angle
            if slat_angle != 0:
                intensity = 1.0 + (slat_angle / 180) * 0.3
                top_half = slice(slat_y, slat_y + slat_width // 2)
                blinds[top_half, :, :3] = np.clip(
                    blinds[top_half, :, :3] * intensity, 0, 255
                ).astype(np.uint8)
        
        return blinds
    
    def _create_shade(
        self,
        geometry: Dict,
        swatch: np.ndarray,
        settings: Dict
    ) -> np.ndarray:
        """Create roller or Roman shade."""
        bbox = geometry['treatment_bbox']
        x, y, w, h = bbox
        
        shade_type = settings.get('shade_type', 'roller')
        
        # Create canvas
        shade = np.zeros((h, w, 4), dtype=np.uint8)  # RGBA
        
        # Tile texture
        texture = self._tile_texture(swatch, (w, h))
        shade[:, :, :3] = texture
        
        # Set opacity based on fabric
        opacity = settings.get('opacity', 0.9)
        shade[:, :, 3] = int(255 * opacity)
        
        # For Roman shade, add horizontal folds
        if shade_type == 'roman':
            fold_spacing = h // 6  # 6 folds
            
            for i in range(1, 6):
                fold_y = i * fold_spacing
                
                # Darken fold line
                fold_region = slice(fold_y - 3, fold_y + 3)
                shade[fold_region, :, :3] = (shade[fold_region, :, :3] * 0.7).astype(np.uint8)
        
        return shade
    
    def _tile_texture(
        self,
        swatch: np.ndarray,
        target_size: Tuple[int, int]
    ) -> np.ndarray:
        """Tile swatch to fill target size seamlessly."""
        target_w, target_h = target_size
        swatch_h, swatch_w = swatch.shape[:2]
        
        # Resize swatch to appropriate tile size (256x256 is good balance)
        tile_size = 256
        swatch_resized = cv2.resize(swatch, (tile_size, tile_size))
        
        # Calculate how many tiles needed
        tiles_x = (target_w // tile_size) + 2
        tiles_y = (target_h // tile_size) + 2
        
        # Tile
        tiled = np.tile(swatch_resized, (tiles_y, tiles_x, 1))
        
        # Crop to exact size
        tiled = tiled[:target_h, :target_w]
        
        return tiled
    
    def _create_pleat_shading(
        self,
        width: int,
        height: int,
        num_pleats: int
    ) -> np.ndarray:
        """Create shading pattern for curtain pleats."""
        x = np.linspace(0, num_pleats * 2 * np.pi, width)
        shading = 0.85 + 0.15 * np.sin(x)  # Vary between 0.85 and 1.0
        
        # Expand to 2D
        shading_2d = np.tile(shading, (height, 1))
        
        return shading_2d
    
    def _create_shadows(
        self,
        mask: np.ndarray,
        depth_map: Optional[np.ndarray],
        geometry: Dict
    ) -> np.ndarray:
        """Create shadow layer for treatment."""
        h, w = mask.shape[:2]
        shadow = np.zeros((h, w), dtype=np.float32)
        
        if depth_map is None:
            # Simple shadow without depth
            # Assume light from top center
            light_direction = np.array([0, 1])  # Downward
        else:
            # Use depth to determine shadow direction
            light_direction = np.array([0.3, 1])
        
        # Get treatment bbox
        bbox = geometry['treatment_bbox']
        x, y, w_treat, h_treat = bbox
        
        # Create shadow offset based on depth
        offset_x = int(light_direction[0] * 10)
        offset_y = int(light_direction[1] * 15)
        
        # Shadow region (slightly offset from treatment)
        shadow_region = np.zeros_like(shadow)
        
        y1 = max(0, y + offset_y)
        y2 = min(h, y + h_treat + offset_y)
        x1 = max(0, x + offset_x)
        x2 = min(w, x + w_treat + offset_x)
        
        shadow_region[y1:y2, x1:x2] = 0.3  # Shadow intensity
        
        # Blur shadow for softness
        shadow_region = cv2.GaussianBlur(shadow_region, (21, 21), 0)
        
        return shadow_region
    
    def _match_room_lighting(
        self,
        treatment: np.ndarray,
        room_image: np.ndarray,
        mask: np.ndarray
    ) -> np.ndarray:
        """Adjust treatment colors to match room lighting."""
        # Sample room colors around window
        mask_dilated = cv2.dilate(mask, np.ones((50, 50), np.uint8))
        room_sample_region = (mask_dilated == 0)
        
        if room_sample_region.sum() > 100:
            # Get average color of room
            room_colors = room_image[room_sample_region]
            avg_room_color = room_colors.mean(axis=0)
            
            # Calculate color temperature
            room_brightness = avg_room_color.mean() / 255.0
            
            # Adjust treatment brightness to match
            treatment_rgb = treatment[:, :, :3].astype(np.float32)
            treatment_brightness = treatment_rgb.mean() / 255.0
            
            if treatment_brightness > 0:
                brightness_ratio = room_brightness / treatment_brightness
                # Limit adjustment to avoid oversaturation
                brightness_ratio = np.clip(brightness_ratio, 0.7, 1.3)
                
                treatment[:, :, :3] = np.clip(
                    treatment_rgb * brightness_ratio, 0, 255
                ).astype(np.uint8)
        
        return treatment
    
    def _composite(
        self,
        background: np.ndarray,
        treatment: np.ndarray,
        shadow: np.ndarray,
        mask: np.ndarray,
        geometry: Dict
    ) -> np.ndarray:
        """Composite treatment and shadow onto background."""
        result = background.copy()
        
        # Get treatment bbox
        bbox = geometry['treatment_bbox']
        x, y, w, h = bbox
        
        # Ensure bbox is within image bounds
        img_h, img_w = result.shape[:2]
        x = max(0, x)
        y = max(0, y)
        w = min(w, img_w - x)
        h = min(h, img_h - y)
        
        if w <= 0 or h <= 0:
            return result
        
        # Crop treatment to fit
        treatment_cropped = treatment[:h, :w]
        
        # Apply shadow first (darken background)
        shadow_region = result[y:y+h, x:x+w].astype(np.float32)
        shadow_cropped = shadow[y:y+h, x:x+w]
        
        for c in range(3):
            shadow_region[:, :, c] *= (1 - shadow_cropped)
        
        result[y:y+h, x:x+w] = shadow_region.astype(np.uint8)
        
        # Alpha blend treatment
        alpha = treatment_cropped[:, :, 3:4] / 255.0
        treatment_rgb = treatment_cropped[:, :, :3]
        background_rgb = result[y:y+h, x:x+w]
        
        blended = (treatment_rgb * alpha + background_rgb * (1 - alpha)).astype(np.uint8)
        result[y:y+h, x:x+w] = blended
        
        # Smooth edges
        result = self._blend_edges(result, x, y, w, h)
        
        return result
    
    def _blend_edges(
        self,
        image: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int
    ) -> np.ndarray:
        """Blend edges of treatment for smooth integration."""
        # Create soft mask at boundaries
        edge_width = 5
        
        # Blur small region around edges
        regions = [
            (y-edge_width, y+edge_width, x, x+w),  # Top edge
            (y+h-edge_width, y+h+edge_width, x, x+w),  # Bottom edge
            (y, y+h, x-edge_width, x+edge_width),  # Left edge
            (y, y+h, x+w-edge_width, x+w+edge_width),  # Right edge
        ]
        
        img_h, img_w = image.shape[:2]
        
        for y1, y2, x1, x2 in regions:
            y1 = max(0, y1)
            y2 = min(img_h, y2)
            x1 = max(0, x1)
            x2 = min(img_w, x2)
            
            if y2 > y1 and x2 > x1:
                region = image[y1:y2, x1:x2]
                blurred = cv2.GaussianBlur(region, (5, 5), 0)
                image[y1:y2, x1:x2] = blurred
        
        return image


def load_swatch(path: str) -> np.ndarray:
    """Load swatch image."""
    import os
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Swatch not found: {path}")
    
    swatch = cv2.imread(path)
    
    if swatch is None:
        raise ValueError(f"Failed to load swatch image: {path}")
    
    swatch = cv2.cvtColor(swatch, cv2.COLOR_BGR2RGB)
    return swatch
