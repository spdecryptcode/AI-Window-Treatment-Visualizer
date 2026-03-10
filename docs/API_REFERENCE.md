# API Reference

Complete API documentation for the Window Treatment Visualizer backend.

**Base URL:** `http://localhost:8000/api`

**Version:** 1.0

**Authentication:** None for MVP (can be added later)

---

## Table of Contents

- [Health & Status](#health--status)
- [Image Upload](#image-upload)
- [Window Detection](#window-detection)
- [Segmentation](#segmentation)
- [Rendering](#rendering)
- [Swatches](#swatches)
- [Export](#export)
- [Admin](#admin)
- [WebSocket](#websocket)

---

## Health & Status

### GET /health

Check API health and model status.

**Request:**

```bash
curl http://localhost:8000/api/health
```

**Response: 200 OK**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_loaded": true,
  "models": {
    "yolo": {"loaded": true, "version": "yolov8n"},
    "fastsam": {"loaded": true, "version": "fastsam-s"},
    "midas": {"loaded": true, "version": "midas_v21_small"},
    "sdxl": {"loaded": false, "reason": "classical mode"}
  },
  "vram": {
    "available": "10.5 GB",
    "used": "1.2 GB",
    "total": "12.0 GB"
  },
  "config": {
    "render_mode": "classical",
    "max_image_size": 1024,
    "cache_enabled": true
  }
}
```

**Status Codes:**
- `200` - Healthy
- `503` - Service unavailable (models not loaded)

---

## Image Upload

### POST /upload

Upload and preprocess room image.

**Request:**

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/room.jpg"
```

**Form Data:**
- `file` (required) - Image file (JPG/PNG, max 10MB)

**Response: 200 OK**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "room.jpg",
  "original_size": [1920, 1080],
  "processed_size": [1024, 576],
  "format": "JPEG",
  "preview_url": "/uploads/550e8400.jpg"
}
```

**Processing:**
- Resizes to max 1024px (maintains aspect ratio)
- Removes EXIF data
- Normalizes orientation
- Stores temporarily with UUID

**Status Codes:**
- `200` - Success
- `400` - Invalid file format or size
- `413` - File too large (>10MB)
- `500` - Processing error

**Error Response:**

```json
{
  "error": "invalid_format",
  "message": "File must be JPG or PNG",
  "detail": "Received: image/webp"
}
```

---

## Window Detection

### POST /detect

Detect windows in uploaded image using YOLOv8.

**Request:**

```bash
curl -X POST http://localhost:8000/api/detect \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "550e8400-e29b-41d4-a716-446655440000",
    "confidence_threshold": 0.5
  }'
```

**Request Body:**

```json
{
  "image_id": "string (required)",
  "confidence_threshold": 0.5,  // 0.0 - 1.0, default 0.5
  "max_detections": 10          // max windows to detect, default 10
}
```

**Response: 200 OK**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "detections": [
    {
      "detection_id": "det_001",
      "class": "window",
      "confidence": 0.89,
      "bbox": {
        "x": 320,
        "y": 150,
        "width": 400,
        "height": 500
      },
      "center": [520, 400],
      "area": 200000
    },
    {
      "detection_id": "det_002",
      "class": "sliding_door",
      "confidence": 0.76,
      "bbox": {
        "x": 50,
        "y": 200,
        "width": 250,
        "height": 600
      },
      "center": [175, 500],
      "area": 150000
    }
  ],
  "total_detections": 2,
  "processing_time": 1.85,
  "visualization_url": "/results/550e8400_detection.jpg"
}
```

**Bounding Box Format:**
- `x, y` - Top-left corner coordinates
- `width, height` - Box dimensions
- Coordinates relative to processed image size

**Status Codes:**
- `200` - Success (may have 0 detections)
- `404` - Image ID not found
- `500` - Detection failed

---

## Segmentation

### POST /segment

Generate pixel-accurate mask for selected window using FastSAM.

**Request:**

```bash
curl -X POST http://localhost:8000/api/segment \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "550e8400-e29b-41d4-a716-446655440000",
    "bbox": {
      "x": 320,
      "y": 150,
      "width": 400,
      "height": 500
    }
  }'
```

**Request Body:**

```json
{
  "image_id": "string (required)",
  "bbox": {                    // Required - detection bbox or manual
    "x": 320,
    "y": 150,
    "width": 400,
    "height": 500
  },
  "refinement": {              // Optional refinement
    "erosion": 0,              // Pixels to erode (-10 to 10)
    "dilation": 0,             // Pixels to dilate (-10 to 10)
    "smooth": true             // Apply smoothing
  }
}
```

**Response: 200 OK**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "segmentation_id": "seg_001",
  "masks": {
    "glass": {
      "url": "/masks/550e8400_glass.png",
      "area": 180000,
      "bbox": [325, 155, 390, 490]
    },
    "frame": {
      "url": "/masks/550e8400_frame.png",
      "area": 20000,
      "bbox": [320, 150, 400, 500]
    },
    "combined": {
      "url": "/masks/550e8400_combined.png",
      "area": 200000,
      "bbox": [320, 150, 400, 500]
    }
  },
  "quality_score": 0.92,       // 0-1, mask quality estimate
  "processing_time": 2.1,
  "visualization_url": "/results/550e8400_segmentation.jpg"
}
```

**Mask Format:**
- PNG image with transparency
- White (255) = masked region
- Black (0) = background
- Grayscale = soft edges

**Status Codes:**
- `200` - Success
- `404` - Image ID not found
- `400` - Invalid bbox
- `500` - Segmentation failed

---

## Rendering

### POST /render

Generate photorealistic window treatment preview.

**Request:**

```bash
curl -X POST http://localhost:8000/api/render \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "550e8400-e29b-41d4-a716-446655440000",
    "segmentation_id": "seg_001",
    "treatment": {
      "type": "curtains",
      "swatch_id": 42,
      "length": "floor",
      "fullness": "standard"
    },
    "render_mode": "classical"
  }'
```

**Request Body:**

```json
{
  "image_id": "string (required)",
  "segmentation_id": "string (required)",
  "treatment": {
    "type": "curtains|blinds|shades|...",  // Required
    "swatch_id": 42,                        // Required
    "length": "floor|sill|below_sill",      // Default: floor
    "fullness": "minimal|standard|extra",   // Curtains only
    "slat_angle": 45,                       // Blinds only (0-90)
    "hardware_visible": true,               // Show mounting rod
    "hardware_color": "nickel"              // white|black|nickel|bronze|wood
  },
  "render_mode": "classical|sdxl",          // Default: classical
  "adjustments": {
    "brightness": 0,                        // -50 to +50
    "mount_offset": 4,                      // Inches above window
    "perspective_correct": true
  }
}
```

**Response: 200 OK**

```json
{
  "render_id": "ren_001",
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "result_url": "/results/550e8400_rendered.jpg",
  "high_res_url": "/results/550e8400_rendered_full.jpg",
  "processing_time": 6.8,
  "render_mode": "classical",
  "treatment_details": {
    "type": "curtains",
    "swatch": {
      "id": 42,
      "vendor": "Acme",
      "material": "100% Linen",
      "color": "Natural Beige"
    }
  },
  "cache_hit": false
}
```

**Result URLs:**
- `result_url` - Web-optimized preview (1024px max)
- `high_res_url` - Full resolution for export

**Caching:**
If same image/window/treatment already rendered, returns cached result instantly.

**Status Codes:**
- `200` - Success
- `404` - Image ID, segmentation ID, or swatch ID not found
- `400` - Invalid treatment parameters
- `500` - Rendering failed

**Background Processing:**

For batch rendering:

```bash
curl -X POST http://localhost:8000/api/render/batch \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "550e8400",
    "segmentation_id": "seg_001",
    "swatch_ids": [42, 43, 44, 45],
    "treatment_type": "curtains"
  }'
```

**Returns:**

```json
{
  "job_id": "batch_001",
  "status": "processing",
  "total": 4,
  "estimated_time": 25
}
```

Check status with `GET /render/batch/batch_001`

---

## Swatches

### GET /swatches

List available fabric swatches with filtering.

**Request:**

```bash
# Get all swatches
curl http://localhost:8000/api/swatches

# Filter by treatment type
curl "http://localhost:8000/api/swatches?treatment_type=curtains"

# Filter by vendor
curl "http://localhost:8000/api/swatches?vendor_id=5"

# Multiple filters
curl "http://localhost:8000/api/swatches?treatment_type=curtains&color=beige&price_tier=mid-range"
```

**Query Parameters:**
- `treatment_type` - Filter by type (curtains, blinds, shades, etc.)
- `vendor_id` - Filter by vendor ID
- `color` - Filter by color name (partial match)
- `price_tier` - budget, mid-range, premium
- `limit` - Results per page (default 50, max 200)
- `offset` - Pagination offset
- `search` - Search material, color, or SKU

**Response: 200 OK**

```json
{
  "swatches": [
    {
      "id": 42,
      "vendor_id": 5,
      "vendor_name": "Acme Window Coverings",
      "treatment_type": "curtains",
      "material": "100% Linen",
      "color": "Natural Beige",
      "color_hex": "#E8DCC8",
      "opacity": 0.9,
      "price_tier": "mid-range",
      "sku": "ACME-LIN-NB-001",
      "thumbnail_url": "/swatches/thumb/42.jpg",
      "preview_url": "/swatches/preview/42.jpg",
      "texture_url": "/swatches/texture/42.jpg"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

**Status Codes:**
- `200` - Success (may be empty array)

---

### GET /swatches/{id}

Get detailed information for single swatch.

**Request:**

```bash
curl http://localhost:8000/api/swatches/42
```

**Response: 200 OK**

```json
{
  "id": 42,
  "vendor_id": 5,
  "vendor": {
    "id": 5,
    "name": "Acme Window Coverings",
    "catalog_url": "https://acme.com/catalog",
    "contact": "sales@acme.com"
  },
  "treatment_type": "curtains",
  "material": "100% Linen",
  "color": "Natural Beige",
  "color_hex": "#E8DCC8",
  "opacity": 0.9,
  "price_tier": "mid-range",
  "sku": "ACME-LIN-NB-001",
  "images": {
    "thumbnail": "/swatches/thumb/42.jpg",
    "preview": "/swatches/preview/42.jpg",
    "texture": "/swatches/texture/42.jpg",
    "normal_map": "/swatches/normal/42.jpg"
  },
  "properties": {
    "roughness": 0.6,
    "metallic": 0.0,
    "specular": 0.2,
    "sheen": 0.4
  },
  "created_at": "2026-02-10T10:30:00Z"
}
```

**Status Codes:**
- `200` - Success
- `404` - Swatch not found

---

## Export

### POST /export/png

Export high-resolution rendered image.

**Request:**

```bash
curl -X POST http://localhost:8000/api/export/png \
  -H "Content-Type: application/json" \
  -d '{
    "render_id": "ren_001",
    "watermark": false
  }' \
  --output result.png
```

**Request Body:**

```json
{
  "render_id": "string (required)",
  "watermark": false,           // Add company watermark
  "format": "png",              // png or jpg
  "quality": 95                 // JPG quality 1-100
}
```

**Response: 200 OK**

Binary image data (Content-Type: image/png or image/jpeg)

**Status Codes:**
- `200` - Success
- `404` - Render ID not found

---

### POST /export/pdf

Generate consultation PDF.

**Request:**

```bash
curl -X POST http://localhost:8000/api/export/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "render_id": "ren_001",
    "customer": {
      "name": "Jane Smith",
      "address": "123 Main St",
      "phone": "555-1234"
    },
    "sales_rep": {
      "name": "John Doe",
      "email": "john@company.com"
    },
    "notes": "Follow-up scheduled for Friday"
  }' \
  --output consultation.pdf
```

**Request Body:**

```json
{
  "render_id": "string (required)",
  "customer": {
    "name": "string",
    "address": "string (optional)",
    "phone": "string (optional)",
    "email": "string (optional)"
  },
  "sales_rep": {
    "name": "string",
    "email": "string (optional)",
    "phone": "string (optional)"
  },
  "notes": "string (optional)",
  "include_pricing": false,     // Include estimated pricing
  "logo_url": "/images/logo.png"
}
```

**Response: 200 OK**

Binary PDF data (Content-Type: application/pdf)

**PDF Contents:**
- Company logo header
- Customer information
- Before/After images side-by-side
- Treatment details (type, vendor, material, color, SKU)
- Sales rep contact information
- Consultation date
- Notes section

**Status Codes:**
- `200` - Success
- `404` - Render ID not found
- `500` - PDF generation failed

---

## Admin

### POST /admin/swatches

Add new swatch (admin only).

**Request:**

```bash
curl -X POST http://localhost:8000/api/admin/swatches \
  -F "texture=@/path/to/fabric.jpg" \
  -F 'metadata={
    "vendor_id": 5,
    "treatment_type": "curtains",
    "material": "100% Linen",
    "color": "Natural Beige",
    "opacity": 0.9,
    "price_tier": "mid-range",
    "sku": "ACME-LIN-NB-001"
  }'
```

**Form Data:**
- `texture` (required) - Swatch image file
- `metadata` (required) - JSON metadata

**Response: 201 Created**

```json
{
  "swatch_id": 101,
  "message": "Swatch created successfully",
  "processing": {
    "seamless_texture": true,
    "normal_map": true,
    "thumbnails": true,
    "color_extraction": true
  }
}
```

**Status Codes:**
- `201` - Created
- `400` - Invalid metadata or image
- `401` - Unauthorized

---

### DELETE /admin/swatches/{id}

Archive swatch (soft delete).

**Request:**

```bash
curl -X DELETE http://localhost:8000/api/admin/swatches/101
```

**Response: 200 OK**

```json
{
  "message": "Swatch archived successfully",
  "swatch_id": 101
}
```

**Status Codes:**
- `200` - Success
- `404` - Swatch not found
- `401` - Unauthorized

---

## WebSocket

### WS /ws/progress

Real-time progress updates during rendering.

**Connect:**

```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws/progress');

ws.onopen = () => {
  // Send render request with job ID
  ws.send(JSON.stringify({
    action: 'subscribe',
    job_id: 'ren_001'
  }));
};

ws.onmessage = (event) => {
  const progress = JSON.parse(event.data);
  console.log(progress);
  // Update UI progress bar
};
```

**Progress Messages:**

```json
{
  "job_id": "ren_001",
  "stage": "detecting",
  "progress": 0.2,
  "message": "Detecting windows...",
  "time_elapsed": 1.85
}

{
  "job_id": "ren_001",
  "stage": "segmenting",
  "progress": 0.4,
  "message": "Segmenting window...",
  "time_elapsed": 3.95
}

{
  "job_id": "ren_001",
  "stage": "rendering",
  "progress": 0.8,
  "message": "Rendering treatment...",
  "time_elapsed": 6.2
}

{
  "job_id": "ren_001",
  "stage": "complete",
  "progress": 1.0,
  "message": "Complete!",
  "time_elapsed": 7.5,
  "result_url": "/results/ren_001.jpg"
}
```

**Stages:**
- `uploading` (0.0 - 0.1)
- `detecting` (0.1 - 0.3)
- `segmenting` (0.3 - 0.5)
- `depth` (0.5 - 0.6)
- `rendering` (0.6 - 0.95)
- `compositing` (0.95 - 1.0)
- `complete` (1.0)

**Error Message:**

```json
{
  "job_id": "ren_001",
  "stage": "error",
  "error": "segmentation_failed",
  "message": "Failed to segment window",
  "detail": "Mask quality too low"
}
```

---

## Error Codes

All error responses follow this format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "detail": "Additional context (optional)",
  "timestamp": "2026-02-16T14:30:00Z"
}
```

**Common Error Codes:**

| Code | Description |
|------|-------------|
| `invalid_format` | Unsupported file format |
| `file_too_large` | File exceeds size limit |
| `image_not_found` | Image ID doesn't exist |
| `detection_failed` | Window detection error |
| `segmentation_failed` | Segmentation error |
| `rendering_failed` | Rendering pipeline error |
| `swatch_not_found` | Swatch ID doesn't exist |
| `validation_error` | Request validation failed |
| `server_error` | Internal server error |
| `gpu_error` | CUDA/GPU error |
| `out_of_memory` | VRAM exhausted |

---

## Rate Limiting

No rate limiting in MVP. Can be added in production.

---

## Versioning

API version included in URL: `/api/v1/...`

Current version: `v1` (implicit)

---

## CORS

Configured to allow:
- `http://localhost:3000` (frontend)
- `http://localhost:7860` (Gradio prototype)

Can be configured in `.env`:

```bash
CORS_ORIGINS=http://localhost:3000,http://localhost:7860
```

---

## Client SDKs

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Upload image
with open("room.jpg", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/upload",
        files={"file": f}
    )
    image_id = response.json()["image_id"]

# Detect windows
response = requests.post(
    f"{BASE_URL}/detect",
    json={"image_id": image_id}
)
detections = response.json()["detections"]

# Segment first window
bbox = detections[0]["bbox"]
response = requests.post(
    f"{BASE_URL}/segment",
    json={"image_id": image_id, "bbox": bbox}
)
seg_id = response.json()["segmentation_id"]

# Render with swatch
response = requests.post(
    f"{BASE_URL}/render",
    json={
        "image_id": image_id,
        "segmentation_id": seg_id,
        "treatment": {
            "type": "curtains",
            "swatch_id": 42
        }
    }
)
result_url = response.json()["result_url"]
print(f"Result: {BASE_URL}{result_url}")
```

### JavaScript Example

```javascript
const BASE_URL = 'http://localhost:8000/api';

// Upload image
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResp = await fetch(`${BASE_URL}/upload`, {
  method: 'POST',
  body: formData
});
const { image_id } = await uploadResp.json();

// Detect windows
const detectResp = await fetch(`${BASE_URL}/detect`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ image_id })
});
const { detections } = await detectResp.json();

// Render treatment
const renderResp = await fetch(`${BASE_URL}/render`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    image_id,
    segmentation_id: 'seg_001',
    treatment: {
      type: 'curtains',
      swatch_id: 42
    }
  })
});
const { result_url } = await renderResp.json();
console.log(`Result: ${BASE_URL}${result_url}`);
```

---

**API Documentation Version:** 1.0  
**Last Updated:** February 16, 2026  
**Contact:** support@yourcompany.com
