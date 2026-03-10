# Quick Start Guide

Get the prototype running in under 10 minutes!

## Prerequisites

- **Python 3.8+** installed
- **NVIDIA GPU** with 12GB+ VRAM (RTX 3060 or better)
  - Or CPU mode (slower, ~30-60s per image)
- **50GB free disk space** (for models)
- **16GB RAM** minimum

## Installation (5 minutes)

### Step 1: Clone/Extract Project
```bash
cd window_treatment
```

### Step 2: Create Python Environment
```bash
# Using venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n window_viz python=3.10
conda activate window_viz
```

### Step 3: Run Setup
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- ✓ Install all Python packages
- ✓ Download AI models (~300MB)
- ✓ Create directory structure
- ✓ Download sample swatches
- ✓ Verify installation

**Note:** Setup may take 5-10 minutes on first run.

## Usage

### Option 1: Gradio Web Interface (Recommended)

```bash
cd prototype
python app.py
```

Then open in browser: http://localhost:7860

**Workflow:**
1. Upload a room photo
2. Click "Detect Windows"
3. Select window (if multiple detected)
4. Click "Segment Window"
5. Choose treatment type & swatch
6. Click "Render Preview"
7. Compare before/after

### Option 2: Batch Testing

Test multiple images at once:

```bash
# Test all images in directory
python prototype/test_pipeline.py --input test_images --output test_results

# Test single image
python prototype/test_pipeline.py --single test_images/living_room.jpg

# Limit to 10 images
python prototype/test_pipeline.py --input test_images --max-images 10
```

Results saved to `test_results/`:
- Detection visualizations
- Segmentation overlays
- Final rendered images
- Before/after comparisons
- JSON report with metrics

### Option 3: Python API

```python
from pipeline import WindowDetector, WindowSegmenter, DepthEstimator, calculate_treatment_geometry
from classical_renderer import ClassicalRenderer, load_swatch
import cv2

# Initialize
detector = WindowDetector()
segmenter = WindowSegmenter()
depth_est = DepthEstimator()
renderer = ClassicalRenderer()

# Load image
image = cv2.imread('room_photo.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect windows
detections = detector.detect(image)
bbox = detections[0]['bbox']

# Segment
seg_result = segmenter.segment(image, bbox)

# Depth
depth_result = depth_est.estimate(image, bbox)

# Geometry
geometry = calculate_treatment_geometry(
    seg_result['combined_mask'],
    depth_result['depth_map'],
    treatment_type='curtains'
)

# Render
swatch = load_swatch('swatches/curtains/linen_beige.jpg')
result = renderer.render(
    image,
    seg_result['combined_mask'],
    swatch,
    geometry,
    depth_result['depth_map'],
    treatment_type='curtains'
)

# Save
cv2.imwrite('output.jpg', cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
```

## Adding Your Own Content

### Add Test Images

```bash
# 1. Copy images to test_images/
cp ~/Pictures/room_photos/*.jpg test_images/

# 2. Run tests
python prototype/test_pipeline.py --input test_images
```

See [test_images/README.md](test_images/README.md) for image requirements.

### Add Fabric Swatches

```bash
# 1. Place swatches in appropriate category
cp vendor_fabric.jpg swatches/curtains/linen_beige.jpg

# 2. Verify
ls swatches/curtains/
```

See [swatches/README.md](swatches/README.md) for swatch requirements.

## Validation Workflow (Week 1)

Following the validation-first approach:

### Day 1-2: Setup & Initial Testing
```bash
# 1. Run setup
./setup.sh

# 2. Test with 5 sample images
python prototype/test_pipeline.py --input test_images --max-images 5

# 3. Check results
open test_results/test_report.json
```

### Day 3-4: Comprehensive Testing
```bash
# Test 20-30 images per TEST_CASES.md
python prototype/test_pipeline.py --input test_images
```

### Day 5: Sales Rep Testing
- Have 5-10 sales reps use Gradio UI
- Collect feedback via `prototype/evaluation_form.md`
- Document issues encountered

### Day 6-7: Analysis & Decision
- Review `test_results/test_report.json`
- Compile feedback in `prototype/RESULTS.md`
- **Decision Gate:** Choose path:
  - ✓ Classical rendering acceptable → Phase 1 production
  - ✗ Quality insufficient → SDXL fine-tuning (Phase 2)
  - ✗ Detection poor → YOLO fine-tuning required

## Performance Expectations

### Classical Rendering Mode (Default)
- **Total time:** 6-10 seconds per image
  - Detection: ~2s
  - Segmentation: ~2s  
  - Depth: ~1s
  - Rendering: ~3-5s
- **GPU VRAM:** ~4-5GB
- **Quality:** 6-7/10 (realistic but some "CG" look)

### With SDXL (Optional)
- **Total time:** 15-20 seconds
- **GPU VRAM:** ~10-12GB
- **Quality:** 7-8/10 (more photorealistic)

## Troubleshooting

### "CUDA out of memory"
```bash
# Use CPU mode
export CUDA_VISIBLE_DEVICES=""
python prototype/app.py
```

### "Models not found"
```bash
# Re-download models
python prototype/download_models.py
```

### "No windows detected"
- Lower confidence threshold in UI (try 0.3 instead of 0.5)
- Ensure window is clearly visible in image
- Try different test image

### Slow performance
```bash
# Check GPU is being used
nvidia-smi

# If no GPU showing, check CUDA install:
python -c "import torch; print(torch.cuda.is_available())"
```

### Installation issues
```bash
# Reinstall dependencies
pip install --upgrade --force-reinstall -r prototype/requirements.txt

# Or use conda
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

## Next Steps

After successful validation:

1. **Production Build** (if validated)
   - See `docs/INSTALLATION.md`
   - Build React frontend
   - Deploy FastAPI backend
   - Containerize with Docker

2. **Fine-tuning** (if needed)
   - See `training/data_collection/strategy.md`
   - Collect training data
   - Label with `training/tools/labeling_guide.md`
   - Fine-tune models

3. **Vendor Integration**
   - Import swatch catalog
   - Set up material database
   - See `docs/SWATCH_MANAGEMENT.md`

## Documentation

- **Prototype:**
  - [prototype/README.md](prototype/README.md) - Full prototype guide
  - [prototype/TEST_CASES.md](prototype/TEST_CASES.md) - Test scenarios
  - [prototype/evaluation_form.md](prototype/evaluation_form.md) - Feedback collection
  - [prototype/RESULTS.md](prototype/RESULTS.md) - Results template

- **Production:**
  - [docs/INSTALLATION.md](docs/INSTALLATION.md) - Production deployment
  - [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - End-user guide
  - [docs/SWATCH_MANAGEMENT.md](docs/SWATCH_MANAGEMENT.md) - Material management
  - [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API docs

- **Training:**
  - [training/data_collection/strategy.md](training/data_collection/strategy.md) - Data collection
  - [training/tools/labeling_guide.md](training/tools/labeling_guide.md) - Labeling guide

## Support

For issues or questions:
1. Check documentation in `docs/` and `prototype/`
2. Review troubleshooting sections
3. Check model installation: `python prototype/download_models.py --verify`

## License

[Your License Here]

---

**Ready to start?** Run `./setup.sh` and you'll be visualizing window treatments in minutes! 🚀
