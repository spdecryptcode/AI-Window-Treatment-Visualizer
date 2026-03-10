# Swatch Management Guide

How to add, organize, and maintain vendor swatch libraries for the Window Treatment Visualizer.

---

## Overview

The swatch system manages fabric and material samples that sales reps apply to window treatments in customer visualizations.

**Key Concepts:**
- **Swatch** = Single fabric/material sample with images and metadata
- **Vendor** = Manufacturer/supplier providing materials
- **Treatment Type** = Category (curtains, blinds, shades, etc.)
- **Diffuse Map** = Main fabric texture image
- **Normal Map** = Generated surface detail enhancement (optional)

---

## Swatch Database Structure

**Tables:**

**vendors**
- `id` - Unique vendor ID
- `name` - Vendor/manufacturer name
- `catalog_url` - Link to online catalog
- `contact_info` - Sales contact details
- `created_at` - Date added

**swatches**
- `id` - Unique swatch ID
- `vendor_id` - Foreign key to vendors table
- `treatment_type` - curtains, blinds, shades, etc.
- `material_name` - Material type (e.g., "100% Linen")
- `color_name` - Color name (e.g., "Natural Beige")
- `color_hex` - Dominant color as hex code
- `texture_path` - Path to texture image
- `normal_path` - Path to normal map (if exists)
- `opacity` - 0.0 (opaque) to 1.0 (sheer)
- `price_tier` - budget, mid-range, premium
- `sku` - Vendor SKU/product code
- `created_at` - Date added

**Storage:**
- SQLite database: `data/swatches.db`
- Images: `materials/swatches/[vendor_name]/[treatment_type]/`

---

## Adding New Vendor

### Step 1: Create Vendor Entry

```bash
# Using CLI script
docker-compose exec backend python scripts/add_vendor.py \
  --name "Acme Window Coverings" \
  --catalog "https://acme.com/catalog" \
  --contact "sales@acme.com"

# Returns: Vendor ID: 5
```

**Or manually via SQL:**

```sql
# Connect to database
sqlite3 data/swatches.db

# Insert vendor
INSERT INTO vendors (name, catalog_url, contact_info)
VALUES ('Acme Window Coverings', 'https://acme.com/catalog', 'sales@acme.com');

# Get ID
SELECT id FROM vendors WHERE name = 'Acme Window Coverings';
```

### Step 2: Create Vendor Directory

```bash
# Create directory structure
mkdir -p materials/swatches/acme_window_coverings/curtains
mkdir -p materials/swatches/acme_window_coverings/blinds
mkdir -p materials/swatches/acme_window_coverings/shades
```

**Directory naming:**
- Use lowercase
- Replace spaces with underscores
- ASCII characters only

---

## Adding Individual Swatches

### Swatch Image Requirements

**Format:** JPG or PNG

**Resolution:**
- **Minimum:** 512x512 pixels
- **Recommended:** 1024x1024 pixels
- **Maximum:** 4096x4096 pixels

**Quality:**
- High-resolution macro photography
- Even lighting (no harsh shadows)
- Color-accurate (calibrated photography)
- Flat/straight-on view (perpendicular to fabric)
- Fill entire frame with fabric texture
- No borders, labels, or watermarks

**Color calibration:**
- Use color chart during photography
- Shoot in RAW, export to sRGB color space
- Avoid phone cameras (use DSLR if possible)

**File naming convention:**

```
[vendor]_[material]_[color].jpg

Examples:
acme_linen_natural_beige.jpg
acme_faux_wood_oak_medium.jpg
acme_polyester_gray_charcoal.jpg
```

Use:
- Lowercase
- Underscores (no spaces)
- Descriptive color names
- No special characters

### Manual Addition Process

**Step 1: Prepare Image**

1. Acquire fabric swatch image (from vendor or photograph sample)
2. Crop to show only fabric texture (no background)
3. Resize to 1024x1024 (square)
4. Save as JPG at 90% quality
5. Name according to convention

**Step 2: Place Image File**

```bash
# Copy to appropriate directory
cp acme_linen_natural_beige.jpg \
  materials/swatches/acme_window_coverings/curtains/
```

**Step 3: Add to Database**

```bash
# Using import script
docker-compose exec backend python scripts/add_swatch.py \
  --vendor-id 5 \
  --treatment-type curtains \
  --material "100% Linen" \
  --color "Natural Beige" \
  --texture-path "acme_window_coverings/curtains/acme_linen_natural_beige.jpg" \
  --opacity 0.9 \
  --price-tier mid-range \
  --sku "ACME-LIN-NB-001"

# System will:
# - Process image (create seamless tileable version)
# - Generate pseudo-normal map
# - Extract dominant color
# - Create thumbnail
# - Insert into database
```

