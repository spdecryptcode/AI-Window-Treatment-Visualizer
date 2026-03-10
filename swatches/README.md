# Fabric Swatches for Prototype Testing

This directory contains fabric/material swatches used for rendering window treatments.

## Directory Structure

```
swatches/
├── curtains/          # Curtain fabrics
│   ├── linen_beige.jpg
│   ├── cotton_white.jpg
│   ├── velvet_navy.jpg
│   └── ...
├── blinds/            # Blind materials  
│   ├── wood_oak.jpg
│   ├── faux_wood_white.jpg
│   ├── aluminum_silver.jpg
│   └── ...
└── shades/            # Shade fabrics
    ├── roller_white.jpg
    ├── cellular_beige.jpg
    ├── roman_tan.jpg
    └── ...
```

## Adding Swatches

### 1. Obtain Swatch Images

**Vendor Sources:**
- Request high-res fabric photos from vendors
- Scan physical swatch books at 300 DPI
- Use royalty-free fabric textures (see sources below)

**Requirements:**
- Format: JPEG or PNG
- Min size: 512x512 pixels
- Ideal size: 1024x1024 pixels
- Color accurate (calibrated lighting)
- Flat, evenly lit (no shadows)
- Straight-on view (no perspective)

### 2. Prepare Images

```bash
# Resize to optimal size (using ImageMagick)
convert original.jpg -resize 1024x1024^ -gravity center -extent 1024x1024 swatch.jpg

# Or using Python PIL
python -c "
from PIL import Image
img = Image.open('original.jpg')
img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
img.save('swatch.jpg', quality=95)
"
```

### 3. Naming Convention

Use descriptive names: `{material}_{color}.jpg`

**Examples:**
- `linen_beige.jpg`
- `cotton_white.jpg`
- `velvet_navy_blue.jpg`
- `wood_natural_oak.jpg`
- `faux_wood_espresso.jpg`
- `aluminum_brushed_silver.jpg`
- `cellular_honeycomb_cream.jpg`

### 4. Add to Correct Directory

```bash
# Place in appropriate treatment type folder
cp my_swatch.jpg swatches/curtains/
cp blind_material.jpg swatches/blinds/
cp shade_fabric.jpg swatches/shades/
```

## Quick Start with Sample Swatches

For immediate testing without vendor swatches, use these free texture sources:

### Free Fabric Textures

1. **Textures.com** (formerly CG Textures)
   - https://www.textures.com/
   - Search: "fabric", "linen", "cotton", "wood"
   - Free tier: 15 credits/day

2. **Unsplash** (Free, no attribution)
   - https://unsplash.com/s/photos/fabric-texture
   - Search: "linen texture", "cotton fabric", "wood grain"

3. **Pexels** (Free, no attribution)
   - https://www.pexels.com/search/fabric/
   - High-res, commercial use

4. **Poly Haven** (CC0 Textures)
   - https://polyhaven.com/textures
   - Search: "fabric", "wood"

### Example Download Script

```bash
#!/bin/bash

# Download sample swatches from Unsplash

mkdir -p swatches/{curtains,blinds,shades}

# Curtains (beige linen, white cotton, gray fabric)
curl -o swatches/curtains/linen_beige.jpg \
  "https://images.unsplash.com/photo-1541643600914-78b084683601?w=1024"

curl -o swatches/curtains/cotton_white.jpg \
  "https://images.unsplash.com/photo-1615486991829-3f5b6f33e6cf?w=1024"

curl -o swatches/curtains/fabric_gray.jpg \
  "https://images.unsplash.com/photo-1604075311531-4e433c01e0be?w=1024"

# Blinds (wood, faux wood, aluminum)
curl -o swatches/blinds/wood_oak.jpg \
  "https://images.unsplash.com/photo-1547389027-e2dfc6f17e3e?w=1024"

curl -o swatches/blinds/faux_wood_white.jpg \
  "https://images.unsplash.com/photo-1615486364838-58568c2c0d30?w=1024"

# Shades (roller white, cellular, roman tan)
curl -o swatches/shades/roller_white.jpg \
  "https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?w=1024"

echo "✓ Downloaded 6 sample swatches"
```

## Vendor Integration (Production)

For production, connect to vendor APIs or use their swatch libraries:

### 1. Hunter Douglas API
```python
# Example: Fetch swatches from vendor
import requests

response = requests.get('https://api.vendor.com/swatches', 
                       headers={'Authorization': 'Bearer YOUR_TOKEN'})

for swatch in response.json():
    image_url = swatch['image_url']
    # Download and save to swatches/
```

### 2. Manual Vendor Upload
- Export swatches from vendor software
- Batch rename using product codes
- Import via admin panel

## Swatch Metadata (Optional)

Create `metadata.json` in each directory for additional info:

```json
{
  "linen_beige.jpg": {
    "vendor": "Acme Fabrics",
    "product_code": "LIN-200-BG",
    "product_name": "Natural Linen - Beige",
    "price_per_yard": 24.99,
    "stock_status": "in_stock",
    "care_instructions": "Dry clean only",
    "properties": {
      "light_filtering": "semi-opaque",
      "texture": "medium_weave",
      "pattern": "solid"
    }
  }
}
```

## Testing Swatches

Verify swatches render correctly:

```bash
# Test single swatch
python test_pipeline.py --single test_images/living_room.jpg

# Test all swatches in category
python -c "
from pathlib import Path
from classical_renderer import load_swatch

for swatch in Path('swatches/curtains').glob('*.jpg'):
    img = load_swatch(str(swatch))
    print(f'✓ {swatch.name}: {img.shape}')
"
```

## Troubleshooting

### Issue: "Swatch not found"
- Check file extension (.jpg vs .jpeg)
- Ensure file is in correct treatment directory
- Verify filename has no spaces (use underscores)

### Issue: "Swatch looks distorted"
- Ensure square aspect ratio (1:1)
- Use high-res source (min 512x512)
- Check JPEG quality (use 90+)

### Issue: "Colors look wrong"
- Ensure proper color profile (sRGB)
- Avoid phone camera photos (lighting inconsistent)
- Use calibrated scanner or vendor-provided images

## Current Swatch Count

Run this to check your collection:

```bash
find swatches -name "*.jpg" -o -name "*.png" | wc -l
```

**Recommended minimum for testing:**
- Curtains: 5-10 swatches
- Blinds: 3-5 swatches
- Shades: 3-5 swatches

**Production target:**
- 50-100 swatches per category
- Covers vendor's full catalog
