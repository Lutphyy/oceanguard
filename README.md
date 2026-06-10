# OceanGuard 🌊

## Sistem Deteksi dan Klasifikasi Sampah Laut Berbasis Deep Learning Menggunakan YOLOv8

Aplikasi web untuk mendeteksi dan mengklasifikasi sampah laut dari gambar atau video menggunakan model YOLOv8 (Ultralytics).

### 🏗️ Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| ML Model | YOLOv8 (Ultralytics) |
| Backend | FastAPI (Python 3.10+) |
| Frontend | Next.js 14 (React) |
| Deployment | Vercel (frontend) + HuggingFace (backend) |

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


### 📝 License

This project is for educational purposes — Pengolahan Citra Digital, Semester Genap 2025/2026.
