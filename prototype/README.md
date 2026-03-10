# Window Treatment Visualizer - Prototype

Week 1 validation prototype using Gradio and pre-trained AI models.

## Purpose

Test whether pre-trained AI models can produce acceptable quality window treatment visualizations before committing to full production architecture.

## Goals

1. **Validate Detection Accuracy:** Can YOLOv8 detect windows in interior room photos?
2. **Test Segmentation Quality:** Does FastSAM produce clean window masks?
3. **Compare Rendering Modes:** Classical graphics vs SDXL inpainting quality
4. **Measure Performance:** Can we hit 10-15 second processing target?
5. **Gather User Feedback:** Will sales reps actually use this tool?

## Installation

### Prerequisites

- NVIDIA GPU with 12GB+ VRAM (RTX 3060 or better)
- CUDA 12.1+ drivers installed
- Python 3.10 or 3.11
- 50GB free disk space (for models)

### Setup Steps

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download AI models (one-time, ~10-15 minutes)
python download_models.py

# This will download:
# - YOLOv8n (~6MB)
# - FastSAM-s (~145MB)
# - MiDaS v2.1 Small (~80MB)
# - SDXL Inpainting (~6.9GB)
# Total: ~7.2GB
```

### Verify Installation

```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Check models downloaded
python -c "import os; print('Models:', os.listdir('models/'))"

# Expected output:
# Models: ['yolov8', 'fastsam', 'midas', 'sdxl']
```

## Usage

### 1. Start Gradio Interface

```bash
python app.py
```

This will start a local web server at `http://localhost:7860`

### 2. Basic Workflow

**Tab 1: Upload**
- Drag and drop a room photo or click to browse
- Supported formats: JPG, PNG
- Max size: 10MB
- Image will auto-resize to max 1024px

**Tab 2: Select Window**
- View detected windows with bounding boxes
- Green boxes = high confidence (>0.7)
- Yellow boxes = medium confidence (0.5-0.7)
- If detection fails, use "Manual Draw" tool to draw rectangle

**Tab 3: Choose Treatment**
- Select treatment type: Curtains, Blinds, Roller Shade, Roman Shade
- Browse swatch gallery (organized by treatment type)
- Click swatch to select

**Tab 4: Render**
- Choose rendering mode:
  - **Classical:** Fast (3-5s), predictable, uses computer graphics
  - **SDXL:** Slower (8-12s), AI-generated, may be more realistic
- Click "Generate Preview"
- Watch progress bar (WebSocket streaming)

**Tab 5: Compare**
- Use slider to compare before/after
- Toggle between side-by-side and slider modes
- Download PNG for consultation

### 3. Testing Protocol

For validation, test each image with:

1. **Automatic detection** - Did YOLOv8 find the window?
2. **Segmentation quality** - Is the mask clean?
3. **Both render modes** - Which looks better?
4. **Timing** - How long did each step take?
5. **Overall quality** - Rate 1-10 for photorealism

Document results in [RESULTS.md](RESULTS.md)

## Test Images

Place test room photos in `test_images/` directory.

**Good test image characteristics:**
- Well-lit room (natural or artificial light)
- Window clearly visible
- Minimal obstructions (furniture blocking view)
- Variety of window types:
  - Standard single/double hung
  - Bay windows
  - Sliding glass doors
  - Small bathroom/kitchen windows
  - Floor-to-ceiling windows

**Challenging cases to include:**
- windows with existing treatments (blinds/curtains)
- Reflective glass showing outdoor scene
- Odd angles or perspective
- Dark rooms
- Windows in corners

## Sample Swatches

Located in `swatches/` directory, organized by treatment type:

```
swatches/
├── curtains/
│   ├── linen_white.jpg
│   ├── linen_beige.jpg
│   ├── cotton_gray.jpg
│   └── ...
├── blinds/
│   ├── wood_oak.jpg
│   ├── wood_walnut.jpg
│   └── ...
└── shades/
    ├── cellular_white.jpg
    ├── roman_fabric_tan.jpg
    └── ...
```

Currently includes ~30 Creative Commons licensed fabric textures. For production, replace with actual vendor materials.

## Performance Benchmarks

Target performance on RTX 3060:

