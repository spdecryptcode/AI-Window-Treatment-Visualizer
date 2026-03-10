#!/usr/bin/env python3
"""
Download AI models for Window Treatment Visualizer prototype.

Run once before first use:
    python download_models.py
"""

import os
from pathlib import Path
import requests
from tqdm import tqdm
from huggingface_hub import hf_hub_download


def download_file(url, dest_path, desc="Downloading"):
    """Download file with progress bar."""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    if dest_path.exists():
        print(f"✓ Already exists: {dest_path.name}")
        return
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(dest_path, 'wb') as file, tqdm(
        desc=desc,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)
    
    print(f"✓ Downloaded: {dest_path.name}")


def download_yolov8():
    """Download YOLOv8 nano model."""
    print("\n📦 Downloading YOLOv8n...")
    
    models_dir = Path("models/yolov8")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # YOLOv8n is downloaded automatically by ultralytics on first use
    # But we can pre-download it
    from ultralytics import YOLO
    
    model = YOLO('yolov8n.pt')  # Auto-downloads to ~/.ultralytics/
    
    # Copy to our models directory
    import shutil
    cache_path = Path.home() / '.ultralytics' / 'weights' / 'yolov8n.pt'
    dest_path = models_dir / 'yolov8n.pt'
    
    if cache_path.exists() and not dest_path.exists():
        shutil.copy(cache_path, dest_path)
        print(f"✓ YOLOv8n ready at {dest_path}")
    else:
        print(f"✓ YOLOv8n already available")


def download_fastsam():
    """Download FastSAM model."""
    print("\n📦 Downloading FastSAM-s...")
    
    models_dir = Path("models/fastsam")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    dest_path = models_dir / "FastSAM-s.pt"
    
    if dest_path.exists():
        print(f"✓ FastSAM-s already exists")
        return
    
    # Download from GitHub releases
    url = "https://github.com/CASIA-IVA-Lab/FastSAM/releases/download/v0.1.0/FastSAM-s.pt"
    
    try:
        download_file(url, dest_path, desc="FastSAM-s")
    except Exception as e:
        print(f"❌ Failed to download FastSAM: {e}")
        print("   Please download manually from:")
        print("   https://github.com/CASIA-IVA-Lab/FastSAM/releases")


def download_midas():
    """Download MiDaS depth estimation model."""
    print("\n📦 Downloading MiDaS v2.1 Small...")
    
    models_dir = Path("models/midas")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # MiDaS is loaded via torch.hub - pre-download it
        import torch
        torch.hub.load_state_dict_from_url(
            'https://github.com/isl-org/MiDaS/releases/download/v2_1/midas_v21_small_256.pt',
            map_location='cpu',
            file_name='midas_v21_small_256.pt'
        )
        print(f"✓ MiDaS downloaded to torch cache")
        
    except Exception as e:
        print(f"❌ Failed to pre-download MiDaS: {e}")
        print("   Will download automatically on first use")


def download_sdxl():
    """Download SDXL inpainting model (optional, for SDXL rendering path)."""
    print("\n📦 Downloading SDXL Inpainting (optional, ~7GB)...")
    print("   This may take 10-20 minutes on slow connections...")
    
    response = input("Download SDXL now? (y/n, recommended to skip for classical path): ").lower()
    
    if response != 'y':
        print("⊘ Skipped SDXL download. You can download later if needed.")
        return
    
    models_dir = Path("models/sdxl")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        from diffusers import StableDiffusionXLInpaintPipeline
        
        print("   Downloading SDXL model components...")
        pipeline = StableDiffusionXLInpaintPipeline.from_pretrained(
            "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
            cache_dir=str(models_dir)
        )
        
        print("✓ SDXL Inpainting downloaded successfully")
        
    except Exception as e:
        print(f"❌ Failed to download SDXL: {e}")
        print("   You can skip SDXL and use classical rendering instead")


def check_gpu():
    """Check if GPU is available."""
    print("\n🔍 Checking GPU availability...")
    
    import torch
    
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"✓ GPU detected: {gpu_name}")
        print(f"  VRAM: {vram:.1f} GB")
        
        if vram < 10:
            print("  ⚠️  Warning: Less than 12GB VRAM. May need to use classical rendering only.")
        else:
            print("  ✓ Sufficient VRAM for all rendering modes")
    else:
        print("⚠️  No NVIDIA GPU detected!")
        print("   Running in CPU mode (slower performance)")
        print("   For production: Install CUDA from https://developer.nvidia.com/cuda-downloads")
        print("   NOTE: CPU mode is fine for development/testing but will be slower.")
    
    return True


def verify_installation():
    """Verify all models are present."""
    print("\n✅ Verifying installation...")
    
    required_models = [
        ("models/fastsam/FastSAM-s.pt", "FastSAM-s"),
    ]
    
    optional_models = []
    
    all_present = True
    
    # Check YOLOv8 in ultralytics cache
    yolo_cache = Path.home() / '.ultralytics' / 'weights' / 'yolov8n.pt'
    if yolo_cache.exists():
        size = yolo_cache.stat().st_size / 1e6
        print(f"  ✓ YOLOv8n: {size:.1f} MB (in cache)")
    else:
        print(f"  ⊘ YOLOv8n: Will download on first use")
    
    for path, name in required_models:
        if Path(path).exists():
            size = Path(path).stat().st_size / 1e6
            print(f"  ✓ {name}: {size:.1f} MB")
        else:
            print(f"  ❌ {name}: NOT FOUND")
            all_present = False
    
    # MiDaS note
    print(f"  ⊘ MiDaS: Will download on first use via torch.hub")
    
    for path, name in optional_models:
        if Path(path).exists():
            size = Path(path).stat().st_size / 1e6
            print(f"  ✓ {name}: {size:.1f} MB")
        else:
            print(f"  ⊘ {name}: Not downloaded (will download on first use)")
    
    return all_present


def main():
    """Main download workflow."""
    print("=" * 60)
    print("AI Window Treatment Visualizer - Model Downloader")
    print("=" * 60)
    
    # Check GPU (informational only, not required)
    check_gpu()
    
    # Download models
    try:
        download_yolov8()
        download_fastsam()
        download_midas()
        download_sdxl()  # Optional
        
    except KeyboardInterrupt:
        print("\n\n⊘ Download interrupted by user")
        return 1
    
    except Exception as e:
        print(f"\n❌ Error during download: {e}")
        return 1
    
    # Verify
    print("\n" + "=" * 60)
    if verify_installation():
        print("\n✅ Setup complete! All required models downloaded.")
        print("\nNext steps:")
        print("  1. Run prototype: python app.py")
        print("  2. Open browser to: http://localhost:7860")
    else:
        print("\n⚠️  Some models missing. Please retry or download manually.")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
