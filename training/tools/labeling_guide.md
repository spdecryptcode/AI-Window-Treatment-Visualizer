# Labeling Guide

Instructions for team members labeling training data for YOLOv8 window detection.

---

## Overview

**Task:** Draw bounding boxes around windows in interior room photos

**Tool:** LabelImg

**Output:** YOLO format text files

**Time per image:** 20-30 seconds average

**Quality standard:** 95%+ accuracy required

---

## Setup

### Install LabelImg

```bash
# Install via pip
pip install labelImg

# Or via conda
conda install -c conda-forge labelimg

# Launch
labelImg
```

### Configure for YOLO Format

1. Open LabelImg
2. Click "File" → "Change Save Dir"
3. Select labels output directory: `training/window_detection/labels/train/`
4. Click "View" → "Auto Save Mode" (optional, saves time)
5. Set format: Click "PascalVOC" button to switch to "YOLO"

---

## Window Classes

We're detecting **4 classes** of windows:

| Class | ID | Description | Example |
|-------|----|-----------|------------|
| window | 0 | Standard window (single/double hung, casement) | Bedroom window |
| sliding_door | 1 | Sliding glass door (patio door) | Living room door |
| french_door | 2 | French doors (hinged, multiple panes) | Dining room entrance |
| skylight | 3 | Ceiling windows | Bathroom skylight |

---

## Labeling Workflow

### Step 1: Open Image

1. Click "Open" button
2. Navigate to image directory: `training/window_detection/images/train/`
3. Select first image

### Step 2: Draw Bounding Box

1. Click "Create RectBox" button (or press `W` key)
2. Click and drag to draw rectangle around window
3. Release mouse button

**Keyboard shortcut:** `W` key

### Step 3: Select Class

Dialog appears asking for class label.

1. Type class name: `window`, `sliding_door`, `french_door`, or `skylight`
2. Or select from dropdown if pre-populated
3. Click "OK"

### Step 4: Adjust Box (if needed)

- Drag corners to resize
- Drag center to move entire box
- Press `Delete` to remove box and start over

### Step 5: Save

1. Click "Save" button (or press `Ctrl+S`)
2. File auto-saves as `image_name.txt` in labels directory
3. Move to next image with "Next Image" button or `D` key

### Step 6: Repeat

Continue for all images in directory.

---

## What to Include in Bounding Box

### ✅ DO Include:

**Window Frame:**
- Include the entire window frame (trim/casing)
- Include window sill (bottom ledge)
- Include header/top frame

**Full Window:**
- All glass panes
- Mullions (dividers between panes)
- Both windows if double-hung

**Multiple Panes:**
- For bay windows: draw one box around all panels
- For separate windows close together: draw separate boxes

### ❌ DON'T Include:

**Wall:**
- Don't include excessive wall area
- Keep box tight to frame edges

**Furniture:**
- Don't include furniture in front of window
- Box should stop at furniture edge if obstructed

**Reflections:**
- Don't include outdoor scenery visible through glass
- Focus on window structure itself

---

## Visual Examples

### Example 1: Standard Bedroom Window

```
Image: bedroom_window_001.jpg

Correct box:
┌─────────────────┐
│                 │  ← Include top frame
│                 │
│  [GLASS]        │  ← Include all glass
│                 │
│  [GLASS]        │  ← Double-hung: include both panes
│                 │
└─────────────────┘  ← Include sill

Label: window (class 0)
```

