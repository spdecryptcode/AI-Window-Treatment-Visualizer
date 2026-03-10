"""
Batch test script for prototype validation.

Tests the pipeline on multiple images to evaluate:
- Detection accuracy
- Segmentation quality
- Rendering speed
- Overall system performance

Usage:
    python test_pipeline.py --input test_images/ --output test_results/
"""

import argparse
from pathlib import Path
import cv2
import numpy as np
import time
import json
from typing import Dict, List
from datetime import datetime

from pipeline import WindowDetector, WindowSegmenter, DepthEstimator, calculate_treatment_geometry
from classical_renderer import ClassicalRenderer, load_swatch


class PrototypeTester:
    """Test harness for window treatment prototype."""
    
    def __init__(self, output_dir: str = "test_results"):
        """Initialize tester with models."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n🔧 Initializing test environment...")
        
        # Initialize models
        self.detector = WindowDetector()
        self.segmenter = WindowSegmenter()
        self.depth_estimator = DepthEstimator()
        self.renderer = ClassicalRenderer()
        
        # Load test swatches
        self.swatches = self._load_test_swatches()
        
        # Results tracking
        self.results = []
        
        print("✅ Test environment ready\n")
    
    def _load_test_swatches(self) -> Dict[str, np.ndarray]:
        """Load swatches for testing."""
        swatches = {}
        swatch_dir = Path("swatches")
        
        if not swatch_dir.exists():
            print("⚠️  No swatches directory found, will use synthetic textures")
            # Create synthetic swatches
            swatches['beige_linen'] = self._create_synthetic_swatch((220, 200, 180))
            swatches['gray_cotton'] = self._create_synthetic_swatch((180, 180, 180))
            swatches['wood_blinds'] = self._create_synthetic_swatch((160, 120, 80))
        else:
            # Load actual swatches
            for treatment_dir in swatch_dir.iterdir():
                if treatment_dir.is_dir():
                    for swatch_file in treatment_dir.glob("*.jpg"):
                        name = f"{treatment_dir.name}_{swatch_file.stem}"
                        swatches[name] = load_swatch(str(swatch_file))
        
        print(f"  Loaded {len(swatches)} test swatches")
        return swatches
    
    def _create_synthetic_swatch(self, color: tuple) -> np.ndarray:
        """Create synthetic fabric texture for testing."""
        swatch = np.ones((512, 512, 3), dtype=np.uint8)
        swatch[:] = color
        
        # Add subtle noise for texture
        noise = np.random.randint(-10, 10, (512, 512, 3), dtype=np.int16)
        swatch = np.clip(swatch.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        return swatch
    
    def test_image(
        self,
        image_path: str,
        treatment_type: str = 'curtains',
        swatch_name: str = None
    ) -> Dict:
        """Test pipeline on single image."""
        
        print(f"\n📷 Testing: {Path(image_path).name}")
        print("-" * 60)
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Failed to load image: {image_path}")
            return None
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize if needed
        max_size = 1024
        h, w = image.shape[:2]
        if max(h, w) > max_size:
            scale = max_size / max(h, w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            image = cv2.resize(image, (new_w, new_h))
        
        result = {
            'image_path': str(image_path),
            'image_size': f"{image.shape[1]}x{image.shape[0]}",
            'timestamp': datetime.now().isoformat(),
            'treatment_type': treatment_type
        }
        
        timings = {}
        
        # Step 1: Detection
        print("  🔍 Running detection...")
        t0 = time.time()
        
        try:
            detections = self.detector.detect(image, confidence=0.5)
            timings['detection'] = time.time() - t0
            
            result['detections'] = {
                'count': len(detections),
                'confidences': [d['confidence'] for d in detections],
                'avg_confidence': np.mean([d['confidence'] for d in detections]) if detections else 0
            }
            
            print(f"     ✓ Found {len(detections)} windows ({timings['detection']:.2f}s)")
            
        except Exception as e:
            print(f"     ❌ Detection failed: {e}")
            result['error'] = f"Detection: {str(e)}"
            return result
        
        if not detections:
            print("     ⚠️  No windows detected")
            result['error'] = "No windows detected"
            return result
        
        # Use first detection
        detection = detections[0]
        bbox = detection['bbox']
        
        # Step 2: Segmentation
        print("  ✂️  Running segmentation...")
        t0 = time.time()
        
        try:
            seg_result = self.segmenter.segment(image, bbox)
            timings['segmentation'] = time.time() - t0
            
            result['segmentation'] = {
                'quality_score': seg_result['quality_score'],
                'mask_coverage': np.sum(seg_result['combined_mask'] > 0) / seg_result['combined_mask'].size
            }
            
            print(f"     ✓ Segmented (quality: {seg_result['quality_score']:.2f}, {timings['segmentation']:.2f}s)")
            
        except Exception as e:
            print(f"     ❌ Segmentation failed: {e}")
            result['error'] = f"Segmentation: {str(e)}"
            return result
        
        # Step 3: Depth Estimation
        print("  📏 Running depth estimation...")
        t0 = time.time()
        
        try:
            depth_result = self.depth_estimator.estimate(image, bbox)
            timings['depth'] = time.time() - t0
            
            result['depth'] = {
                'estimation_method': depth_result['estimation_method']
            }
            
            print(f"     ✓ Depth estimated ({timings['depth']:.2f}s)")
            
        except Exception as e:
            print(f"     ❌ Depth estimation failed: {e}")
            result['error'] = f"Depth: {str(e)}"
            return result
        
        # Step 4: Geometry Calculation
        print("  📐 Calculating geometry...")
        t0 = time.time()
        
        try:
            geometry = calculate_treatment_geometry(
                seg_result['combined_mask'],
                depth_result['depth_map'],
                treatment_type=treatment_type
            )
            timings['geometry'] = time.time() - t0
            
            result['geometry'] = {
                'valid': geometry['valid'],
                'treatment_bbox': geometry['treatment_bbox']
            }
            
            if not geometry['valid']:
                print("     ⚠️  Invalid geometry")
                result['error'] = "Invalid geometry"
                return result
            
            print(f"     ✓ Geometry calculated ({timings['geometry']:.2f}s)")
            
        except Exception as e:
            print(f"     ❌ Geometry calculation failed: {e}")
            result['error'] = f"Geometry: {str(e)}"
            return result
        
        # Step 5: Rendering
        print("  🎨 Rendering treatment...")
        t0 = time.time()
        
        try:
            # Select swatch
            if swatch_name and swatch_name in self.swatches:
                swatch = self.swatches[swatch_name]
            else:
                swatch = list(self.swatches.values())[0]
                swatch_name = list(self.swatches.keys())[0]
            
            rendered = self.renderer.render(
                image,
                seg_result['combined_mask'],
                swatch,
                geometry,
                depth_result['depth_map'],
                treatment_type=treatment_type
            )
            
            timings['rendering'] = time.time() - t0
            result['swatch'] = swatch_name
            
            print(f"     ✓ Rendered ({timings['rendering']:.2f}s)")
            
        except Exception as e:
            print(f"     ❌ Rendering failed: {e}")
            result['error'] = f"Rendering: {str(e)}"
            return result
        
        # Total time
        timings['total'] = sum(timings.values())
        result['timings'] = timings
        
        print(f"\n  ⏱️  Total time: {timings['total']:.2f}s")
        print(f"     Detection: {timings['detection']:.2f}s")
        print(f"     Segmentation: {timings['segmentation']:.2f}s")
        print(f"     Depth: {timings['depth']:.2f}s")
        print(f"     Geometry: {timings['geometry']:.2f}s")
        print(f"     Rendering: {timings['rendering']:.2f}s")
        
        # Save outputs
        output_name = Path(image_path).stem
        
        # Save detection visualization
        det_viz = image.copy()
        x, y, w, h = bbox
        cv2.rectangle(det_viz, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.imwrite(
            str(self.output_dir / f"{output_name}_1_detection.jpg"),
            cv2.cvtColor(det_viz, cv2.COLOR_RGB2BGR)
        )
        
        # Save segmentation visualization
        seg_viz = image.copy()
        mask = seg_result['combined_mask']
        blue_overlay = np.zeros_like(image)
        blue_overlay[:, :, 2] = mask
        seg_viz = cv2.addWeighted(seg_viz, 0.6, blue_overlay, 0.4, 0)
        cv2.imwrite(
            str(self.output_dir / f"{output_name}_2_segmentation.jpg"),
            cv2.cvtColor(seg_viz, cv2.COLOR_RGB2BGR)
        )
        
        # Save final render
        cv2.imwrite(
            str(self.output_dir / f"{output_name}_3_rendered.jpg"),
            cv2.cvtColor(rendered, cv2.COLOR_RGB2BGR)
        )
        
        # Save before/after comparison
        comparison = np.hstack([image, rendered])
        cv2.imwrite(
            str(self.output_dir / f"{output_name}_4_comparison.jpg"),
            cv2.cvtColor(comparison, cv2.COLOR_RGB2BGR)
        )
        
        print(f"  💾 Results saved to {self.output_dir}/")
        
        result['success'] = True
        return result
    
    def test_directory(
        self,
        input_dir: str,
        treatment_type: str = 'curtains',
        max_images: int = None
    ):
        """Test all images in directory."""
        
        input_path = Path(input_dir)
        
        if not input_path.exists():
            print(f"❌ Directory not found: {input_dir}")
            return
        
        # Find all images
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_files.extend(input_path.glob(ext))
        
        if max_images:
            image_files = image_files[:max_images]
        
        print(f"\n{'='*60}")
        print(f"Testing {len(image_files)} images from {input_dir}")
        print(f"{'='*60}")
        
        # Test each image
        for i, image_file in enumerate(image_files, 1):
            print(f"\n[{i}/{len(image_files)}]", end=" ")
            
            result = self.test_image(str(image_file), treatment_type=treatment_type)
            
            if result:
                self.results.append(result)
        
        # Generate summary report
        self._generate_report()
    
    def _generate_report(self):
        """Generate summary report from test results."""
        
        if not self.results:
            print("\n⚠️  No results to report")
            return
        
        print(f"\n\n{'='*60}")
        print("TEST SUMMARY REPORT")
        print(f"{'='*60}\n")
        
        # Success rate
        successful = [r for r in self.results if r.get('success', False)]
        success_rate = len(successful) / len(self.results) * 100
        
        print(f"Total Images: {len(self.results)}")
        print(f"Successful: {len(successful)} ({success_rate:.1f}%)")
        print(f"Failed: {len(self.results) - len(successful)}")
        
        if successful:
            # Timing statistics
            all_times = [r['timings']['total'] for r in successful]
            
            print(f"\n⏱️  Performance:")
            print(f"  Average total time: {np.mean(all_times):.2f}s")
            print(f"  Min time: {np.min(all_times):.2f}s")
            print(f"  Max time: {np.max(all_times):.2f}s")
            
            # Detection statistics
            all_detections = [r['detections']['count'] for r in successful]
            all_confidences = [r['detections']['avg_confidence'] for r in successful]
            
            print(f"\n🔍 Detection:")
            print(f"  Average windows per image: {np.mean(all_detections):.1f}")
            print(f"  Average confidence: {np.mean(all_confidences):.2f}")
            
            # Segmentation quality
            all_quality = [r['segmentation']['quality_score'] for r in successful]
            
            print(f"\n✂️  Segmentation:")
            print(f"  Average quality score: {np.mean(all_quality):.2f}")
            print(f"  Min quality: {np.min(all_quality):.2f}")
            print(f"  Max quality: {np.max(all_quality):.2f}")
        
        # Failure analysis
        if len(successful) < len(self.results):
            print(f"\n❌ Failures:")
            for r in self.results:
                if not r.get('success', False):
                    print(f"  {Path(r['image_path']).name}: {r.get('error', 'Unknown error')}")
        
        # Save full results
        report_file = self.output_dir / "test_report.json"
        with open(report_file, 'w') as f:
            json.dump({
                'summary': {
                    'total': len(self.results),
                    'successful': len(successful),
                    'success_rate': success_rate,
                    'avg_time': np.mean(all_times) if successful else 0,
                    'avg_confidence': np.mean(all_confidences) if successful else 0,
                    'avg_quality': np.mean(all_quality) if successful else 0
                },
                'results': self.results
            }, f, indent=2)
        
        print(f"\n💾 Full report saved to: {report_file}")
        print(f"📁 Visual results in: {self.output_dir}/\n")


def main():
    parser = argparse.ArgumentParser(description="Test window treatment prototype")
    
    parser.add_argument(
        '--input',
        default='test_images',
        help='Input directory with test images'
    )
    
    parser.add_argument(
        '--output',
        default='test_results',
        help='Output directory for results'
    )
    
    parser.add_argument(
        '--treatment',
        default='curtains',
        choices=['curtains', 'blinds', 'shades'],
        help='Treatment type to render'
    )
    
    parser.add_argument(
        '--max-images',
        type=int,
        default=None,
        help='Maximum number of images to test'
    )
    
    parser.add_argument(
        '--single',
        type=str,
        default=None,
        help='Test single image instead of directory'
    )
    
    args = parser.parse_args()
    
    # Create tester
    tester = PrototypeTester(output_dir=args.output)
    
    # Test single image or directory
    if args.single:
        result = tester.test_image(args.single, treatment_type=args.treatment)
        if result:
            tester.results.append(result)
            tester._generate_report()
    else:
        tester.test_directory(
            args.input,
            treatment_type=args.treatment,
            max_images=args.max_images
        )


if __name__ == "__main__":
    main()
