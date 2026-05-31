"""
Image Processing Utilities for OceanGuard Backend
"""

import io
from typing import Tuple

import cv2
import numpy as np
from PIL import Image


def validate_image(image_bytes: bytes) -> bool:
    """Check if bytes represent a valid image"""
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img is not None
    except Exception:
        return False


def get_image_dimensions(image_bytes: bytes) -> Tuple[int, int]:
    """Get image width and height from bytes"""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image")
    h, w = img.shape[:2]
    return w, h


def resize_image(
    image_bytes: bytes,
    max_size: int = 1280,
    quality: int = 90,
) -> bytes:
    """
    Resize image if it exceeds max_size while maintaining aspect ratio.
    Returns JPEG bytes.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image")

    h, w = img.shape[:2]
    if max(h, w) <= max_size:
        return image_bytes

    ratio = max_size / max(h, w)
    new_w, new_h = int(w * ratio), int(h * ratio)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    success, buffer = cv2.imencode(".jpg", resized, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not success:
        raise ValueError("Failed to encode image")
    return buffer.tobytes()


def apply_underwater_enhancement(image_bytes: bytes) -> bytes:
    """
    Apply underwater image enhancement to improve visibility.
    Uses CLAHE (Contrast Limited Adaptive Histogram Equalization).
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image")

    # Convert to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_l = clahe.apply(l)

    # Merge channels and convert back
    enhanced_lab = cv2.merge([enhanced_l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # Slight color correction for underwater blue/green tint
    enhanced = cv2.addWeighted(enhanced, 1.2, np.zeros_like(enhanced), 0, 10)

    success, buffer = cv2.imencode(".jpg", enhanced, [cv2.IMWRITE_JPEG_QUALITY, 90])
    if not success:
        raise ValueError("Failed to encode enhanced image")
    return buffer.tobytes()
