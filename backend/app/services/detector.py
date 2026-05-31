"""
Marine Debris Detector Service
Handles YOLOv8 model loading and inference for underwater trash detection
"""

import io
import os
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from PIL import Image

# Try to import ultralytics, gracefully handle if not installed
try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None
    print("WARNING: ultralytics not installed. Run: pip install ultralytics")


class MarineDebrisDetector:
    """
    YOLOv8-based marine debris detector.
    Loads a fine-tuned YOLOv8 model and provides inference methods.
    """

    # Class labels for marine debris categories
    # These must match the order in data.yaml from your trained model
    CLASS_NAMES = [
         "bottle",  # Index 0
    "can",  # Index 1
    "electronics",  # Index 2
    "net_rope",  # Index 3
    "other",  # Index 4
    "plastic",  # Index 5
    ]

    # Colors for bounding boxes (BGR format for OpenCV)
    CLASS_COLORS = {
        "plastic": (0, 165, 255),     # Orange
        "bottle": (255, 0, 0),        # Blue
        "can": (0, 255, 0),           # Green
        "net_rope": (0, 0, 255),      # Red
        "other": (128, 0, 128),       # Purple
        "electronics": (255, 0, 255), # Magenta
    }

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the detector with a YOLOv8 model.
        
        Args:
            model_path: Path to the trained YOLOv8 .pt weights file.
                        If None, looks for weights in the default location.
        """
        self.model = None
        self.model_path = model_path

        if YOLO is None:
            print("ERROR: ultralytics package not available.")
            return

        # Determine model path
        if model_path is None:
            # Look for weights in the default directory
            weights_dir = Path(__file__).parent.parent.parent.parent / "model" / "weights"
            candidates = [
                weights_dir / "best.pt",           # Custom trained
                weights_dir / "yolov8n.pt",        # Pretrained nano
                weights_dir / "yolov8s.pt",        # Pretrained small
            ]
            for candidate in candidates:
                if candidate.exists():
                    model_path = str(candidate)
                    break

        if model_path and os.path.exists(model_path):
            try:
                self.model = YOLO(model_path)
                print(f"✅ Model loaded successfully from: {model_path}")
            except Exception as e:
                print(f"❌ Failed to load model: {e}")
        else:
            print(f"⚠️  No model weights found. Please train the model first.")
            print(f"   Expected location: model/weights/best.pt")
            print(f"   Or download pretrained: yolov8n.pt")

    def _bytes_to_image(self, image_bytes: bytes) -> np.ndarray:
        """Convert image bytes to OpenCV numpy array (BGR)"""
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Failed to decode image. Ensure the file is a valid image.")
        return image

    def _image_to_bytes(self, image: np.ndarray, quality: int = 90) -> bytes:
        """Convert OpenCV image (BGR) to JPEG bytes"""
        success, buffer = cv2.imencode(
            ".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality]
        )
        if not success:
            raise ValueError("Failed to encode image to JPEG.")
        return buffer.tobytes()

    def detect(
        self,
        image_bytes: bytes,
        confidence: float = 0.25,
        iou_threshold: float = 0.45,
    ) -> dict:
        """
        Run object detection on an image.
        
        Args:
            image_bytes: Raw image bytes
            confidence: Minimum confidence threshold
            iou_threshold: IoU threshold for NMS
            
        Returns:
            Dictionary with detection results:
            - detections: list of {class, confidence, bbox}
            - statistics: count per class
            - image dimensions
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Please provide model weights.")

        # Decode image
        image = self._bytes_to_image(image_bytes)
        h, w = image.shape[:2]

        # Run inference
        results = self.model.predict(
            source=image,
            conf=confidence,
            iou=iou_threshold,
            verbose=False,
        )

        # Parse results
        detections = []
        class_counts = {}

        if results and len(results) > 0:
            result = results[0]
            if result.boxes is not None:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    # Get class name
                    if cls_id < len(self.CLASS_NAMES):
                        class_name = self.CLASS_NAMES[cls_id]
                    else:
                        class_name = result.names.get(cls_id, f"class_{cls_id}")

                    detection = {
                        "class": class_name,
                        "confidence": round(conf, 4),
                        "bbox": {
                            "x1": round(x1, 2),
                            "y1": round(y1, 2),
                            "x2": round(x2, 2),
                            "y2": round(y2, 2),
                        },
                    }
                    detections.append(detection)

                    # Count per class
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1

        return {
            "image_width": w,
            "image_height": h,
            "total_detections": len(detections),
            "detections": detections,
            "statistics": class_counts,
        }

    def detect_and_annotate(
        self,
        image_bytes: bytes,
        confidence: float = 0.25,
        iou_threshold: float = 0.45,
    ) -> bytes:
        """
        Run detection and return annotated image with bounding boxes drawn.
        
        Args:
            image_bytes: Raw image bytes
            confidence: Minimum confidence threshold
            iou_threshold: IoU threshold for NMS
            
        Returns:
            JPEG bytes of the annotated image
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Please provide model weights.")

        image = self._bytes_to_image(image_bytes)

        # Run inference
        results = self.model.predict(
            source=image,
            conf=confidence,
            iou=iou_threshold,
            verbose=False,
        )

        # Draw bounding boxes
        if results and len(results) > 0:
            result = results[0]
            if result.boxes is not None:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                    # Get class name and color
                    if cls_id < len(self.CLASS_NAMES):
                        class_name = self.CLASS_NAMES[cls_id]
                    else:
                        class_name = result.names.get(cls_id, f"class_{cls_id}")

                    color = self.CLASS_COLORS.get(class_name, (255, 255, 255))

                    # Draw bounding box
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

                    # Draw label background
                    label = f"{class_name} {conf:.2f}"
                    (label_w, label_h), baseline = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1
                    )
                    cv2.rectangle(
                        image,
                        (x1, y1 - label_h - baseline - 5),
                        (x1 + label_w, y1),
                        color,
                        -1,
                    )

                    # Draw label text
                    cv2.putText(
                        image,
                        label,
                        (x1, y1 - baseline - 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA,
                    )

        return self._image_to_bytes(image)
