# 🚀 Tutorial Deploy OceanGuard (Frontend + Backend)

## 📋 Overview

Kita akan deploy 2 bagian:
1. **Backend API** (FastAPI + YOLO) → Hugging Face Spaces
2. **Frontend** (Next.js) → Vercel

**Total waktu: ~20 menit**

---

## PART 1: Deploy Backend ke Hugging Face (10 menit)

### Step 1: Ganti SDK Space dari Gradio ke Docker

1. Buka Space kamu: https://huggingface.co/spaces/lutphyy/oceanguard-citra
2. Klik tab **"Settings"** (paling kanan)
3. Scroll ke bawah sampai **"Change Space hardware"**
4. Di bagian **"Space SDK"**, klik **"Change SDK"**
5. Pilih **"Docker"**
6. Klik **"Change SDK"** (konfirmasi)
7. **PENTING:** Space akan rebuild otomatis

### Step 2: Upload File Backend

Klik tab **"Files"**, lalu upload file-file ini:

#### 2.1 Hapus File Lama (PENTING!)
- Hapus file `app.py` (klik file → Delete)
- Biarkan `best.pt` dan `requirements.txt`

#### 2.2 Upload Dockerfile

1. Klik **"+ Add file"** → **"Create a new file"**
2. Nama file: `Dockerfile`
3. Copy-paste isi dari file `backend/Dockerfile.hf`
4. Commit

#### 2.3 Upload README

1. Klik file `README.md` yang sudah ada
2. Klik **"Edit"**
3. Hapus semua isi
4. Copy-paste isi dari file `backend/README-HF.md`
5. Commit

#### 2.4 Update requirements.txt

1. Klik file `requirements.txt`
2. Klik **"Edit"**
3. Hapus semua isi
4. Copy-paste isi dari file `backend/requirements.txt`
5. Commit

#### 2.5 Upload Folder `app/`

**PENTING:** Hugging Face tidak support upload folder via web UI!

**Solusi: Upload file satu-per-satu**

1. Klik **"+ Add file"** → **"Create a new file"**
2. Nama file: `app/__init__.py`
3. Isi: (kosong, langsung commit)
4. Ulangi untuk semua file di folder `app/`:
   - `app/main.py`
   - `app/routers/__init__.py`
   - `app/routers/detection.py`
   - `app/services/__init__.py`
   - `app/services/detector.py`
   - `app/utils/__init__.py`
   - `app/utils/image.py`

**Tips:** Copy-paste isi file dari VS Code ke Hugging Face web editor

### Step 3: Tunggu Build (~5 menit)

1. Klik tab **"App"**
2. Lihat log build
3. Tunggu sampai status **"Running"** (hijau)

### Step 4: Test API

Buka browser, test endpoint:
```
https://lutphyy-oceanguard-citra.hf.space/
```

Harusnya return:
```json
{"status": "ok", "message": "OceanGuard API is running"}
```

✅ **Backend DONE!**

---

## PART 2: Deploy Frontend ke Vercel (10 menit)

### Step 1: Push Project ke GitHub (kalau belum)

```bash
# Di folder project
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/oceanguard.git
git push -u origin main
```

### Step 2: Deploy ke Vercel

1. Buka https://vercel.com
2. Sign up / Login dengan GitHub
3. Klik **"Add New Project"**
4. Pilih repository **"oceanguard"**
5. **Root Directory:** Pilih `frontend`
6. **Framework Preset:** Next.js (auto-detect)
7. **Environment Variables:** Tambahkan:
   ```
   NEXT_PUBLIC_API_URL=https://lutphyy-oceanguard-citra.hf.space
   ```
8. Klik **"Deploy"**

### Step 3: Tunggu Deploy (~2 menit)

Vercel akan auto-build dan deploy.

### Step 4: Test Frontend

Buka URL yang diberikan Vercel:
```
https://oceanguard-xxx.vercel.app
```

✅ **Frontend DONE!**

---

## PART 3: Test End-to-End

1. Buka frontend di Vercel
2. Upload gambar underwater trash
3. Klik **"Mulai Deteksi"**
4. Lihat hasil deteksi!

---

## 🔧 Troubleshooting

### Backend Error: "Model not found"
- Pastikan file `best.pt` sudah di-upload
- Pastikan path di Dockerfile benar: `./model/weights/best.pt`

### Frontend Error: "Failed to fetch"
- Cek CORS di backend (sudah di-enable di `main.py`)
- Cek API URL di environment variable Vercel

### Build Error di Hugging Face
- Cek log error di tab "Logs"
- Pastikan semua file sudah di-upload
- Pastikan Dockerfile syntax benar

---

## 📱 Link Final

**Backend API:**
```
https://lutphyy-oceanguard-citra.hf.space
```

**Frontend:**
```
https://oceanguard-xxx.vercel.app
```

---

## 🎓 Untuk Demo ke Dosen

1. Buka frontend
2. Upload 2-3 gambar berbeda
3. Tunjukkan hasil deteksi real-time
4. Explain arsitektur:
   - Frontend: Next.js di Vercel
   - Backend: FastAPI + YOLOv8 di Hugging Face
   - Model: Trained sendiri dengan 3,028 images

**Dosen pasti impressed!** 🎉

---

Made with ❤️ for Ocean Conservation
