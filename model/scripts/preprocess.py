"""
Dataset Preprocessing Script for Marine Debris Detection
OceanGuard Project - Pengolahan Citra Digital

This script handles:
1. Downloading dataset from Kaggle
2. Converting annotations to YOLO format
3. Splitting dataset into train/val/test
4. Image resizing and normalization

Usage:
    python preprocess.py --source kaggle    # Download from Kaggle
    python preprocess.py --source local     # Use local dataset
"""

import argparse
import os
import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(
        description="Preprocess marine debris dataset for YOLOv8"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="local",
        choices=["kaggle", "roboflow", "local"],
        help="Dataset source",
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default=None,
        help="Input directory containing raw images and annotations",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for processed dataset",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Target image size (default: 640)",
    )
    parser.add_argument(
        "--split",
        type=str,
        default="0.7,0.15,0.15",
        help="Train/Val/Test split ratio (default: 0.7,0.15,0.15)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    return parser.parse_args()


def download_kaggle_dataset(output_dir: Path):
    """
    Download TrashCan dataset from Kaggle.
    Requires kaggle API key (~/.kaggle/kaggle.json)
    """
    try:
        import kaggle
    except ImportError:
        print("ERROR: kaggle package not installed.")
        print("Run: pip install kaggle")
        print("And setup API key: https://www.kaggle.com/docs/api")
        return False

    print("📥 Downloading TrashCan 1.0 dataset from Kaggle...")
    kaggle.api.dataset_download_files(
        "haaborrescience/trashcan10",
        path=str(output_dir),
        unzip=True,
    )
    print(f"✅ Dataset downloaded to: {output_dir}")
    return True


def coco_to_yolo(
    bbox: List[float],
    img_width: int,
    img_height: int,
) -> Tuple[float, float, float, float]:
    """
    Convert COCO bbox format [x, y, width, height] to YOLO format
    [x_center, y_center, width, height] (normalized 0-1)
    """
    x, y, w, h = bbox
    x_center = (x + w / 2) / img_width
    y_center = (y + h / 2) / img_height
    w_norm = w / img_width
    h_norm = h / img_height

    # Clamp values to [0, 1]
    x_center = max(0, min(1, x_center))
    y_center = max(0, min(1, y_center))
    w_norm = max(0, min(1, w_norm))
    h_norm = max(0, min(1, h_norm))

    return x_center, y_center, w_norm, h_norm


def convert_coco_to_yolo(coco_json_path: str, output_dir: Path, images_dir: Path):
    """
    Convert COCO format annotations to YOLO format.
    Creates individual .txt label files for each image.
    """
    print(f"🔄 Converting COCO annotations to YOLO format...")

    with open(coco_json_path, "r") as f:
        coco_data = json.load(f)

    # Build category mapping
    categories = {cat["id"]: cat["name"] for cat in coco_data["categories"]}
    
    # Map original categories to our 6 classes
    CATEGORY_MAP = {
        # Plastic
        "plastic": 0, "wrapper": 0, "plastic_bag": 0, "packaging": 0,
        # Bottle
        "bottle": 1, "glass_bottle": 1, "plastic_bottle": 1,
        # Can
        "can": 2, "metal_can": 2, "aluminum": 2,
        # Net/Rope
        "net": 3, "rope": 3, "fishing_net": 3, "fishing_line": 3, "line": 3,
        # Bag
        "bag": 4, "shopping_bag": 4,
        # Others
        "other": 5, "styrofoam": 5, "rubber": 5, "cloth": 5, "shoe": 5,
        "tire": 5, "paper": 5, "cardboard": 5, "wood": 5,
    }

    # Build image ID to info mapping
    images_info = {img["id"]: img for img in coco_data["images"]}

    # Group annotations by image
    annotations_by_image = {}
    for ann in coco_data["annotations"]:
        img_id = ann["image_id"]
        if img_id not in annotations_by_image:
            annotations_by_image[img_id] = []
        annotations_by_image[img_id].append(ann)

    labels_dir = output_dir / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0

    for img_id, img_info in images_info.items():
        filename = img_info["file_name"]
        img_w = img_info["width"]
        img_h = img_info["height"]

        # Get base name without extension for label file
        label_name = Path(filename).stem + ".txt"
        label_path = labels_dir / label_name

        annotations = annotations_by_image.get(img_id, [])

        yolo_lines = []
        for ann in annotations:
            cat_name = categories.get(ann["category_id"], "other").lower()
            
            # Map to our class IDs
            class_id = None
            for key, cid in CATEGORY_MAP.items():
                if key in cat_name:
                    class_id = cid
                    break
            
            if class_id is None:
                class_id = 5  # Default to "others"

            bbox = ann["bbox"]  # COCO format: [x, y, w, h]
            x_c, y_c, w_n, h_n = coco_to_yolo(bbox, img_w, img_h)

            yolo_lines.append(f"{class_id} {x_c:.6f} {y_c:.6f} {w_n:.6f} {h_n:.6f}")

        # Write label file
        with open(label_path, "w") as f:
            f.write("\n".join(yolo_lines))

        converted += 1

    print(f"✅ Converted {converted} label files to YOLO format")
    print(f"   Saved to: {labels_dir}")


def split_dataset(
    images_dir: Path,
    labels_dir: Path,
    output_dir: Path,
    split_ratios: Tuple[float, float, float] = (0.7, 0.15, 0.15),
    seed: int = 42,
):
    """
    Split dataset into train/val/test sets.
    """
    print(f"\n📂 Splitting dataset (train={split_ratios[0]}, val={split_ratios[1]}, test={split_ratios[2]})...")

    random.seed(seed)

    # Get all image files
    image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    image_files = [
        f for f in images_dir.iterdir()
        if f.suffix.lower() in image_extensions
    ]
    random.shuffle(image_files)

    total = len(image_files)
    train_end = int(total * split_ratios[0])
    val_end = train_end + int(total * split_ratios[1])

    splits = {
        "train": image_files[:train_end],
        "val": image_files[train_end:val_end],
        "test": image_files[val_end:],
    }

    for split_name, files in splits.items():
        split_img_dir = output_dir / split_name / "images"
        split_lbl_dir = output_dir / split_name / "labels"
        split_img_dir.mkdir(parents=True, exist_ok=True)
        split_lbl_dir.mkdir(parents=True, exist_ok=True)

        for img_file in files:
            # Copy image
            shutil.copy2(img_file, split_img_dir / img_file.name)

            # Copy corresponding label
            label_file = labels_dir / (img_file.stem + ".txt")
            if label_file.exists():
                shutil.copy2(label_file, split_lbl_dir / label_file.name)

        print(f"   {split_name}: {len(files)} images")

    print(f"✅ Dataset split complete → {output_dir}")


def resize_images(images_dir: Path, target_size: int = 640):
    """Resize all images to target size while maintaining aspect ratio"""
    print(f"\n📐 Resizing images to {target_size}x{target_size}...")

    image_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    count = 0

    for img_path in images_dir.rglob("*"):
        if img_path.suffix.lower() not in image_extensions:
            continue

        img = cv2.imread(str(img_path))
        if img is None:
            continue

        h, w = img.shape[:2]
        if h == target_size and w == target_size:
            continue

        # Resize with letterboxing
        ratio = min(target_size / h, target_size / w)
        new_h, new_w = int(h * ratio), int(w * ratio)
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

        # Create canvas
        canvas = np.full((target_size, target_size, 3), 114, dtype=np.uint8)
        top = (target_size - new_h) // 2
        left = (target_size - new_w) // 2
        canvas[top : top + new_h, left : left + new_w] = resized

        cv2.imwrite(str(img_path), canvas)
        count += 1

    print(f"✅ Resized {count} images")


def main():
    args = parse_args()

    project_root = Path(__file__).parent.parent
    input_dir = Path(args.input_dir) if args.input_dir else project_root / "data" / "raw"
    output_dir = Path(args.output_dir) if args.output_dir else project_root / "data"

    print("=" * 60)
    print("🌊 OceanGuard - Dataset Preprocessing")
    print("=" * 60)

    # Step 1: Download if needed
    if args.source == "kaggle":
        raw_dir = project_root / "data" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        download_kaggle_dataset(raw_dir)
        input_dir = raw_dir

    # Step 2: Convert annotations (if COCO format exists)
    coco_json = input_dir / "annotations.json"
    if coco_json.exists():
        convert_coco_to_yolo(
            str(coco_json),
            output_dir,
            input_dir / "images",
        )

    # Step 3: Split dataset
    images_dir = input_dir / "images" if (input_dir / "images").exists() else input_dir
    labels_dir = output_dir / "labels" if (output_dir / "labels").exists() else input_dir / "labels"

    if images_dir.exists() and labels_dir.exists():
        split_ratios = tuple(float(x) for x in args.split.split(","))
        split_dataset(images_dir, labels_dir, output_dir, split_ratios, args.seed)

        # Step 4: Resize images
        resize_images(output_dir, args.imgsz)
    else:
        print(f"\n⚠️  Could not find images or labels directory.")
        print(f"   Images dir: {images_dir}")
        print(f"   Labels dir: {labels_dir}")
        print(f"\n   Please ensure your raw dataset is in: {input_dir}")
        print(f"   With 'images/' and 'labels/' (or 'annotations.json') subdirectories.")

    print(f"\n🎉 Preprocessing complete!")


if __name__ == "__main__":
    main()
