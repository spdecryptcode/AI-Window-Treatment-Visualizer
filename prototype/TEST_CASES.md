# Prototype Test Cases

Document expected results for validation testing. Use this to track detection accuracy and rendering quality across diverse room types.

## Test Image Categories

### Category 1: Standard Bedroom Windows (5 images)

**Purpose:** Baseline performance test - most common sales scenario

**Test Images:**
1. `bedroom_standard_single.jpg` - Single hung window, centered wall
2. `bedroom_standard_double.jpg` - Two adjacent windows
3. `bedroom_corner.jpg` - Window in room corner
4. `bedroom_large.jpg` - Large picture window
5. `bedroom_furniture.jpg` - Window partially obstructed by bed/dresser

**Expected Results:**

| Image | Detection Expected | Segmentation Quality | Notes |
|-------|-------------------|---------------------|-------|
| single | ✅ High confidence | Clean mask expected | Ideal case |
| double | ✅ Both windows | Two separate masks | Test multi-window |
| corner | ⚠️ May miss | May include wall | Depth estimation critical |
| large | ✅ Should detect | Clean mask | Good for curtains |
| furniture | ⚠️ Partial detection | May include furniture | Manual adjustment likely |

**Success Criteria:** 4/5 detected with minimal manual adjustment

---

### Category 2: Living Room Bay/Large Windows (5 images)

**Purpose:** Test complex geometries and larger surfaces

**Test Images:**
1. `living_bay_window.jpg` - Classic 3-panel bay window
2. `living_floor_ceiling.jpg` - Floor-to-ceiling window
3. `living_multiple.jpg` - 3+ separate windows in frame
4. `living_angled.jpg` - Angled room perspective
5. `living_bright.jpg` - Very bright, high exposure

**Expected Results:**

| Image | Detection Expected | Segmentation Quality | Notes |
|-------|-------------------|---------------------|-------|
| bay | ⚠️ May detect as 3 separate | Complex mask | Geometry engine crucial |
| floor_ceiling | ✅ Should detect | Clean mask | Scale test |
| multiple | ⚠️ May miss 1-2 | Separate masks | Multi-select UI test |
| angled | ⚠️ Lower confidence | Perspective distortion | Depth estimation test |
| bright | ✅ Should detect | May overexpose glass | Color matching test |

**Success Criteria:** 3/5 usable with manual refinement

---

### Category 3: Sliding Glass Doors (5 images)

**Purpose:** Test door vs window classification

**Test Images:**
1. `sliding_patio.jpg` - Standard patio door
2. `sliding_double.jpg` - Double sliding doors
3. `sliding_open.jpg` - Door partially open
4. `sliding_reflection.jpg` - Heavy outdoor reflection
5. `sliding_vertical.jpg` - Vertical blinds already present

**Expected Results:**

| Image | Detection Expected | Segmentation Quality | Notes |
|-------|-------------------|---------------------|-------|
| patio | ⚠️ May label as "door" | Glass mask expected | Class relabeling may be needed |
| double | ⚠️ May miss one panel | Two regions | Wide aspect ratio |
| open | ❌ Likely to fail | Confusing geometry | Manual draw expected |
| reflection | ⚠️ May detect outdoor objects | Noisy mask | Segmentation challenge |
| vertical | ⚠️ YOLO may miss window behind | Existing treatment confusion | Preprocessing needed |

**Success Criteria:** 2/5 auto-detected, all usable with manual tools

---

### Category 4: Kitchen/Bathroom Small Windows (5 images)

**Purpose:** Test small object detection and varying lighting

**Test Images:**
1. `kitchen_over_sink.jpg` - Small window above sink
2. `kitchen_multiple_small.jpg` - Two small windows
3. `bathroom_frosted.jpg` - Frosted/privacy glass
4. `bathroom_shower.jpg` - Window in shower area
5. `kitchen_backsplash.jpg` - Window near tile backsplash

**Expected Results:**

| Image | Detection Expected | Segmentation Quality | Notes |
|-------|-------------------|---------------------|-------|
| over_sink | ⚠️ May miss (small) | Clean if detected | Size lower threshold test |
| multiple_small | ❌ Likely to miss 1-2 | Small masks | Confidence threshold test |
| frosted | ⚠️ Lower confidence | Texture affects segmentation | Material challenge |
| shower | ⚠️ May miss | Tile background noise | Busy background test |
| backsplash | ⚠️ May confuse tile pattern | Noisy mask possible | Edge detection test |

**Success Criteria:** 2/5 auto-detected acceptable, manual tools work for rest

---

### Category 5: Office/Commercial Spaces (5 images)

**Purpose:** Test large glass walls and commercial settings

**Test Images:**
1. `office_wall_glass.jpg` - Entire glass wall
2. `office_cubicle.jpg` - Window in cubicle
3. `office_conference.jpg` - Conference room windows
4. `office_corner_floor.jpg` - Floor-to-ceiling corner windows
5. `office_exterior.jpg` - View of building exterior windows

**Expected Results:**

| Image | Detection Expected | Segmentation Quality | Notes |
|-------|-------------------|---------------------|-------|
| wall_glass | ⚠️ May detect as multiple | Complex large region | Scaling test |
| cubicle | ⚠️ Obstructions likely | Partial mask | Office furniture challenge |
| conference | ✅ Should detect | Clean mask | Professional setting |
| corner_floor | ⚠️ Perspective distortion | Two-plane mask | Geometry challenge |
| exterior | ❌ Wrong perspective | N/A | Should fail gracefully |

