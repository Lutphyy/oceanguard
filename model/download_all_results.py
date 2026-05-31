"""
Auto-Download All Training Results from Google Colab
Run this in a new cell in your Colab notebook
"""

from google.colab import files
import os
import shutil

print("="*60)
print("📥 OCEANGUARD - AUTO DOWNLOAD TRAINING RESULTS")
print("="*60)
print()

# Auto-detect project path
if os.path.exists('/content/ocean_trash/ultimate_yolov8n'):
    project_path = '/content/ocean_trash/ultimate_yolov8n'
elif os.path.exists('/content/ocean_trash/ultimate_yolov11n'):
    project_path = '/content/ocean_trash/ultimate_yolov11n'
else:
    print("❌ ERROR: Training results not found!")
    print("   Expected: /content/ocean_trash/ultimate_yolov8n")
    exit()

print(f"✅ Found training results: {project_path}\n")

# List of files to download
files_to_download = {
    "🎯 Model Weights (CRITICAL!)": [
        f'{project_path}/weights/best.pt',
    ],
    "📊 Training Results & Plots": [
        f'{project_path}/results.png',
        f'{project_path}/confusion_matrix.png',
        f'{project_path}/confusion_matrix_normalized.png',
    ],
    "📈 Metrics & Logs": [
        f'{project_path}/results.csv',
        f'{project_path}/args.yaml',
    ],
    "🖼️  Training Samples": [
        f'{project_path}/train_batch0.jpg',
        f'{project_path}/train_batch1.jpg',
        f'{project_path}/train_batch2.jpg',
    ],
    "🔍 Validation Predictions": [
        f'{project_path}/val_batch0_pred.jpg',
        f'{project_path}/val_batch1_pred.jpg',
    ],
    "📋 Labels Distribution": [
        f'{project_path}/labels.jpg',
    ],
}

# Download files
total_files = sum(len(files) for files in files_to_download.values())
downloaded = 0
missing = 0

for category, file_list in files_to_download.items():
    print(f"\n{category}")
    print("-" * 60)
    
    for file_path in file_list:
        filename = os.path.basename(file_path)
        
        if os.path.exists(file_path):
            print(f"  📥 Downloading: {filename}")
            try:
                files.download(file_path)
                downloaded += 1
                print(f"     ✅ Success!")
            except Exception as e:
                print(f"     ❌ Failed: {e}")
        else:
            print(f"  ⚠️  Not found: {filename}")
            missing += 1

print("\n" + "="*60)
print("📊 DOWNLOAD SUMMARY")
print("="*60)
print(f"✅ Downloaded: {downloaded}/{total_files} files")
if missing > 0:
    print(f"⚠️  Missing: {missing}/{total_files} files")
print()
print("📁 Files saved to your Downloads folder")
print()
print("🚀 NEXT STEPS:")
print("  1. Copy best.pt to: model/weights/best.pt")
print("  2. Copy plots to: docs/images/ (for report)")
print("  3. Test model in your application")
print("  4. Backup to Google Drive (recommended)")
print()
print("="*60)
print("✅ DOWNLOAD COMPLETE!")
print("="*60)
