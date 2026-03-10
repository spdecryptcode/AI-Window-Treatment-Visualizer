#!/usr/bin/env python3
"""Create synthetic fabric swatches for testing."""

import numpy as np
import cv2
from pathlib import Path

# Create synthetic fabric swatches
swatches = {
    'curtains': {
        'linen_beige': (220, 200, 180),
        'cotton_white': (245, 245, 240),
        'linen_gray': (180, 180, 180),
        'velvet_navy': (30, 40, 80),
        'silk_cream': (255, 250, 230)
    },
    'blinds': {
        'wood_oak': (160, 120, 80),
        'faux_wood_white': (230, 220, 210),
        'wood_walnut': (100, 70, 50),
        'aluminum_silver': (192, 192, 192)
    },
    'shades': {
        'roller_white': (250, 250, 250),
        'cellular_beige': (230, 215, 195),
        'roman_tan': (210, 180, 140)
    }
}

for category, items in swatches.items():
    swatch_dir = Path('swatches') / category
    swatch_dir.mkdir(parents=True, exist_ok=True)
    
    for name, color in items.items():
        # Create 512x512 texture
        texture = np.ones((512, 512, 3), dtype=np.uint8)
        texture[:] = color
        
        # Add subtle noise for fabric texture
        noise = np.random.randint(-10, 10, (512, 512, 3), dtype=np.int16)
        texture = np.clip(texture.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Save
        output_path = swatch_dir / f"{name}.jpg"
        cv2.imwrite(str(output_path), cv2.cvtColor(texture, cv2.COLOR_RGB2BGR))
        print(f"✓ Created {output_path}")

print("\n✅ Created 12 synthetic swatches")
