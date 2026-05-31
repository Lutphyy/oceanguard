"""
Model Evaluation Script for Marine Debris Detection
OceanGuard Project - Pengolahan Citra Digital

Usage:
    python evaluate.py                              # Evaluate best.pt on test set
    python evaluate.py --model ../weights/best.pt   # Specific model
    python evaluate.py --visualize                  # Show detection visualizations
"""

import argparse
import os
from pathlib import Path

import cv2
import numpy as np
import matplotlib.pyplot as plt

try:
    from ultralytics import YOLO
except ImportError:
    print("ERROR: ultralytics not installed. Run: pip install ultralytics")
    exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Evaluate YOLOv8 model for marine debris detection"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to model weights (.pt file)",
    )
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Path to dataset YAML config",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Image size (default: 640)",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=16,
        help="Batch size (default: 16)",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold (default: 0.25)",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Generate and save detection visualizations",
    )
    parser.add_argument(
        "--num-vis",
        type=int,
        default=10,
        help="Number of images to visualize (default: 10)",
    )
    return parser.parse_args()


def plot_metrics(results_dir: Path, save_dir: Path):
    """
    Plot training metrics from results CSV.
    Generates publication-ready plots for the paper.
    """
    import pandas as pd

    results_csv = results_dir / "results.csv"
    if not results_csv.exists():
        print(f"⚠️  results.csv not found at {results_csv}")
        return

    df = pd.read_csv(results_csv)
    df.columns = df.columns.str.strip()

    save_dir.mkdir(parents=True, exist_ok=True)

    # Plot 1: Loss curves
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    loss_cols = {
        "train/box_loss": "Box Loss",
        "train/cls_loss": "Classification Loss",
        "train/dfl_loss": "DFL Loss",
    }

    for ax, (col, title) in zip(axes, loss_cols.items()):
        if col in df.columns:
            ax.plot(df["epoch"], df[col], "b-", linewidth=1.5, label="Train")
            val_col = col.replace("train/", "val/")
            if val_col in df.columns:
                ax.plot(df["epoch"], df[val_col], "r-", linewidth=1.5, label="Val")
            ax.set_xlabel("Epoch")
            ax.set_ylabel("Loss")
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_dir / "loss_curves.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   📊 Loss curves saved")

    # Plot 2: mAP curves
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    map_cols = [
        ("metrics/mAP50(B)", "mAP@50"),
        ("metrics/mAP50-95(B)", "mAP@50:95"),
    ]

    for ax, (col, title) in zip(axes, map_cols):
        if col in df.columns:
            ax.plot(df["epoch"], df[col], "g-", linewidth=2)
            ax.set_xlabel("Epoch")
            ax.set_ylabel(title)
            ax.set_title(f"{title} over Epochs")
            ax.grid(True, alpha=0.3)
            # Mark best epoch
            best_idx = df[col].idxmax()
            best_val = df[col].max()
            ax.axhline(y=best_val, color="r", linestyle="--", alpha=0.5)
            ax.annotate(
                f"Best: {best_val:.4f}",
                xy=(df["epoch"][best_idx], best_val),
                fontsize=9,
                color="red",
            )

    plt.tight_layout()
    plt.savefig(save_dir / "map_curves.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   📊 mAP curves saved")

    # Plot 3: Precision & Recall
    fig, ax = plt.subplots(figsize=(8, 4))
    
    if "metrics/precision(B)" in df.columns:
        ax.plot(df["epoch"], df["metrics/precision(B)"], "b-", linewidth=1.5, label="Precision")
    if "metrics/recall(B)" in df.columns:
        ax.plot(df["epoch"], df["metrics/recall(B)"], "r-", linewidth=1.5, label="Recall")
    
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Score")
    ax.set_title("Precision & Recall over Epochs")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_dir / "precision_recall.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"   📊 Precision/Recall curves saved")


def evaluate(args):
    """Main evaluation function"""

    print("=" * 60)
    print("🌊 OceanGuard - Model Evaluation")
    print("=" * 60)

    project_root = Path(__file__).parent.parent

    # Find model weights
    if args.model:
        model_path = args.model
    else:
        model_path = project_root / "weights" / "best.pt"
        if not model_path.exists():
            # Try to find in runs directory
            runs_dir = project_root / "runs"
            if runs_dir.exists():
                for run in sorted(runs_dir.iterdir(), reverse=True):
                    candidate = run / "weights" / "best.pt"
                    if candidate.exists():
                        model_path = candidate
                        break

    if not Path(model_path).exists():
        print(f"❌ Model not found: {model_path}")
        print("   Train a model first with: python train.py")
        return

    # Dataset config
    if args.data:
        data_yaml = args.data
    else:
        data_yaml = project_root / "data" / "dataset.yaml"
        if not data_yaml.exists():
            print(f"❌ Dataset config not found: {data_yaml}")
            return

    print(f"\n📋 Evaluation Configuration:")
    print(f"   Model:      {model_path}")
    print(f"   Dataset:    {data_yaml}")
    print(f"   Image Size: {args.imgsz}")
    print(f"   Confidence: {args.conf}")

    # Load model
    model = YOLO(str(model_path))

    # Run validation
    print(f"\n🔍 Running evaluation on test set...")
    results = model.val(
        data=str(data_yaml),
        imgsz=args.imgsz,
        batch=args.batch,
        conf=args.conf,
        split="test",
        plots=True,
        verbose=True,
    )

    # Print results summary
    print(f"\n{'='*60}")
    print(f"📊 EVALUATION RESULTS")
    print(f"{'='*60}")
    print(f"   mAP@50:      {results.box.map50:.4f}")
    print(f"   mAP@50:95:   {results.box.map:.4f}")
    print(f"   Precision:   {results.box.mp:.4f}")
    print(f"   Recall:      {results.box.mr:.4f}")
    print(f"{'='*60}")

    # Per-class results
    class_names = ["plastic", "bottle", "can", "net_rope", "bag", "others"]
    print(f"\n📋 Per-Class Results:")
    print(f"{'Class':<15} {'Precision':<12} {'Recall':<12} {'mAP@50':<12} {'mAP@50:95':<12}")
    print("-" * 63)

    for i, name in enumerate(class_names):
        if i < len(results.box.ap50):
            print(
                f"{name:<15} "
                f"{results.box.p[i]:.4f}       "
                f"{results.box.r[i]:.4f}       "
                f"{results.box.ap50[i]:.4f}       "
                f"{results.box.ap[i]:.4f}"
            )

    # Save evaluation report
    eval_dir = project_root / "evaluation"
    eval_dir.mkdir(exist_ok=True)

    report_path = eval_dir / "evaluation_report.txt"
    with open(report_path, "w") as f:
        f.write("OceanGuard - Model Evaluation Report\n")
        f.write(f"Model: {model_path}\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"mAP@50:    {results.box.map50:.4f}\n")
        f.write(f"mAP@50:95: {results.box.map:.4f}\n")
        f.write(f"Precision: {results.box.mp:.4f}\n")
        f.write(f"Recall:    {results.box.mr:.4f}\n")

    print(f"\n✅ Report saved to: {report_path}")

    # Generate plots
    print(f"\n📈 Generating metric plots...")
    # Find the latest run directory for plotting
    runs_dir = project_root / "runs"
    if runs_dir.exists():
        for run in sorted(runs_dir.iterdir(), reverse=True):
            if (run / "results.csv").exists():
                plot_metrics(run, eval_dir)
                break

    print(f"\n🎉 Evaluation complete!")


if __name__ == "__main__":
    args = parse_args()
    evaluate(args)
