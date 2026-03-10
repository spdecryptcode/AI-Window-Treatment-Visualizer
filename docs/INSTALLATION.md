# Installation Guide

Production deployment guide for AI Window Treatment Visualizer on sales rep laptops.

---

## Prerequisites

### Hardware Requirements

**Minimum Specification:**
- NVIDIA RTX 3060 GPU (12GB VRAM)
- Intel Core i5 or AMD Ryzen 5 (or better)
- 16GB RAM
- 50GB free storage (SSD recommended)
- Windows 10/11, macOS 12+, or Ubuntu 20.04+

**Recommended Specification:**
- NVIDIA RTX 4060 GPU (16GB VRAM)
- Intel Core i7 or AMD Ryzen 7
- 32GB RAM
- 100GB free storage (NVMe SSD)
- Windows 11 or Ubuntu 22.04

**Check GPU:**

```bash
# Windows
nvidia-smi

# macOS (if NVIDIA eGPU)
system_profiler SPDisplaysDataType

# Linux
nvidia-smi
lspci | grep -i nvidia
```

Expected output should show RTX 3060 or better with 12GB+ VRAM.

### Software Requirements

**All Platforms:**
- NVIDIA GPU Driver 525.xx or newer
- Docker Desktop 24.0+ (with NVIDIA Container Toolkit on Linux)
- Git 2.30+
- 10 Mbps+ internet (for initial setup only)

**Platform-Specific:**

**Windows:**
- WSL2 enabled
- Docker Desktop with WSL2 backend
- Visual C++ Redistributable 2019+

**macOS:**
- Docker Desktop for Mac
- Note: Apple Silicon not supported (requires NVIDIA GPU)

**Linux:**
- Docker Engine 24.0+
- NVIDIA Container Toolkit
- docker-compose 2.20+

---

## Installation Steps

### Step 1: Install NVIDIA Drivers

**Windows:**