**Common mistakes:**
- ❌ Box too small (only glass, missed frame)
- ❌ Box too large (includes 6" of wall)
- ❌ Only labeled top pane (should include both)

### Example 2: Bay Window

```
Image: living_room_bay.jpg

Correct box:
    ┌───────────────────────┐
   ╱│                       │╲
  ╱ │  [LEFT]  [CENTER]  [RIGHT]  │ ╲
 ╱  │                       │  ╲
└───────────────────────┘

Label: window (class 0)
One box around entire bay structure
```

**Common mistakes:**
- ❌ Three separate boxes (should be one)
- ❌ Only labeled center panel
- ❌ Box doesn't follow angle of bay

### Example 3: Sliding Glass Door

```
Image: patio_door.jpg

Correct box:
┌─────────────┐
│             │  ← Full height
│             │
│   [GLASS]   │  ← Include both panels
│   [GLASS]   │     (stationary + slider)
│             │
│             │
└─────────────┘  ← Include bottom track

Label: sliding_door (class 1)
```

**Common mistakes:**
- ❌ Only labeled sliding panel
- ❌ Confused with french_door

### Example 4: Multiple Windows

```
Image: living_room_three_windows.jpg

Correct:
┌────┐     ┌────┐     ┌────┐
│ W1 │     │ W2 │     │ W3 │
└────┘     └────┘     └────┘

Three separate boxes
Each labeled: window (class 0)
```

**Common mistakes:**
- ❌ One big box around all three
- ❌ Only labeled most prominent window

---

## Edge Cases & Guidelines

### Partially Visible Windows

**If window is >50% visible:**
✅ Label it - draw box around visible portion

**If window is <50% visible:**
❌ Skip it - don't label

**Example:** Window mostly behind furniture - skip it.

### Windows with Existing Treatments

**If window structure is visible:**
✅ Label the window frame/opening
- Include curtain rod if visible
- Box should encompass where window would be

**If completely covered:**
❌ Skip it - can't determine window boundaries

### Reflections and Glass

**Ignore outdoor scenery:**
- Only label window structure
- Glass reflecting trees/sky - doesn't matter
- Focus on frame, not view

### Blurry or Dark Windows

**If you can clearly see it's a window:**
✅ Label it

**If uncertain (maybe window, maybe door, maybe mirror):**
❌ Skip it - flag for review

### Non-Standard Cases

**Corner windows (two walls):**
- Draw one box if structurally connected
- Or two boxes if separate windows

**Arched/round windows:**
- Rectangular box is fine (doesn't need to match shape)
- Include entire arch in box

**Skylights:**
- Label if visible from room perspective
- Use `skylight` class (3)

---

## Quality Checks

### Self-Review Checklist

Before moving to next image:

- [ ] All visible windows labeled (>50% visible)
- [ ] Bounding boxes include full frame + glass
- [ ] Boxes don't include excessive wall
- [ ] Correct class selected
- [ ] No overlapping boxes (unless windows actually overlap)
- [ ] Saved successfully (check .txt file created)

### Common Errors to Avoid

1. **Box too small** - Most common error
   - Should include frame, not just glass
   
2. **Wrong class** - Second most common
   - Double-check: window vs sliding_door vs french_door
   - When in doubt: use `window` (most general)

3. **Skipped windows** - Easy to miss
   - Check corners, backgrounds
   - Multiple windows in same room

4. **Duplicate boxes** - Rare but happens
   - Check before saving
   - Delete duplicates

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `W` | Create new bounding box |
| `D` | Next image |
| `A` | Previous image |
| `Del` | Delete selected box |
| `Ctrl+S` | Save |
| `Ctrl+U` | Load next unlabeled image |
| `Space` | Flag image as verified |

**Tip:** Use keyboard shortcuts to speed up labeling. Can label 100+ images per hour with practice.

---

## Workflow Tips

### Batch Labeling Strategy

**For maximum efficiency:**

1. **First pass (10 min):** Label only obvious, clear windows
2. **Second pass (5 min):** Handle edge cases and difficult images
3. **Review pass (3 min):** Spot-check 10% of your work

**Result:** ~150 images per hour once proficient

### Focus Modes

**Speed mode (easy images):**
- Auto-save enabled
- Keyboard shortcuts only
- Don't overthink edge cases

**Accuracy mode (difficult images):**
- Double-check each box
- Manual save to review before proceeding
- Flag uncertain cases

### Stamina Tips

- Label in 30-minute sessions
- Take 5-minute breaks
- Switch between easy and hard batches
- Don't label when tired (accuracy drops)

---

## Flagging for Review

If you encounter images you're unsure about:

### Mark for Team Review

1. Click "Verify Image" checkbox (or press `Space`)
2. Add note in filename or separate log:
   ```
   bedroom_017.jpg - uncertain if bay window or three separate
   kitchen_042.jpg - window heavily obstructed, skipped
   ```

3. Lead reviewer will examine flagged images

### Common Flag Reasons

- Uncertainty about class (window vs door)
- Unusual window configuration
- Very poor image quality
- Privacy concerns (visible personal info)
- Potential copyright issue

---

## Output Format

### Generated Label File

For image `bedroom_001.jpg`, creates `bedroom_001.txt`:

```
0 0.512 0.35 0.28 0.45
```

**Format:** `class_id x_center y_center width height`

All values normalized (0.0 to 1.0):
- `class_id` - 0=window, 1=sliding_door, 2=french_door, 3=skylight
- `x_center` - Horizontal center position (0=left, 1=right)
- `y_center` - Vertical center position (0=top, 1=bottom)
- `width` - Box width as fraction of image width
- `height` - Box height as fraction of image height

**Multiple windows:**

```
0 0.25 0.35 0.18 0.40
0 0.50 0.35 0.18 0.40
0 0.75 0.35 0.18 0.40
```

Three windows at different horizontal positions.

### Validation

Run validation script after labeling batch:

```bash
python training/scripts/validate_labels.py \
  --images training/window_detection/images/train/ \
  --labels training/window_detection/labels/train/
```

Checks:
- All images have corresponding labels
- Label format correct
- Bounding boxes within image bounds (0-1)
- Class IDs valid (0-3)

---

## Progress Tracking

### Daily Log Template

```
Date: 2026-02-16
Labeler: [Your Name]
Session: 1

Images labeled: 150
Time spent: 1.5 hours
Avg time per image: 36 seconds

Flagged for review: 3 images
- bedroom_017.jpg - unusual bay window
- kitchen_042.jpg - very dark
- living_089.jpg - window or mirror?

Notes:
- Sliding doors were challenging today
- Getting faster with keyboard shortcuts
```

### Team Progress

Track on shared spreadsheet:

| Date | Labeler | Images | Time | Flags | Total Complete |
|------|---------|--------|------|-------|----------------|
| 2/16 | Alice   | 150    | 1.5h | 3     | 150            |
| 2/16 | Bob     | 175    | 2.0h | 5     | 325            |
| 2/17 | Alice   | 180    | 1.5h | 2     | 505            |

**Target:** 800 images total

---

## Quality Assurance

### Peer Review System

**Every 100 images:**
1. Swap with partner
2. Review each other's labels
3. Check 20 random samples
4. Flag issues/corrections

**If >5% errors found:**
- Re-train labeler
- Re-do batch

### Lead Review

Lead reviewer spot-checks:
- 10% of all labeled data
- 100% of flagged images
- Final approval before training

---

## FAQs

**Q: What if window is partially behind furniture?**
A: If >50% visible, label the visible portion. If <50%, skip.

**Q: Bay window - one box or multiple?**
A: One box around the entire bay structure.

**Q: Window with open curtains - include curtains?**
A: No, box should include window frame only, not curtains.

**Q: Very small window in background (like 30 pixels)?**
A: Label it if you can clearly see it's a window.

**Q: Multiple windows very close together (like 1" apart)?**
A: Separate boxes unless structurally connected (like bay window).

**Q: Glass door that's mostly glass - window or door?**
A: If it's a door (even if glass): use `sliding_door` or `french_door`.

**Q: Skylight visible in ceiling - label it?**
A: Yes, use class `skylight` (3).

**Q: Made a mistake - how to fix?**
A: Open image again, delete box (Del key), redraw, save.

**Q: Label file not created - what's wrong?**
A: Check save directory is set correctly and you clicked Save.

---

## Getting Help

**Questions during labeling:**
- Ask lead reviewer
- Check this guide
- Review example images

**Technical issues with LabelImg:**
- Restart application
- Check installation
- Contact dev team

**Uncertain about specific image:**
- Flag for review (press Space)
- Move to next image
- Don't guess

---

## Recognition & Gamification

**Top Labeler Leaderboard:**
- Most images labeled
- Highest accuracy (lowest error rate in reviews)
- Fastest average time

**Milestones:**
- 100 images: Apprentice Labeler
- 300 images: Expert Labeler  
- 500 images: Master Labeler

**Small rewards for quality work!**

---

**Good luck and thank you for contributing to the training data!**

---

**Guide Version:** 1.0  
**Last Updated:** February 16, 2026  
**Questions:** Contact lead reviewer
