# Data Collection Strategy

Training data collection plan for fine-tuning YOLOv8 and SDXL models if prototype validation determines higher quality is needed.

**Execute only if:** Prototype quality <6.5/10 but sales rep interest >70%

---

## Overview

**Goal:** Collect sufficient training data to fine-tune:
1. **YOLOv8** for interior window detection (800 images)
2. **SDXL LoRA** for photorealistic treatment rendering (150-200 pairs)

**Timeline:** 3-4 weeks

**Budget:** ~$3,000

**Team:** 2-3 people (can be part-time)

---

## YOLOv8 Window Detection Dataset

### Target Dataset

**Size:** 800 labeled images

**Breakdown:**
- Training set: 640 images (80%)
- Validation set: 80 images (10%)
- Test set: 80 images (10%)

### Image Requirements

**Content:**
- Interior room photos (perspective from inside room looking at window)
- Variety of window types:
  - Standard single/double hung (40%)
  - Bay windows (15%)
  - Sliding glass doors (15%)
  - Floor-to-ceiling windows (10%)
  - Small bathroom/kitchen windows (10%)
  - French doors (5%)
  - Other (skylights, corner windows) (5%)

**Diversity:**
- Different room types: bedroom, living room, kitchen, bathroom, office
- Various lighting: bright, dim, backlit, artificial, natural
- Different wall colors and textures
- Furniture present/absent
- With and without existing treatments

**Quality:**
- Resolution: 1920x1080 minimum
- Format: JPG or PNG
- Well-focused (not blurry)
- Various angles (straight-on preferred, but include some angled)

### Data Sources

#### Source 1: Real Estate Listings (Free, 400 images)

**Platforms:**
- Zillow
- Realtor.com
- Redfin
- Local MLS (if accessible)

**Process:**
1. Search for listings with interior photos
2. Download room photos showing windows clearly
3. Prioritize high-end listings (better photo quality)
4. Respect copyright - for training use only (fair use)

**Automated scraping:**

```python
# training/scripts/scrape_zillow.py
# Use with caution - check ToS
# Implement rate limiting
# Rotate user agents
# Download only what's needed
```

**Manual collection:**
- 1-2 hours per day for 2 weeks
- ~30-50 images per hour
- Total: ~400 images

#### Source 2: Interior Design Websites (Free, 200 images)

**Platforms:**
- Houzz
- Pinterest
- Interior design blogs
- Architectural Digest online
- Elle Decor

**Process:**
- Search for room photos with visible windows
- Download high-resolution versions
- Credit photographers (for internal use only)

**Time:** 1 week, 2-3 hours per day

#### Source 3: Sales Team Archives (Free, 100 images)

**Source:**
- Past customer consultations
- Before photos from installations
- Measurement appointment photos

**Process:**
1. Request photos from sales team
2. Strip customer identifying information
3. Organize by window type

**Privacy:**
- Get customer consent if possible
- Remove EXIF location data
- Blur/crop out personal items

**Time:** 1 week to collect from team

#### Source 4: Original Photography (Cost: $500-1000, 100 images)

**Approach:**
- Visit model homes, show homes, furniture stores
- Take systematic photos of different window setups

**Equipment needed:**
- Good camera or high-end smartphone
- Tripod (for consistent framing)
- Measuring tape (for scale reference)

**Locations:**
- Model homes (get permission from builder)
- Furniture showrooms (IKEA, etc.)
- Friend/family homes (with permission)
- Office buildings (with permission)

**Time:** 2 weeks, visiting 5-10 locations

**Cost:** Minimal (gas, maybe small location fees)

### Labeling Process

