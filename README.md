# AI Window Treatment Visualizer

[![GitHub](https://img.shields.io/badge/GitHub-spdecryptcode%2FAI--Window--Treatment--Visualizer-blue?logo=github)](https://github.com/spdecryptcode/AI-Window-Treatment-Visualizer)

A fully offline, laptop-based multi-stage vision pipeline that detects windows in room photos and renders photorealistic window treatments using vendor swatches. Sales reps upload room images, select treatments and fabrics, then receive photorealistic before/after comparisons—all processed locally on RTX 3060+ GPU hardware with no cloud dependencies.

## Project Status

**Current Phase:** Prototype & Validation (Week 1)

This project follows a validation-first approach. We're building a Gradio prototype to test AI model viability with real sales photos before committing to full production architecture.

## Architecture Overview

### Multi-Stage Vision Pipeline

```
Room Image Upload
        ↓
Window Detection (YOLOv8)
        ↓
Glass/Frame Segmentation (FastSAM)
        ↓
Depth + Geometry Estimation (MiDaS)
        ↓
Treatment Placement Engine
        ↓
Material Swatch Mapping
        ↓
Classical Rendering OR SDXL Inpainting
        ↓
Photorealistic Rendering
        ↓
Before/After Comparison
```

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/spdecryptcode/AI-Window-Treatment-Visualizer.git
cd AI-Window-Treatment-Visualizer
```

### One-Command Setup

```bash
# Automated setup (installs everything)
chmod +x setup.sh
./setup.sh
```

This will:
- Install Python dependencies
- Download AI models (~300MB)
- Create directory structure
- Download sample swatches
- Verify installation

### Manual Setup

```bash
# 1. Create Python environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r prototype/requirements.txt

# 3. Download AI models (one-time, ~15 min)
python prototype/download_models.py

# 4. Download sample swatches (optional)
cd swatches && chmod +x download_samples.sh && ./download_samples.sh && cd ..

# 5. Run Gradio interface
cd prototype && python app.py
```

Access at: `http://localhost:7860`

**📖 See [QUICKSTART.md](QUICKSTART.md) for detailed guide.**

### Hardware Requirements

**Minimum:**
- NVIDIA RTX 3060 (12GB VRAM)
- 16GB RAM
- 50GB storage

**Recommended:**
- NVIDIA RTX 4060 (16GB VRAM)
- 32GB RAM
- 100GB storage

## Project Structure

```
window_treatment/
├── prototype/              # Week 1: Validation prototype
│   ├── app.py             # Gradio interface
│   ├── pipeline.py        # AI pipeline implementation
│   ├── classical_renderer.py  # Non-AI rendering fallback
│   ├── requirements.txt
│   ├── models/            # Downloaded AI models
│   ├── swatches/          # Sample fabric textures
│   └── test_images/       # Test room photos
│
├── frontend/              # Production React/Next.js app (Phase 1)
├── backend/               # Production FastAPI server (Phase 1)
├── training/              # Fine-tuning pipelines (Phase 2, if needed)
├── docker/                # Docker deployment configs
├── docs/                  # Comprehensive documentation
└── materials/             # Production swatch library
```

## Technology Stack

### Prototype
- **Interface:** Gradio
- **AI Models:** YOLOv8n, FastSAM-s, MiDaS v2.1 Small, SDXL-Inpainting
- **Rendering:** Classical (OpenCV/Pillow) + SDXL comparative testing

### Production (Pending validation)
- **Frontend:** React + Next.js 14 + Tailwind CSS + Konva.js
- **Backend:** FastAPI + PyTorch + OpenCV
- **Database:** SQLite (swatch catalog)
- **Deployment:** Docker + NVIDIA Container Runtime

## Development Phases

### ✅ Phase 0: Validation Prototype (Week 1)
Build Gradio app to test pre-trained model quality with real sales photos.

**Deliverables:**
- Working Gradio prototype
- Test results on 20-30 room images
- Sales rep feedback from 5-10 users
- Decision: Classical rendering OR fine-tuned SDXL OR pivot

### 🔄 Phase 1: Production System (Week 2-7)
**Triggered if:** Classical rendering quality is acceptable (6-7/10)

Build production React+FastAPI system with classical graphics rendering.

### 🔄 Phase 2: Fine-Tuning (Week 2-13)
**Triggered if:** Need higher quality than classical rendering provides

Collect training data and fine-tune YOLOv8 + SDXL LoRA for window treatment-specific rendering.

## Decision Gate (End Week 1)

After prototype validation, choose path:

| Metric | Path A: Classical | Path B: Fine-Tune | Path C: Pivot |
|--------|------------------|-------------------|---------------|
| Quality Rating | 6-7/10 acceptable | <6/10 but high interest | Any quality |
| Sales Rep Interest | 70%+ say "Yes" | 70%+ say "Would be great if better" | <50% interest |
| Timeline | 6 weeks to production | 12 weeks to production | Cancel/rethink |
| Cost | Dev time only | +$3k training data | $0 |

## Key Features

- **Fully Offline:** No cloud APIs, no data upload, complete privacy
- **Fast Processing:** 6-15 seconds per rendering (depending on path)
- **Manual Fallbacks:** If AI detection fails, manual tools available
- **Multiple Treatments:** Curtains, drapes, blinds, roller shades, Roman shades
- **Vendor Swatches:** Support for 50-100+ fabric materials
- **Before/After:** Interactive slider comparison
- **Export:** High-res PNG + consultation PDF

## Documentation

- [Prototype README](prototype/README.md) - Setup and run Gradio prototype
- [Test Cases](prototype/TEST_CASES.md) - Expected results for validation
- [Evaluation Form](prototype/evaluation_form.md) - Sales rep feedback template
- [Results Template](prototype/RESULTS.md) - Document validation findings
- [Installation Guide](docs/INSTALLATION.md) - Production deployment
- [User Guide](docs/USER_GUIDE.md) - Sales rep workflow
- [API Reference](docs/API_REFERENCE.md) - Backend API endpoints
- [Swatch Management](docs/SWATCH_MANAGEMENT.md) - Add vendor materials

## Contributing

This is an internal sales tool project. Development team only.

To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

Proprietary - National Franchise Internal Use Only

## Support

For technical issues during prototype phase, contact development team.

---

**Repository:** [github.com/spdecryptcode/AI-Window-Treatment-Visualizer](https://github.com/spdecryptcode/AI-Window-Treatment-Visualizer)  
**Last Updated:** March 10, 2026  
**Current Phase:** Prototype & Validation  
**Next Milestone:** Decision Gate (End Week 1)
