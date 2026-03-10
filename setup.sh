#!/bin/bash

# Quick setup script for Window Treatment Visualizer prototype
# Run this after installing Python environment

set -e  # Exit on error

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Window Treatment Visualizer - Prototype Setup           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "🐍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "   ✓ Found Python $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip"
    exit 1
fi
echo "   ✓ Found pip"

# Check GPU (optional but recommended)
echo ""
echo "🎮 Checking GPU availability..."
if command -v nvidia-smi &> /dev/null; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
    GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader | head -1)
    echo "   ✓ Found GPU: $GPU_NAME ($GPU_MEM)"
else
    echo "   ⚠️  No NVIDIA GPU detected (will use CPU - slower)"
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
echo "   This may take 5-10 minutes on first run..."
echo ""

pip3 install -r prototype/requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "   ✓ Dependencies installed successfully"
else
    echo ""
    echo "   ❌ Failed to install dependencies"
    exit 1
fi

# Create directories
echo ""
echo "📁 Creating directory structure..."
mkdir -p models
mkdir -p swatches/curtains
mkdir -p swatches/blinds
mkdir -p swatches/shades
mkdir -p test_images
mkdir -p test_results
echo "   ✓ Directories created"

# Download models
echo ""
echo "🤖 Downloading AI models..."
echo "   This will download ~300MB (7GB if including SDXL)"
echo ""
read -p "   Download SDXL for AI rendering? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 prototype/download_models.py --with-sdxl
else
    python3 prototype/download_models.py
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "   ✓ Models downloaded successfully"
else
    echo ""
    echo "   ❌ Model download failed"
    exit 1
fi

# Download sample swatches
echo ""
echo "🎨 Downloading sample fabric swatches..."
if [ -f swatches/download_samples.sh ]; then
    chmod +x swatches/download_samples.sh
    cd swatches && ./download_samples.sh && cd ..
    echo "   ✓ Sample swatches downloaded"
else
    echo "   ⚠️  Download script not found, skipping swatches"
    echo "   You can add swatches manually to swatches/ directory"
fi

# Download sample test images (optional)
echo ""
read -p "📷 Download sample test images? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   Downloading 5 sample test images..."
    
    # Create simple download script
    mkdir -p test_images/samples
    
    # Download a few sample images
    curl -L -o test_images/samples/living_room_1.jpg \
      "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=1024&q=80" 2>/dev/null &
    
    curl -L -o test_images/samples/bedroom_1.jpg \
      "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=1024&q=80" 2>/dev/null &
    
    curl -L -o test_images/samples/office_1.jpg \
      "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1024&q=80" 2>/dev/null &
    
    wait
    
    COUNT=$(ls test_images/samples/*.jpg 2>/dev/null | wc -l)
    echo "   ✓ Downloaded $COUNT test images"
else
    echo "   Skipping test images - add your own to test_images/"
fi

# Verify installation
echo ""
echo "✅ Running installation verification..."
python3 prototype/download_models.py --verify

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  ✅ Setup Complete!                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📂 Directory Structure:"
echo "   models/          - AI models ($(ls models 2>/dev/null | wc -l) files)"
echo "   swatches/        - Fabric swatches ($(find swatches -name "*.jpg" 2>/dev/null | wc -l) files)"
echo "   test_images/     - Test images ($(find test_images -name "*.jpg" 2>/dev/null | wc -l) files)"
echo ""
echo "🚀 Quick Start:"
echo ""
echo "   1. Launch Gradio UI:"
echo "      cd prototype && python3 app.py"
echo "      Then open: http://localhost:7860"
echo ""
echo "   2. Run batch tests:"
echo "      python3 prototype/test_pipeline.py --input test_images"
echo ""
echo "   3. Test single image:"
echo "      python3 prototype/test_pipeline.py --single path/to/image.jpg"
echo ""
echo "📚 Documentation:"
echo "   - prototype/README.md       - Usage guide"
echo "   - prototype/TEST_CASES.md   - Test scenarios"
echo "   - swatches/README.md        - Adding swatches"
echo "   - test_images/README.md     - Test image requirements"
echo ""
echo "💡 Next Steps:"
echo "   1. Add your test images to test_images/"
echo "   2. Add vendor swatches to swatches/"
echo "   3. Run validation tests (see prototype/TEST_CASES.md)"
echo "   4. Collect feedback (see prototype/evaluation_form.md)"
echo "   5. Document results (see prototype/RESULTS.md)"
echo ""
echo "🐛 Troubleshooting:"
echo "   - Out of VRAM: Use CPU mode or close other GPU apps"
echo "   - Models not loading: Re-run python3 prototype/download_models.py"
echo "   - Slow performance: Check GPU with nvidia-smi"
echo ""
echo "Good luck with Week 1 validation! 🎉"
echo ""