**Or via SQL:**

```sql
INSERT INTO swatches (
  vendor_id, 
  treatment_type, 
  material_name, 
  color_name,
  color_hex,
  texture_path,
  opacity,
  price_tier,
  sku
) VALUES (
  5,
  'curtains',
  '100% Linen',
  'Natural Beige',
  '#E8DCC8',  -- Extract using color picker tool
  'acme_window_coverings/curtains/acme_linen_natural_beige.jpg',
  0.9,
  'mid-range',
  'ACME-LIN-NB-001'
);
```

---

## Bulk Import

### From Vendor Catalog

**If vendor provides fabric images:**

**Step 1: Organize Files**

Create directory structure:

```
/tmp/vendor_import/
├── vendor_info.json
└── swatches/
    ├── curtains/
    │   ├── fabric1.jpg
    │   ├── fabric2.jpg
    ├── blinds/
    │   ├── wood1.jpg
    │   ├── wood2.jpg
    └── shades/
        ├── cellular1.jpg
```

**Step 2: Create Metadata File**

`vendor_info.json`:

```json
{
  "vendor": {
    "name": "Acme Window Coverings",
    "catalog_url": "https://acme.com",
    "contact": "sales@acme.com"
  },
  "swatches": [
    {
      "file": "curtains/fabric1.jpg",
      "treatment_type": "curtains",
      "material": "100% Linen",
      "color": "Natural Beige",
      "opacity": 0.9,
      "price_tier": "mid-range",
      "sku": "ACME-LIN-NB-001"
    },
    {
      "file": "curtains/fabric2.jpg",
      "treatment_type": "curtains",
      "material": "Cotton Blend",
      "color": "Snow White",
      "opacity": 0.85,
      "price_tier": "budget",
      "sku": "ACME-CTN-SW-002"
    }
  ]
}
```

**Step 3: Run Bulk Import**

```bash
docker-compose exec backend python scripts/bulk_import.py \
  /tmp/vendor_import/vendor_info.json

# Output:
# Processing vendor: Acme Window Coverings
# Importing 2 swatches...
# ✓ curtains/fabric1.jpg -> Swatch ID 101
# ✓ curtains/fabric2.jpg -> Swatch ID 102
# Complete! Imported 2 swatches.
```

### From Excel/CSV

**If vendor provides spreadsheet catalog:**

**Step 1: Prepare CSV**

`swatches_import.csv`:

```csv
vendor_name,treatment_type,material,color,image_filename,opacity,price_tier,sku
Acme,curtains,100% Linen,Natural Beige,acme_001.jpg,0.9,mid-range,ACME-LIN-NB-001
Acme,curtains,Cotton Blend,Snow White,acme_002.jpg,0.85,budget,ACME-CTN-SW-002
```

**Step 2: Place Images**

Copy all swatch images to temporary directory matching CSV filenames.

**Step 3: Import**

```bash
docker-compose exec backend python scripts/import_from_csv.py \
  /path/to/swatches_import.csv \
  /path/to/images/

# Validates CSV format
# Checks all images exist
# Processes and imports
```

---

## Swatch Processing Pipeline

When adding swatches, the system automatically:

### 1. Image Validation

- Checks file format (JPG/PNG)
- Verifies resolution (>= 512x512)
- Confirms square aspect ratio (or crops to square)
- Checks file size (< 25MB)

### 2. Seamless Tiling

Converts swatch to seamless tileable texture:

```python
# backend/processing/swatch_processor.py

def make_seamless(image):
    """Convert fabric swatch to seamless tileable texture"""
    # Clone stamp edges using overlap blending
    # Ensures no visible seam when tiled 4x4 or larger
    # Output: seamless texture map
```

This ensures fabric doesn't show repeating edges when applied to large curtains.

### 3. Normal Map Generation

Creates pseudo-normal map from texture:

```python
def generate_normal_map(diffuse_image):
    """Create normal map from fabric texture for depth"""
    # Convert to grayscale (height map)
    # Calculate surface gradients (Sobel filter)
    # Encode as RGB normal map
    # Adds subtle 3D appearance to flat fabric
```

Optional but improves realism.

### 4. Color Extraction

Analyzes swatch to extract dominant color:

```python
def extract_dominant_color(image):
    """Get primary color as hex code"""
    # K-means clustering on RGB values
    # Returns most prominent color (ignoring neutrals)
    # Stored as hex for filtering in UI
```

