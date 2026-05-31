"""
Detection Router — API endpoints for marine debris detection
"""
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response

from ..services.detector import MarineDebrisDetector

router = APIRouter(prefix="/api/v1", tags=["detection"])

# Global detector instance
detector = MarineDebrisDetector()


@router.post("/detect")
async def detect_objects(file: UploadFile = File(...), confidence: float = 0.25):
    """Detect marine debris and return JSON results"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()
    start = time.time()

    try:
        if detector.model is None:
            # Demo mode — return sample data when no model is loaded
            return {
                "detections": [
                    {"class_name": "plastic", "confidence": 0.92, "bbox": {"x1": 100, "y1": 50, "x2": 300, "y2": 250}},
                    {"class_name": "bottle", "confidence": 0.87, "bbox": {"x1": 350, "y1": 100, "x2": 450, "y2": 350}},
                    {"class_name": "can", "confidence": 0.78, "bbox": {"x1": 500, "y1": 200, "x2": 600, "y2": 320}},
                ],
                "total_detections": 3,
                "inference_time_ms": 42.0,
                "mode": "demo",
            }

        result = detector.detect(image_bytes, confidence=confidence)
        elapsed = (time.time() - start) * 1000

        # Remap keys for frontend compatibility
        detections = []
        for d in result.get("detections", []):
            detections.append({
                "class_name": d["class"],
                "confidence": d["confidence"],
                "bbox": d["bbox"],
            })

        return {
            "detections": detections,
            "total_detections": result["total_detections"],
            "inference_time_ms": round(elapsed, 1),
            "image_width": result["image_width"],
            "image_height": result["image_height"],
            "statistics": result["statistics"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect/annotated")
async def detect_annotated(file: UploadFile = File(...), confidence: float = 0.25):
    """Detect and return annotated image with bounding boxes"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()

    try:
        if detector.model is None:
            # Demo mode — return original image
            return Response(content=image_bytes, media_type="image/jpeg")

        annotated = detector.detect_and_annotate(image_bytes, confidence=confidence)
        return Response(content=annotated, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