1. Download latest Game Ready Driver from [nvidia.com/drivers](https://nvidia.com/drivers)
2. Run installer, select "Custom Installation"
3. Check "Perform clean installation"
4. Reboot after installation
5. Verify: `nvidia-smi` in PowerShell

**Linux (Ubuntu/Debian):**

```bash
# Add NVIDIA PPA
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install driver (525 or newer)
sudo apt install nvidia-driver-535

# Reboot
sudo reboot

# Verify
nvidia-smi
```

**macOS:**

NVIDIA drivers bundled with eGPU setup. Follow eGPU manufacturer instructions.

### Step 2: Install Docker

**Windows:**

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Run installer
3. Enable WSL2 backend during setup
4. Start Docker Desktop
5. Verify in PowerShell:

```powershell
docker --version
docker run hello-world
```

**macOS:**

```bash
# Install via Homebrew
brew install --cask docker

# Or download from docker.com
# Start Docker Desktop from Applications
# Verify
docker --version
```

**Linux (Ubuntu):**

```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose-plugin

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU in Docker
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Step 3: Clone Repository

```bash
# Navigate to desired installation directory
cd ~/Projects  # or C:\Projects on Windows

# Clone repository
git clone https://github.com/your-org/window_treatment.git
cd window_treatment
```

### Step 4: Download AI Models

**Option A: Automated Download**

```bash
# Run model download script
make download-models

# This will download:
# - YOLOv8n (~6MB)
# - FastSAM-s (~145MB)
# - MiDaS Small (~80MB)
# - SDXL or SD 1.5 + LCM (~2-7GB depending on path)
#
# Total: ~2.5GB (Classical) or ~7.5GB (SDXL)
# Time: 5-15 minutes on 10 Mbps connection
```

**Option B: Manual Download**

If automated download fails:

1. Download models from provided links (see `docs/MODEL_SOURCES.md`)
2. Place in respective directories:
   - `models/yolov8/yolov8n.pt`
   - `models/fastsam/FastSAM-s.pt`
   - `models/midas/dpt_swin2_tiny_256.pt`
   - `models/sdxl/` (if using SDXL path)

### Step 5: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional)
nano .env  # or notepad .env on Windows
```

**Key configuration options:**

```bash
# .env file

# Rendering mode
RENDER_MODE=classical  # or 'sdxl'

# Model paths (usually auto-detected)
MODELS_DIR=/app/models

# Swatch storage
SWATCHES_DIR=/app/materials/swatches

# Performance tuning
MAX_IMAGE_SIZE=1024
ENABLE_CACHE=true
VRAM_RESERVED=2048  # MB to reserve for system

# Database
DB_PATH=/app/data/swatches.db

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

### Step 6: Build Docker Containers

```bash
# Build all containers
make build

# This will:
# - Build backend container (~10GB, includes CUDA)
# - Build frontend container (~500MB)
# - Set up volumes for models and swatches
# Time: 15-30 minutes on first build
```

**Manual build (if Makefile unavailable):**

```bash
# Build backend
docker build -f docker/Dockerfile.backend -t window-treatment-backend .

# Build frontend
docker build -f docker/Dockerfile.frontend -t window-treatment-frontend .
```

### Step 7: Initialize Database

```bash
# Create database and load sample swatches
make init-db

# Or manually:
docker-compose run --rm backend python scripts/seed_swatches.py
```

### Step 8: Start Application

```bash
# Start all services
make start

# Or using docker-compose:
docker-compose up -d

# Check status
docker-compose ps

# Expected output:
# NAME                    STATUS
# window-treatment-backend    Up
# window-treatment-frontend   Up
```

### Step 9: Verify Installation

**Check services:**

```bash
# Backend health check
curl http://localhost:8000/api/health

# Expected response:
# {
#   "status": "healthy",
#   "models_loaded": true,
#   "vram_available": "10.5 GB",
#   "version": "1.0.0"
# }
```

**Access frontend:**

Open browser to: `http://localhost:3000`

You should see the upload interface.

**Run test image:**

1. Upload a test image from `test_data/sample_rooms/`
2. Verify window detection works
3. Select treatment and swatch
4. Generate preview
5. Check processing completes in <15 seconds

---

## Post-Installation Setup

### Load Vendor Swatches

```bash
# Copy vendor swatch images to materials directory
cp -r /path/to/vendor/swatches/* materials/swatches/

# Process and import to database
make import-swatches

# Or manually:
docker-compose exec backend python scripts/import_swatches.py /app/materials/swatches
```

### Configure Company Branding

Edit `frontend/.env.local`:

```bash
NEXT_PUBLIC_COMPANY_NAME="Your Company Name"
NEXT_PUBLIC_LOGO_URL="/images/logo.png"
NEXT_PUBLIC_CONTACT_EMAIL="support@yourcompany.com"
```

Place logo at `frontend/public/images/logo.png`

### Set Up User Accounts (if multi-user)

```bash
# Create sales rep user
docker-compose exec backend python scripts/create_user.py \
  --name "John Doe" \
  --email "john@company.com" \
  --role "sales_rep"
```

### Backup Configuration

```bash
# Backup database and configuration
make backup

# Creates timestamped backup in backups/
# Includes: database, .env, swatch metadata
```

---

## Updating

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
make build

# Restart services
make restart

# Run migrations (if any)
make migrate
```

### Update Models

```bash
# Download new model versions
make update-models

# Restart backend
docker-compose restart backend
```

### Update Swatches

```bash
# Import new swatches
make import-swatches

# No restart required
```

---

## Uninstallation

### Full Removal

```bash
# Stop all services
make stop

# Remove containers and volumes
docker-compose down -v

# Remove images
docker rmi window-treatment-backend window-treatment-frontend

# Remove cloned repository
cd ..
rm -rf window_treatment

# Remove Docker (optional)
# Windows: Uninstall Docker Desktop from Control Panel
# macOS: Remove Docker.app from Applications
# Linux: sudo apt remove docker-ce docker-compose-plugin
```

### Partial Removal (keep models/data)

```bash
# Stop services
make stop

# Remove containers only
docker-compose down

# Models and data remain in models/ and materials/
```

---

## Troubleshooting

### NVIDIA Driver Issues

**"nvidia-smi command not found"**

- Driver not installed or not in PATH
- Reinstall NVIDIA driver
- Windows: Check PATH includes `C:\Program Files\NVIDIA Corporation\NVSMI`

**"CUDA driver version is insufficient"**

- Driver too old for CUDA 12.1
- Update to driver 525.xx or newer

### Docker Issues

**"Cannot connect to Docker daemon"**

- Docker Desktop not running
- Windows: Check WSL2 is enabled
- Linux: Check docker service: `sudo systemctl status docker`

**"docker: Error response from daemon: could not select device driver"**

- NVIDIA Container Toolkit not installed (Linux)
- Follow Step 2 Linux instructions for nvidia-container-toolkit

**"no matching manifest for platform"**

- Pulling wrong architecture image
- Ensure using x86_64/amd64, not ARM
- macOS Intel required (Apple Silicon not supported)

### VRAM Issues

**"CUDA out of memory"**

- Other GPU applications running (close them)
- Reduce `MAX_IMAGE_SIZE` in `.env`
- Switch to Classical rendering mode (lower VRAM)
- Check `nvidia-smi` for memory usage

**Models not loading:**

- Check model files exist: `ls -lh models/*/`
- Check file permissions
- Re-run `make download-models`
- Check disk space: `df -h`

### Performance Issues

**Rendering takes >30 seconds:**

- Check GPU utilization: `nvidia-smi dmon`
- Verify models on GPU not CPU (check logs)
- Ensure CUDA version matches PyTorch
- Check CPU/RAM not bottlenecking
- Reduce image size

**Frontend won't connect to backend:**

- Check backend is running: `docker-compose ps`
- Check backend health: `curl localhost:8000/api/health`
- Check CORS configuration (should allow localhost:3000)
- Check firewall not blocking port 8000

### Database Issues

**"no such table: swatches"**

- Database not initialized
- Run: `make init-db`

**Swatches not appearing:**

- Import not completed
- Check: `docker-compose exec backend sqlite3 /app/data/swatches.db "SELECT COUNT(*) FROM swatches;"`
- Should show >0
- Re-run: `make import-swatches`

---

## Performance Tuning

### For RTX 3060 (12GB VRAM)

```bash
# .env settings
MAX_IMAGE_SIZE=1024
RENDER_MODE=classical
ENABLE_MODEL_UNLOAD=true
BATCH_SIZE=1
```

### For RTX 4060+ (16GB+ VRAM)

```bash
# .env settings
MAX_IMAGE_SIZE=1920
RENDER_MODE=sdxl  # if Phase 2
ENABLE_MODEL_UNLOAD=false  # keep in VRAM
BATCH_SIZE=4  # batch swatch rendering
```

### Low-end Systems (RTX 3050)

```bash
# .env settings
MAX_IMAGE_SIZE=768
RENDER_MODE=classical
ENABLE_MODEL_UNLOAD=true
FP16_INFERENCE=true
REDUCE_PRECISION=true
```

---

## Support

### Log Files

```bash
# View backend logs
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend

# View frontend logs
docker-compose logs frontend

# Export logs
docker-compose logs > logs.txt
```

### Diagnostic Script

```bash
# Run system diagnostic
make diagnose

# Checks:
# - NVIDIA driver version
# - Docker installation
# - Model files present
# - Database integrity
# - Port availability
# - Disk space
```

### Get Help

1. Check logs: `docker-compose logs`
2. Check health: `curl localhost:8000/api/health`
3. Run diagnostic: `make diagnose`
4. Review troubleshooting section above
5. Contact: support@yourcompany.com

---

## System Requirements Summary

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | RTX 3060 12GB | RTX 4060 16GB |
| CPU | Core i5 / Ryzen 5 | Core i7 / Ryzen 7 |
| RAM | 16GB | 32GB |
| Storage | 50GB SSD | 100GB NVMe |
| OS | Win10, macOS 12, Ubuntu 20.04 | Win11, Ubuntu 22.04 |
| Driver | NVIDIA 525+ | NVIDIA 545+ |
| Internet | 10 Mbps (setup only) | Offline after setup |

---

**Installation Support:** support@yourcompany.com  
**Documentation:** [docs/](../docs/)  
**Version:** 1.0  
**Last Updated:** February 16, 2026