Used for swatch gallery color filtering.

### 5. Thumbnail Creation

Generates preview thumbnails:

- **200x200** - Gallery thumbnail
- **500x500** - Hover preview
- **1024x1024** - Full texture (original or processed)

### 6. Opacity Analysis (Optional)

For sheer fabrics, analyzes transparency:

```python
def measure_opacity(fabric_image):
    """Estimate fabric opacity/sheerness"""
    # Analyze pixel brightness distribution
    # 0.0 = fully opaque
    # 0.5 = semi-sheer
    # 1.0 = very sheer
```

Can be manually overridden in metadata.

---

## Organizing Swatches

### Treatment Type Categories

**curtains:**
- Drapery panels
- Sheer curtains
- Layerable panels

**blinds:**
- Wood blinds
- Faux wood
- Aluminum

**shades:**
- Roller shades
- Roman shades
- Cellular/honeycomb

**vertical_blinds:**
- Vertical slats
- Panel track

**shutters:**
- Wood shutters
- Composite shutters

**Others:**
- Add custom categories as needed

### Color Organization

**Best practices:**

1. Use consistent color naming across vendors
2. Standard names: White, Beige, Gray, Tan, Brown, Blue, Green, etc.
3. Avoid marketing names like "Driftwood Dreams" (use "Light Gray")
4. Store original marketing name in notes field

**Color tags for filtering:**

```sql
# Add color tags to enable filtering
UPDATE swatches 
SET tags = 'neutral,warm,beige' 
WHERE color_name LIKE '%beige%';
```

### Price Tiers

**Standard tiers:**
- `budget` - Value/economy options
- `mid-range` - Standard quality
- `premium` - High-end/luxury
- `custom` - Specialty/made-to-order

**Setting price tier:**

Helps sales reps filter based on customer budget during consultation.

---

## Updating Swatches

### Update Metadata

```bash
# Update swatch details
docker-compose exec backend python scripts/update_swatch.py \
  --swatch-id 101 \
  --color "Warm Beige" \
  --price-tier premium \
  --sku "ACME-LIN-WB-001-V2"
```

**Or via SQL:**

```sql
UPDATE swatches 
SET color_name = 'Warm Beige',
    price_tier = 'premium',
    sku = 'ACME-LIN-WB-001-V2'
WHERE id = 101;
```

### Replace Texture Image

```bash
# 1. Replace file
cp new_image.jpg materials/swatches/acme/curtains/acme_linen_warm_beige.jpg

# 2. Reprocess
docker-compose exec backend python scripts/reprocess_swatch.py \
  --swatch-id 101

# Regenerates:
# - Seamless texture
# - Normal map
# - Thumbnails
# - Color extraction
```

### Archive Discontinued Swatches

```sql
# Don't delete - mark as archived
UPDATE swatches 
SET archived = TRUE,
    archived_date = CURRENT_TIMESTAMP
WHERE id = 101;

# Archived swatches don't show in gallery but remain in database
```

---

## Removing Swatches

### Soft Delete (Recommended)

```sql
# Mark as deleted (preserves data)
UPDATE swatches 
SET deleted = TRUE,
    deleted_date = CURRENT_TIMESTAMP
WHERE id = 101;
```

### Hard Delete

```bash
# Remove from database and filesystem
docker-compose exec backend python scripts/delete_swatch.py \
  --swatch-id 101 \
  --confirm

# WARNING: Cannot be undone!
# Removes:
# - Database record
# - All image files
# - Thumbnails
```

---

## Swatch Quality Control

### Checklist for New Swatches

Before adding to production:

- [ ] Image is high resolution (1024x1024 minimum)
- [ ] Colors are accurate (not oversaturated)
- [ ] Lighting is even (no shadows or highlights)
- [ ] Texture shows fabric detail clearly
- [ ] File is properly named
- [ ] Metadata is complete (vendor, material, color, SKU)
- [ ] Treatment type category is correct
- [ ] Price tier assigned
- [ ] Test rendering looks good on sample room

### Testing New Swatches

```bash
# Test render with new swatch
docker-compose exec backend python scripts/test_swatch.py \
  --swatch-id 101 \
  --test-image test_data/sample_rooms/bedroom_standard.jpg

# Generates preview using new swatch
# Check:
# - Texture tiles seamlessly
# - Color matches expected
# - Opacity looks correct
# - Rendering quality acceptable
```

### Common Issues

**Texture shows visible seam when tiled:**
- Swatch image wasn't truly square
- Edges have border/shadow
- Solution: Crop tighter, reprocess

