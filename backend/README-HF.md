---
title: OceanGuard API
emoji: 🌊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# 🌊 OceanGuard API

**Marine Debris Detection API powered by YOLOv8**

This is the backend API for OceanGuard - an underwater trash detection system using YOLOv8.

## 🚀 API Endpoints

### `POST /api/v1/detect`
Detect marine debris and return JSON results.

**Parameters:**
- `file`: Image file (JPG, PNG, WebP)
- `confidence`: Confidence threshold (0.1-0.9, default: 0.25)

**Response:**
```json
{
  "detections": [
    {
      "class_name": "plastic",
      "confidence": 0.92,
      "bbox": {"x1": 100, "y1": 50, "x2": 300, "y2": 250}
    }
  ],
  "total_detections": 3,
  "inference_time_ms": 42.0
}
```

### `POST /api/v1/detect/annotated`
Detect and return annotated image with bounding boxes.

**Parameters:**
- `file`: Image file (JPG, PNG, WebP)
- `confidence`: Confidence threshold (0.1-0.9, default: 0.25)

**Response:** Image file (JPEG) with bounding boxes

## 📊 Model Info

- **Model**: YOLOv8 Nano
- **Classes**: 6 (plastic, bottle, can, net_rope, other, electronics)
- **Input size**: 640x640
- **Framework**: Ultralytics YOLOv8

## 🔗 Frontend

The frontend Next.js application is deployed separately on Vercel.

## 📝 License

MIT License - Made with ❤️ for Ocean Conservation
