"""
Check Class Order from Trained Model
Run this in Google Colab to get the correct class order
"""

from ultralytics import YOLO
import yaml
import os

print("🔍 CHECKING CLASS ORDER FROM MODEL...\n")

# Auto-detect model path
if os.path.exists('ocean_trash/ultimate_yolov8n/weights/best.pt'):
    model_path = 'ocean_trash/ultimate_yolov8n/weights/best.pt'
    project_path = 'ocean_trash/ultimate_yolov8n'
elif os.path.exists('ocean_trash/ultimate_yolov11n/weights/best.pt'):
    model_path = 'ocean_trash/ultimate_yolov11n/weights/best.pt'
    project_path = 'ocean_trash/ultimate_yolov11n'
else:
    print("❌ Model not found!")
    exit()

print(f"✅ Found model: {model_path}\n")

# Load model
model = YOLO(model_path)

# Print class names from model
print("="*60)
print("📊 CLASS ORDER IN TRAINED MODEL:")
print("="*60)
for idx, name in model.names.items():
    print(f"  {idx}: {name}")
print("="*60)

# Also check from data.yaml
print("\n📊 CLASS ORDER IN data.yaml:")
print("="*60)
try:
    # Try to find data.yaml
    yaml_paths = [
        f'{dataset.location}/data.yaml',
        'data.yaml',
    ]
    
    yaml_path = None
    for path in yaml_paths:
        if os.path.exists(path):
            yaml_path = path
            break
    
    if yaml_path:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
            for idx, name in enumerate(data['names']):
                print(f"  {idx}: {name}")
    else:
        print("  ⚠️ data.yaml not found")
except Exception as e:
    print(f"  ⚠️ Could not read data.yaml: {e}")
print("="*60)

# Generate Python code for detector.py
print("\n🔧 COPY THIS TO YOUR detector.py:")
print("="*60)
print("CLASS_NAMES = [")
for idx in sorted(model.names.keys()):
    name = model.names[idx]
    print(f'    "{name}",  # Index {idx}')
print("]")
print("="*60)

print("\n✅ Done! Copy the CLASS_NAMES list above to your detector.py")