**Color looks wrong in rendering:**
- Source image has color cast
- Improper white balance
- Solution: Color-correct source image, re-upload

**Fabric looks too shiny/matte:**
- Normal map too strong/weak
- Solution: Regenerate with adjusted parameters

**File size too large:**
- Resolution too high (>4096px)
- PNG instead of JPG
- Solution: Resize to 1024px, convert to JPG 90% quality

---

## Advanced: Custom Material Properties

For specialized materials:

### PBR Material Properties

Define advanced rendering properties:

```sql
ALTER TABLE swatches ADD COLUMN pbr_properties JSON;

UPDATE swatches 
SET pbr_properties = '{
  "roughness": 0.6,
  "metallic": 0.0,
  "specular": 0.2,
  "sheen": 0.4
}'
WHERE id = 101;
```

**Properties:**
- `roughness` (0-1): 0=glossy, 1=matte
- `metallic` (0-1): 0=fabric, 1=metallic sheen
- `specular` (0-1): Reflection intensity
- `sheen` (0-1): Fabric sheen (like silk)

### Custom Texture Maps

For high-end rendering:

```
materials/swatches/vendor/treatment_type/
├── fabric_diffuse.jpg      # Main texture
├── fabric_normal.jpg        # Surface detail
├── fabric_roughness.jpg     # Roughness map
├── fabric_specular.jpg      # Specular/gloss map
└── fabric_opacity.jpg       # Transparency map (for sheers)
```

Reference in database:

```sql
UPDATE swatches 
SET normal_path = 'vendor/curtains/fabric_normal.jpg',
    roughness_path = 'vendor/curtains/fabric_roughness.jpg',
    specular_path = 'vendor/curtains/fabric_specular.jpg',
    opacity_path = 'vendor/curtains/fabric_opacity.jpg'
WHERE id = 101;
```

---

## Backup & Restore

### Backup Swatch Database

```bash
# Backup database
cp data/swatches.db backups/swatches_$(date +%Y%m%d).db

# Backup all swatch images
tar -czf backups/swatch_images_$(date +%Y%m%d).tar.gz materials/swatches/
```

### Restore from Backup

```bash
# Restore database
cp backups/swatches_20260216.db data/swatches.db

# Restore images
tar -xzf backups/swatch_images_20260216.tar.gz -C ./
```

### Export Catalog

```bash
# Export entire catalog to portable format
docker-compose exec backend python scripts/export_catalog.py \
  --output exports/catalog_export_$(date +%Y%m%d).zip

# Creates ZIP with:
# - swatches.db (SQLite database)
# - All swatch images
# - catalog.json (human-readable)
# - README.txt
```

---

## API Access

### Query Swatches via API

```bash
# Get all swatches
curl http://localhost:8000/api/swatches

# Filter by treatment type
curl http://localhost:8000/api/swatches?treatment_type=curtains

# Filter by vendor
curl http://localhost:8000/api/swatches?vendor_id=5

# Filter by color
curl http://localhost:8000/api/swatches?color=beige

# Filter by price tier
curl http://localhost:8000/api/swatches?price_tier=budget
```

**Response:**

```json
{
  "swatches": [
    {
      "id": 101,
      "vendor_name": "Acme Window Coverings",
      "treatment_type": "curtains",
      "material": "100% Linen",
      "color": "Natural Beige",
      "color_hex": "#E8DCC8",
      "opacity": 0.9,
      "price_tier": "mid-range",
      "sku": "ACME-LIN-NB-001",
      "thumbnail_url": "/swatches/thumb/101.jpg",
      "preview_url": "/swatches/preview/101.jpg"
    }
  ],
  "total": 1
}
```

---

## Admin Panel

Access admin interface at: `http://localhost:3000/admin`

**Features:**
- Upload swatches via drag-and-drop
- Edit metadata inline
- Preview renders
- Bulk operations
- Vendor management
- Archive/delete
- Export catalog

**Authentication:**
Default credentials in production deployment guide.

---

## Best Practices Summary

1. **Consistent naming** - Use standardized file naming convention
2. **Color accuracy** - Calibrate photography, sRGB color space
3. **High resolution** - Don't compromise on image quality
4. **Complete metadata** - Fill all fields (SKU, material, price tier)
5. **Test before production** - Render samples before deploying
6. **Regular backups** - Weekly database + image backups
7. **Archive, don't delete** - Preserve historical data
8. **Organize by vendor** - Clear directory structure
9. **Document sources** - Note where images came from
10. **Version control** - Track changes to catalog

---

**Support:** support@yourcompany.com  
**Guide Version:** 1.0  
**Last Updated:** February 16, 2026
