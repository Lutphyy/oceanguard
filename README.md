# OceanGuard 🌊

## Sistem Deteksi dan Klasifikasi Sampah Laut Berbasis Deep Learning Menggunakan YOLOv8

Aplikasi web untuk mendeteksi dan mengklasifikasi sampah laut dari gambar atau video menggunakan model YOLOv8 (Ultralytics).

### 🏗️ Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| ML Model | YOLOv8 (Ultralytics) |
| Backend | FastAPI (Python 3.10+) |
| Frontend | Next.js 14 (React) |
| Deployment | Vercel (frontend) + Railway (backend) |

### 📁 Project Structure

```
Pengelolaan Citra/
├── model/                  # ML Model & Training
│   ├── scripts/            # Training & evaluation scripts
│   ├── notebooks/          # Jupyter notebooks
│   ├── data/               # Dataset (gitignored)
│   └── weights/            # Trained model weights
├── backend/                # FastAPI Backend
│   └── app/
│       ├── main.py         # FastAPI entry point
│       ├── routers/        # API routes
│       ├── services/       # Business logic
│       └── utils/          # Utilities
├── frontend/               # Next.js Frontend
└── docs/                   # Documentation & Reports
```

### 🚀 Quick Start

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Model Training
```bash
cd model
pip install -r requirements.txt
python scripts/train.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### 📊 Model Performance (Target)

| Metric | Target |
|--------|--------|
| mAP@50 | ≥ 0.75 |
| mAP@50:95 | ≥ 0.50 |
| Precision | ≥ 0.80 |
| Recall | ≥ 0.75 |
| Inference Speed | ≤ 50ms/image |

### 📝 License

This project is for educational purposes — Pengolahan Citra Digital, Semester Genap 2025/2026.