**Tool:** [LabelImg](https://github.com/heartexlabs/labelImg)

**Setup:**
```bash
pip install labelImg
labelImg
```

**Labeling workflow:**

1. Open image in LabelImg
2. Draw bounding box around each window
3. Label class: `window`, `sliding_door`, `french_door`, or `skylight`
4. Include frame but not excess wall
5. For multiple windows, label each separately
6. Save in YOLO format

**Output:** `.txt` file per image

```
# Format: class_id x_center y_center width height (normalized 0-1)
0 0.512 0.35 0.28 0.45
0 0.782 0.35 0.28 0.45
```

**Time estimate:**
- Experienced labeler: ~20-30 seconds per image
- 800 images × 30 seconds = 400 minutes = **6-7 hours total**

**Team approach:**
- 2 people × 3-4 hours each = done in 1 day
- Quality check by second person

**Quality control:**
- Random sample 10% for double-checking
- Ensure consistency in what's included (frame vs glass only)
- Verify class labels correct

### Dataset Organization

```
training/window_detection/
├── images/
│   ├── train/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   ├── val/
│   │   ├── img641.jpg
│   │   └── ...
│   └── test/
│       ├── img721.jpg
│       └── ...
├── labels/
│   ├── train/
│   │   ├── img001.txt
│   │   ├── img002.txt
│   │   └── ...
│   ├── val/
│   │   └── ...
│   └── test/
│       └── ...
└── dataset.yaml
```

**dataset.yaml:**

```yaml
path: /workspace/training/window_detection
train: images/train
val: images/val
test: images/test

nc: 4  # number of classes
names: ['window', 'sliding_door', 'french_door', 'skylight']
```

---

## SDXL Fine-Tuning Dataset

### Target Dataset

**Size:** 150-200 before/after pairs

**What you need:**
- **Before:** Room photo with empty/untreated window
- **After:** Same room/window with treatment installed
- **Mask:** Window region mask
- **Caption:** Description of treatment

### Image Requirements

**Matching pairs:**
- Same camera position
- Same lighting conditions
- Same room (obviously)
- Only difference: window treatment

**Quality:**
- High resolution (2048x2048 minimum for SDXL)
- Sharp focus
- Good lighting
- Professional or semi-professional photography

**Treatment diversity:**
- Curtains/drapes (50%)
- Roller shades (20%)
- Blinds (20%)
- Roman shades (10%)

**Fabric diversity:**
- Solid colors (60%)
- Patterns (20%)
- Sheers (10%)
- Blackout (10%)

### Data Sources

#### Source 1: Vendor Before/After Photos (Free, 50 pairs)

**Approach:**
- Contact window treatment vendors/manufacturers
- Request before/after installation photos
- Many vendors have marketing materials with such photos

**Outreach script:**

```
Subject: Partnership Opportunity - Training Data Request

Dear [Vendor],

We're developing an AI visualization tool for window treatments 
that will help sales professionals showcase your products to customers.

Would you be willing to share before/after installation photos from 
your portfolio? We need the images for training our AI model. 
Your products would be featured prominently in our system.

We can credit your company and potentially establish a partnership.

[Your details]
```

**Vendors to contact:**
- Your current suppliers (leverage existing relationships)
- Major brands: Hunter Douglas, Levolor, Bali, etc.
- Local custom treatment makers

**Time:** 2-3 weeks for outreach and collection

**Success rate:** ~30-40% response rate

#### Source 2: Staged Photography (Cost: $2000-2500, 50 pairs)

**Most reliable but most expensive option.**

**Approach:**
- Hire professional photographer
- Stage 10-15 different rooms
- Photograph each room:
  - Before (empty window)
  - After (with 3-4 different treatments)
- Result: 40-60 pairs from ~15 rooms

**Locations:**
- Model homes (negotiate access)
- Furniture showrooms
- AirBnB properties (rent for day shoot)
- Sales team/employee homes

**Equipment:**
- Professional DSLR
- Tripod (essential for matching angles)
- Lighting setup
- Color calibration chart

**Treatment samples:**
- Borrow from vendors
- Use temporary mounting
- Quick-change setups (roller shades, clip-on curtains)

**Photographer cost:**
- Professional: $200-300/hour × 8 hours = $1600-2400
- Or experienced amateur: $50-100/hour

**Time:** 1-2 full days of shooting

**Post-processing:**
- Color correction
- Alignment verification
- Cropping/resizing

#### Source 3: Customer Installations (Free, 30 pairs)

**Approach:**
- Sales team takes before photos during measurement appointments
- Returns after installation for after photo
- Customer consent required

**Process:**
1. Train sales team on photo requirements
2. Provide camera positioning guide
3. Standardize: same angle, time of day, lighting
4. Collect over 2-3 months

**Challenges:**
- Time lag (installations not immediate)
- Inconsistent quality
- Lighting/angle variations
- Customer privacy concerns

**Incentive for sales team:**
- Small bonus per usable pair ($10-20)
- Gamification (leaderboard)

#### Source 4: 3D Rendering (Cost: $500, 20 pairs)

**Approach:**
- Use Blender to render synthetic room scenes
- Generate before/after programmatically

**Benefits:**
- Perfect matching (identical camera position)
- Infinite variation
- Controlled lighting
- No cost per image (after initial setup)

**Drawbacks:**
- May not generalize to real photos
- Requires 3D modeling skill
- Risk of "uncanny valley" - too perfect

**Setup:**
- Download/purchase room 3D models
- Set up window treatment models
- Render pipeline script

**Time:** 1 week setup, then automated generation

### Dataset Annotation

For each pair, create:

**1. Before image** (before.jpg)
**2. After image** (after.jpg)
**3. Mask** (mask.png)
- White where treatment is
- Black elsewhere
- Can generate from before/after difference

**4. Caption** (caption.txt)

```
realistic linen curtain panels in natural beige, 
hanging from ceiling to floor, soft natural lighting, 
bedroom interior, gentle folds and draping
```

**Caption template:**

```
realistic [material] [treatment_type] in [color],
[mounting description], [lighting conditions],
[room type], [fabric characteristics]
```

**Auto-caption generation:**

```python
# training/scripts/generate_captions.py
def generate_caption(metadata):
    return f"realistic {metadata['material']} {metadata['treatment']} " \
           f"in {metadata['color']}, {metadata['lighting']}, " \
           f"{metadata['room_type']}, {metadata['fabric_detail']}"
```

### Dataset Organization

```
training/sdxl_lora/
├── train/
│   ├── pair_001/
│   │   ├── before.jpg
│   │   ├── after.jpg
│   │   ├── mask.png
│   │   └── caption.txt
│   ├── pair_002/
│   │   └── ...
│   └── ...
├── val/
│   ├── pair_151/
│   │   └── ...
│   └── ...
└── metadata.json
```

**metadata.json:**

```json
{
  "pairs": [
    {
      "id": "pair_001",
      "before": "train/pair_001/before.jpg",
      "after": "train/pair_001/after.jpg",
      "mask": "train/pair_001/mask.png",
      "caption": "realistic linen curtain...",
      "metadata": {
        "room_type": "bedroom",
        "treatment_type": "curtains",
        "material": "linen",
        "color": "natural beige",
        "vendor": "Acme",
        "lighting": "natural daylight"
      }
    }
  ]
}
```

---

## Data Quality Standards

### Rejection Criteria

**Reject if:**
- Blurry or out of focus
- Extreme angles (>30° off perpendicular)
- Very dark (<10% average brightness)
- Overexposed (>90% clipped highlights)
- Window heavily obstructed (>50% blocked)
- Multiple windows if can't label all
- Copyright/watermark issues

### Quality Checklist

For each image:
- [ ] Resolution meets minimum
- [ ] Window clearly visible
- [ ] Good focus
- [ ] Acceptable lighting
- [ ] No privacy concerns
- [ ] No copyright violations
- [ ] Suitable for purposes

### Review Process

1. Initial collection (team members)
2. Quality filter (automated script checks resolution, brightness)
3. Manual review (lead reviewer spot-checks 20%)
4. Final approval

---

## Timeline & Milestones

### Week 1-2: YOLOv8 Data Collection

- Days 1-3: Scrape real estate listings (400 images)
- Days 4-7: Interior design sites (200 images)
- Days 8-10: Sales team archives (100 images)
- Days 11-14: Original photography (100 images)

**Deliverable:** 800 unlabeled images

### Week 2-3: YOLOv8 Labeling

- Day 15-16: Set up LabelImg, train labelers
- Days 17-21: Labeling (6-7 hours total, can parallelize)
- Day 22: Quality review and corrections

**Deliverable:** 800 labeled images in YOLO format

### Week 3-4: SDXL Data Collection

- Days 15-21: Vendor outreach (50 pairs)
- Days 22-23: Staged photography (50 pairs)
- Days 24-28: Customer installations start (30 pairs over time)
- Day 29-30: 3D rendering setup (20 pairs)

**Deliverable:** 150 before/after pairs

### Week 4-5: SDXL Annotation

- Days 29-35: Generate masks (automated + manual)
- Days 32-35: Write captions (can use template + manual review)

**Deliverable:** 150 annotated pairs ready for training

---

## Budget Breakdown

| Item | Cost | Notes |
|------|------|-------|
| Real estate photos | $0 | Fair use |
| Interior design sites | $0 | Fair use |
| Sales team archives | $0 | Internal |
| Photography (staged) | $2,000 | Professional photographer |
| Photography (locations) | $300 | Location fees, travel |
| 3D rendering setup | $200 | Models, software |
| Labeling tools | $0 | Open source |
| Team time (80 hours) | $0 | Internal allocation |
| **Total** | **$2,500** | **One-time cost** |

---

## Legal & Ethical Considerations

### Copyright

- Real estate/design photos: Fair use for training (non-commercial initially)
- Vendor photos: Get explicit permission
- Customer photos: Written consent required
- 3D models: Use licensed/purchased models

### Privacy

- Remove EXIF GPS data
- Blur identifiable information (family photos, addresses)
- Customer consent forms
- Anonymize data storage

### Data Retention

- Keep raw data backed up
- Don't distribute publicly
- Delete customer data upon request
- Secure storage (encrypted)

---

## Quality Assurance

### Automated Checks

```python
# training/scripts/validate_dataset.py

def validate_yolo_dataset(dataset_path):
    """Check YOLO dataset integrity"""
    # Check all images have labels
    # Verify label format
    # Check bounding boxes within image bounds
    # Validate class IDs
    # Check train/val/test split ratios
    
def validate_sdxl_dataset(dataset_path):
    """Check SDXL dataset integrity"""
    # Verify before/after pairs exist
    # Check image dimensions match
    # Validate mask dimensions
    # Check captions exist and non-empty
    # Verify metadata JSON structure
```

### Manual Review Sample

- Review 10% of dataset manually
- Check labeling accuracy
- Verify caption quality
- Ensure image quality standards met

---

## Fallback Strategies

**If can't collect 800 YOLO images:**
- Minimum viable: 400-500 images
- Use data augmentation aggressively
- Accept lower detection accuracy initially

**If can't collect 150 SDXL pairs:**
- Minimum viable: 50-75 pairs
- Use synthetic data (3D rendering)
- Train with higher learning rate (riskier but faster)
- Accept some quality loss

**If budget too high:**
- Skip professional photography
- Focus on free sources (800 YOLO, 50 SDXL)
- Use more synthetic data
- Extend timeline to collect customer installations

---

## Deliverables

Upon completion:
- [ ] 800 labeled YOLOv8 training images
- [ ] 150 annotated SDXL before/after pairs
- [ ] Dataset validation reports
- [ ] Data source documentation
- [ ] Backup copies (3 locations)

**Ready for:** Phase 2 model training

---

**Document Version:** 1.0  
**Last Updated:** February 16, 2026  
**Owner:** Development Team