**Success Criteria:** 2/5 usable (exterior expected to fail)

---

### Category 6: Challenging Edge Cases (5 images)

**Purpose:** Stress test and identify failure modes

**Test Images:**
1. `dark_room.jpg` - Very low lighting
2. `backlit_window.jpg` - Window blown out (extreme backlight)
3. `curtains_existing.jpg` - Window with curtains already installed
4. `dirty_glass.jpg` - Dirty/smudged glass
5. `night_reflected.jpg` - Nighttime with interior reflection

**Expected Results:**

| Image | Detection Expected | Segmentation Quality | Notes |
|-------|-------------------|---------------------|-------|
| dark_room | ❌ May miss | Poor mask | Brightness normalization test |
| backlit | ⚠️ May detect frame only | Clipped highlights | HDR needed |
| curtains_existing | ⚠️ Detects curtain not window | Confusing mask | Context understanding test |
| dirty_glass | ⚠️ Lower confidence | Texture noise | Preprocessing filter test |
| night_reflected | ❌ Likely confusion | Mirror-like artifacts | Lighting condition limit |

**Success Criteria:** 1/5 auto-detected acceptable - identify clear failure modes

---

## Rendering Quality Rubric

Rate each rendered output 1-10:

### Classical Rendering (Graphics-Based)

**What to evaluate:**
- Perspective match (10 pts)
- Shadow realism (10 pts)
- Color matching to room (10 pts)
- Texture quality (10 pts)
- Edge blending (10 pts)

**Scoring:**
- 9-10: Customer-ready, looks convincing
- 7-8: Sales-ready with minor flaws
- 5-6: Useful for concept, obviously rendered
- 3-4: Poor quality, would need fixes
- 1-2: Unusable

### SDXL Rendering (AI-Generated)

**What to evaluate:**
- Photorealism (10 pts)
- Fabric texture fidelity (10 pts)
- Lighting coherence (10 pts)
- Physics (draping, folds) (10 pts)
- Hallucinations/artifacts (10 pts - deduct for weird AI mistakes)

**Scoring:**
- 9-10: Photorealistic, indistinguishable from real photo
- 7-8: Very good, minor AI tells
- 5-6: Acceptable, noticeable AI generation
- 3-4: Blurry, obvious fake
- 1-2: Broken, artifacts, unusable

---

## Performance Tracking

For each test image, record:

```markdown
### Test Image: [filename]

**Detection:**
- Window detected: Yes / No / Partial
- Confidence score: ___
- Manual adjustment needed: Yes / No
- Time: ___ seconds

**Segmentation:**
- Mask quality (1-10): ___
- Manual refinement needed: Yes / No
- Time: ___ seconds

**Depth Estimation:**
- Depth map reasonable: Yes / No
- Time: ___ seconds

**Classical Rendering:**
- Quality score (1-10): ___
- Time: ___ seconds
- Notes: ___

**SDXL Rendering:**
- Quality score (1-10): ___
- Time: ___ seconds
- Notes: ___

**Overall:**
- Preferred mode: Classical / SDXL
- Would show to customer: Yes / No
- Issues encountered: ___
```

---

## Aggregate Metrics (End of Testing)

After processing all 30 test images:

**Detection Accuracy:**
- Fully automatic successful: ___/30 (___%)
- Usable with manual adjustment: ___/30 (___%)
- Complete failure: ___/30 (___%)

**Average Quality Scores:**
- Classical rendering average: ___ / 10
- SDXL rendering average: ___ / 10

**Average Processing Time:**
- Classical mode: ___ seconds
- SDXL mode: ___ seconds

**VRAM Usage:**
- Peak during Classical: ___ GB
- Peak during SDXL: ___ GB
- Any OOM errors: Yes / No

**Usability:**
- Customer-ready images: ___/30 (___%)
- Sales-ready images: ___/30 (___%)
- Concept-only quality: ___/30 (___%)
- Unusable: ___/30 (___%)

---

## Decision Criteria

Based on test results, recommend:

### Proceed with Classical Rendering (Phase 1)
✅ If:
- Classical average quality ≥ 6.5/10
- Customer-ready rate ≥ 50%
- Processing time < 10 seconds
- Sales rep feedback positive

### Proceed with SDXL Fine-Tuning (Phase 2)
✅ If:
- Classical quality < 6.5/10 BUT
- High sales rep interest (70%+)
- Budget available (~$3k)
- Can commit 10-12 weeks

### Pivot or Cancel
❌ If:
- Both modes < 5/10 quality
- Low sales rep interest (<50%)
- Fundamental technical blockers discovered
- Detection success rate < 40%

---

## Notes Section

Document any insights, patterns, or surprises:

**What worked better than expected:**
- 

**What worked worse than expected:**
- 

**Unexpected failure modes:**
- 

**Feature requests from testers:**
- 

**Technical limitations discovered:**
- 

**Recommendations for production:**
- 

---

**Last Updated:** February 16, 2026  
**Tester Name:** ___________________  
**Date Range:** ___________ to ___________
