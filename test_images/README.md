# Test Images Directory

This directory contains test images for validating the window treatment prototype.

## Purpose

Test images help evaluate:
- Window detection accuracy across different scenarios
- Segmentation quality for various window types
- Rendering realism in different lighting conditions
- Overall system performance

## Directory Structure

```
test_images/
├── single_window/        # One window, simple scenes
├── multiple_windows/     # Multiple windows in one image
├── challenging/          # Difficult cases (reflections, obstructions, etc.)
├── lighting/             # Various lighting conditions
├── room_types/           # Different room settings
└── edge_cases/           # Corner cases, failures
```

## Test Image Categories

Based on [TEST_CASES.md](../prototype/TEST_CASES.md), you need:

### 1. Single Window (5-10 images)
- Large picture window with clear view
- Standard double-hung window
- Bay window (3 sections)
- French doors with glass panes
- Sliding glass door

**Characteristics:**
- One primary window
- Good lighting
- Minimal obstructions
- Clear window boundaries

### 2. Multiple Windows (5-10 images)
- Living room with 2-3 windows
- Office with adjacent windows
- Bedroom with window pair
- Kitchen with window over sink + side window

**Characteristics:**
- 2-4 windows per image
- Various sizes
- Different orientations

### 3. Challenging Lighting (5-10 images)
- Bright backlight (sunny day)
- Low light / evening
- Mixed lighting (window + lamps)
- Shadowed window area
- Sun glare on glass

**Characteristics:**
- Tests depth estimation
- Tests shadow rendering
- Tests brightness matching

### 4. Window Types (5-10 images)
- Arched/curved top window
- Floor-to-ceiling window
- Transom window (above door)
- Corner windows (wrap around)
- Skylight (if applicable)

**Characteristics:**
- Non-standard shapes
- Unusual mounting scenarios
- Tests geometry calculation

### 5. Obstructions (3-5 images)
- Furniture in front of window
- Plants on windowsill
- Existing curtains (sheer)
- Blinds partially closed

**Characteristics:**
- Tests detection robustness
- Tests segmentation accuracy
- May cause failures (good to test)

### 6. Room Contexts (5-10 images)
- Living room
- Bedroom
- Kitchen
- Office/study
- Dining room

**Characteristics:**
- Different decor styles
- Various color schemes
- Real-world usage scenarios

## Acquiring Test Images

### Option 1: Free Stock Photos

**Unsplash** (Free, no attribution required)
```bash
# Search terms: "living room window", "bedroom window", "home interior window"
# https://unsplash.com/s/photos/living-room-window
```

**Pexels** (Free, no attribution required)
```bash
# https://www.pexels.com/search/room%20window/
```

**Pixabay** (Free, CC0)
```bash
# https://pixabay.com/images/search/room%20with%20window/
```

### Option 2: Take Your Own Photos

**Best Practices:**
- Use smartphone camera (matches sales rep usage)
- Take from ~6-8 feet back (typical sales position)
- Capture full window in frame
- Ensure good lighting (avoid extreme backlight)
- Hold phone steady
- Take multiple angles

**Photo Checklist:**
- ✓ Window fully visible
- ✓ Window in focus
- ✓ Reasonable lighting
- ✓ Minimal motion blur
- ✓ 1-3 windows per image

### Option 3: Download Sample Set

Quick start script to download 20 test images:

```bash
#!/bin/bash
# Download sample test images

mkdir -p test_images/{single_window,multiple_windows,challenging}

# Single windows
curl -L -o test_images/single_window/living_room_1.jpg \
  "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=1024"

curl -L -o test_images/single_window/bedroom_1.jpg \
  "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=1024"

# ... add more downloads
```

## Image Requirements

### Technical Specs
- **Format:** JPEG or PNG
- **Min Resolution:** 1280x720 (720p)
- **Max Resolution:** 1920x1080 (1080p)
- **Aspect Ratio:** Any (will be auto-resized)
- **File Size:** < 5MB per image

### Content Requirements
- At least one window clearly visible
- Window should be > 10% of image area
- Reasonably well-lit scene
- Natural indoor photography (not CGI/renders)

### What to AVOID
- Outdoor photos
- Windows from outside looking in
- Extreme fisheye/distortion
- Heavily edited/filtered images
- CGI or 3D renders
- Images with existing window treatments you can't remove

## Organizing Test Images

### Naming Convention

Use descriptive names:
```
{room_type}_{window_type}_{lighting}_{number}.jpg
```

Examples:
- `living_room_bay_window_bright_01.jpg`
- `bedroom_single_window_evening_02.jpg`
- `kitchen_double_window_backlit_01.jpg`

### Batch Rename Script

```bash
# Rename all JPGs in a directory with prefix
cd test_images/single_window/
i=1
for f in *.jpg; do
  mv "$f" "single_window_$(printf %02d $i).jpg"
  ((i++))
done
```

## Running Tests

### Test Single Image
```bash
python test_pipeline.py --single test_images/single_window/living_room_01.jpg
```

### Test Entire Directory
```bash
python test_pipeline.py --input test_images --output test_results
```

### Test Specific Category
```bash
python test_pipeline.py --input test_images/challenging --output test_results/challenging
```

## Expected Test Results

See [prototype/TEST_CASES.md](../prototype/TEST_CASES.md) for detailed expected outcomes.

**Success Criteria:**
- Detection: 70%+ of windows detected with confidence > 0.5
- Segmentation: Quality score > 0.6 for clear windows
- Rendering: < 15 seconds total time per image
- Visual Quality: 6-7/10 realism rating

**Known Limitations:**
- May miss small or heavily obstructed windows
- Struggles with extreme backlight
- Non-rectangular windows may have geometry issues
- Rendered treatments may look "CG-like" (validation goal: assess if acceptable)

## Sample Test Images

We recommend starting with these 10 images for quick validation:

1. **Simple living room** - Single large window, good light
2. **Bedroom** - Double-hung window, moderate light  
3. **Office** - Two adjacent windows
4. **Kitchen** - Window with slight backlighting
5. **Living room** - Bay window (3 sections)
6. **Bedroom** - Window with furniture partially blocking
7. **Dining room** - French doors 
8. **Study** - Window in corner with plant on sill
9. **Living room** - Backlit window (bright sunshine)
10. **Bedroom** - Evening/low light scene

## Troubleshooting

### No windows detected
- Check if window is large enough in frame
- Try lowering confidence threshold (--confidence 0.3)
- Ensure window is clearly visible (not heavily obstructed)

### Poor segmentation
- Window may have heavy reflections
- Try image with clearer glass/frame boundary
- Check if window is rectangular enough

### Slow processing
- Resize large images (> 1920x1080) first
- Check GPU is being used (`nvidia-smi`)
- Close other GPU applications

## Contributing Test Images

When you find particularly good or challenging test cases:

1. Add to appropriate category folder
2. Document what makes it interesting
3. Note expected behavior
4. Include in evaluation report

## Current Test Set

Check your collection:
```bash
find test_images -name "*.jpg" -o -name "*.png" | wc -l
```

**Target:** 20-30 images for Week 1 validation
**Minimum:** 10 images covering basic scenarios