| Step | Target Time | VRAM Usage |
|------|-------------|------------|
| Window Detection | <2s | ~1GB |
| Segmentation | <2s | ~2.5GB |
| Depth Estimation | <1s | ~1.5GB |
| Classical Rendering | <2s | <1GB |
| SDXL Rendering | <10s | ~8GB |
| **Total (Classical)** | **~7s** | **Peak: 2.5GB** |
| **Total (SDXL)** | **~15s** | **Peak: 8GB** |

Models are loaded/unloaded sequentially to manage VRAM.

## Troubleshooting

### CUDA Out of Memory

```
RuntimeError: CUDA out of memory
```

**Solutions:**
- Close other GPU applications
- Use Classical rendering only (lower VRAM)
- Reduce image size in `app.py` (line 23: `MAX_SIZE = 1024` → `768`)
- Restart Python to clear VRAM

### Models Not Found

```
FileNotFoundError: Model checkpoint not found
```

**Solution:**
```bash
# Re-run model downloader
python download_models.py

# Verify downloads
ls -lh models/*/
```

### Slow Performance

If processing takes >30 seconds:

- Check GPU utilization: `nvidia-smi`
- Ensure CUDA version matches PyTorch
- Verify models loaded on GPU not CPU (check console logs)

### Poor Detection Quality

If windows not detected:

- Use "Manual Draw" tool in Tab 2
- Try different photo angles
- Ensure window is not heavily obstructed
- Check lighting (very dark rooms may fail)

### Gradio Won't Start

```
Address already in use: 7860
```

**Solution:**
```bash
# Kill existing process
lsof -ti:7860 | xargs kill -9

# Or change port in app.py
# demo.launch(server_port=7861)
```

## Validation Checklist

After testing with 20-30 images, answer:

- [ ] Window detection accuracy: ___/30 detected correctly
- [ ] Average segmentation quality (1-10): ___
- [ ] Classical rendering quality (1-10): ___
- [ ] SDXL rendering quality (1-10): ___
- [ ] Average processing time (Classical): ___ seconds
- [ ] Average processing time (SDXL): ___ seconds
- [ ] VRAM peak usage: ___ GB
- [ ] Any crashes or errors: Yes / No
- [ ] Manual corrections needed: ___% of images

## Sales Rep Feedback

Have 5-10 sales reps test the prototype. Use [evaluation_form.md](evaluation_form.md) to collect feedback.

**Key questions:**
1. Would this help you close more deals?
2. Is the quality acceptable for customer presentations?
3. Which rendering mode do you prefer?
4. What improvements are critical?

## Next Steps

Based on validation results:

**If Classical quality is acceptable (6-7/10) + 70% sales rep interest:**
→ Proceed to Phase 1: Production Build (Classical Rendering)

**If quality too low (<6/10) but high interest:**
→ Proceed to Phase 2: Collect training data + fine-tune SDXL

**If <50% sales rep interest or fundamental issues:**
→ Pivot or cancel project

Document decision in [RESULTS.md](RESULTS.md)

## File Structure

```
prototype/
├── app.py                      # Main Gradio interface
├── pipeline.py                 # AI pipeline functions
├── classical_renderer.py       # Graphics-based rendering
├── download_models.py          # Model download script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── TEST_CASES.md              # Expected test results
├── evaluation_form.md          # Sales rep feedback form
├── RESULTS.md                  # Validation findings template
├── models/                     # Downloaded AI models
│   ├── yolov8/
│   ├── fastsam/
│   ├── midas/
│   └── sdxl/
├── swatches/                   # Sample fabric textures
│   ├── curtains/
│   ├── blinds/
│   └── shades/
└── test_images/                # Room photos for testing
    ├── bedroom_standard.jpg
    ├── living_room_bay.jpg
    └── ...
```

## Development Notes

- Models load sequentially to manage VRAM
- Warmup inference runs on startup (dummy data)
- Progress updates via Gradio streaming
- Caching not implemented in prototype (add in production)
- Error handling is minimal (improve in production)

## Support

For questions during prototype phase, contact development team.

---

**Last Updated:** February 16, 2026  
**Phase:** Validation Prototype  
**Target Completion:** End of Week 1
