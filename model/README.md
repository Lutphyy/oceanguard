# 🌊 OceanGuard - Model Training

**YOLOv11 Model untuk Underwater Trash Detection**

---

## 📁 FOLDER STRUCTURE

```
model/
├── weights/                    # Model weights (deploy here!)
│   └── best.pt                # Trained model (download from Colab)
├── data/                      # Dataset (optional, for local training)
│   ├── train/
│   ├── valid/
│   ├── test/
│   └── data.yaml
├── roboflow_colab_training.ipynb  # ⭐ MAIN NOTEBOOK (use this!)
├── oceanguard_colab_training.ipynb # Old notebook (legacy)
├── ULTIMATE_TRAINING_GUIDE.md     # 📖 Complete guide (read this!)
├── QUICK_START_CHEATSHEET.md      # ⚡ Quick reference
├── DATASET_STRATEGY.md            # Dataset strategy notes
├── colab_training_guide.md        # Training guide
└── README.md                      # This file
```

---

## 🚀 QUICK START

### Option 1: Train di Google Colab (RECOMMENDED) ⭐

**File:** `roboflow_colab_training.ipynb`

**Steps:**
1. Export dataset dari Roboflow
2. Upload notebook ke Colab
3. Aktifkan GPU (T4)
4. Run cells (1-2 hours)
5. Download best.pt
6. Deploy!

**Guide:** Read `ULTIMATE_TRAINING_GUIDE.md`

**Time:** ~2 hours
**Cost:** FREE
**Expected mAP:** 82-85%

---

### Option 2: Use Pretrained Model

**Kalau gak mau train sendiri:**

1. Download pretrained YOLOv11:
   ```bash
   curl -L https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov11n.pt -o weights/yolov11n.pt
   ```

2. Or use Roboflow hosted API (temporary)

**Note:** Pretrained model gak spesifik untuk underwater trash!

---

## 📊 MODEL SPECS

### Current Model (Trained)

```
Architecture: YOLOv11 Nano
Pretrained: MS COCO
Classes: 6
  - plastic
  - bottle
  - can
  - net_rope
  - other
  - electronics

Performance:
  mAP@50:     81.6-85%
  Precision:  84.6-87%
  Recall:     74.3-80%
  F1 Score:   79.1-83%

Size: ~6-10 MB
Speed: 50-100 FPS (GPU), 10-30 FPS (CPU)
```

---

## 📖 DOCUMENTATION

### Training Guides

1. **ULTIMATE_TRAINING_GUIDE.md** ⭐
   - Complete step-by-step guide
   - Troubleshooting
   - FAQ
   - Best practices

2. **QUICK_START_CHEATSHEET.md** ⚡
   - Quick reference
   - Commands
   - Common errors

3. **DATASET_STRATEGY.md**
   - Dataset strategy
   - Class mapping
   - Data sources

---

## 🔧 REQUIREMENTS

### For Training (Colab)
- Google account
- Internet connection
- 2 hours time
- Roboflow account (free)

### For Inference (Local)
- Python 3.10+
- ultralytics==8.3.0
- torch>=2.0.0
- opencv-python-headless
- See: `backend/requirements.txt`

---

## 🎯 USAGE

### Load Model

```python
from ultralytics import YOLO

# Load trained model
model = YOLO('model/weights/best.pt')

# Inference
results = model.predict('image.jpg', conf=0.4)

# Get detections
for result in results:
    boxes = result.boxes
    for box in boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        xyxy = box.xyxy[0].tolist()
        print(f"Class: {cls}, Confidence: {conf:.2f}, Box: {xyxy}")
```

### API Endpoint

```bash
# Start backend
cd backend
python -m uvicorn app.main:app --reload

# Test detection
curl -X POST "http://localhost:8000/api/detect" \
  -F "file=@image.jpg"
```

---

## 📈 TRAINING RESULTS

### Expected Metrics

```
Training Configuration:
  Epochs: 200 (with early stopping)
  Batch: 16
  Image size: 640x640
  Augmentation: Strong (mosaic, mixup, rotation, flip)
  Optimizer: AdamW
  Learning rate: 0.001 → 0.00001

Results:
  mAP@50:     82-85%  (vs Roboflow 81.6%)
  Precision:  84-87%  (vs Roboflow 84.6%)
  Recall:     76-80%  (vs Roboflow 74.3%)
  F1 Score:   80-83%  (vs Roboflow 79.1%)

Training time: 30-90 minutes (Google Colab T4 GPU)
```

---

## 🔄 RETRAINING

### When to Retrain

- Add more data (new images)
- Add new classes
- Improve accuracy
- Fix misclassifications

### How to Retrain

1. Update dataset di Roboflow
2. Export new version
3. Run `roboflow_colab_training.ipynb` again
4. Download new best.pt
5. Replace old weights

---

## 🐛 TROUBLESHOOTING

### Model not loading

```python
# Check file exists
import os
print(os.path.exists('model/weights/best.pt'))

# Check file size
print(os.path.getsize('model/weights/best.pt'))
# Should be ~6-10 MB
```

### Low accuracy

- Check confidence threshold (try 0.3-0.5)
- Check image quality (blur, lighting)
- Retrain with more data
- Use bigger model (YOLOv11 Small)

### Slow inference

- Use GPU (if available)
- Reduce image size
- Use smaller model (Nano)
- Batch processing

---

## 📚 RESOURCES

### Documentation
- Ultralytics: https://docs.ultralytics.com/
- Roboflow: https://docs.roboflow.com/
- YOLOv11: https://docs.ultralytics.com/models/yolo11/

### Tutorials
- Training: `ULTIMATE_TRAINING_GUIDE.md`
- Quick start: `QUICK_START_CHEATSHEET.md`
- Dataset: `DATASET_STRATEGY.md`

---

## 📝 NOTES

### Model Versions

- **v1.0:** Initial model (81.6% mAP)
- **v2.0:** Optimized settings (82-85% mAP) ← Current

### Future Improvements

- [ ] Add more classes (bag, etc)
- [ ] Increase dataset size (5,000+ images)
- [ ] Try YOLOv11 Small/Medium
- [ ] Ensemble models
- [ ] Post-processing optimization

---

## 🎉 SUCCESS CRITERIA

**Model is ready when:**
- ✅ mAP@50 > 80%
- ✅ Precision > 80%
- ✅ Recall > 70%
- ✅ F1 Score > 75%
- ✅ Inference < 100ms (GPU)
- ✅ File size < 20 MB

**Current model: ALL CRITERIA MET! ✅**

---

**Happy Training! 🚀**

**Questions? Read `ULTIMATE_TRAINING_GUIDE.md`**
