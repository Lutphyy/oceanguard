# 🚀 PANDUAN DEPLOYMENT OCEANGUARD

## 📦 PERSIAPAN

### 1. Install Git (jika belum)
Download: https://git-scm.com/downloads

### 2. Buat Akun (GRATIS)
- **GitHub:** https://github.com/signup
- **Vercel:** https://vercel.com/signup (login pakai GitHub)
- **Railway:** https://railway.app/ (login pakai GitHub)

---

## 🔧 STEP 1: PUSH KE GITHUB

### A. Inisialisasi Git di Project Root
```bash
cd "c:\Users\NITRO\Documents\Kuliah\Semester6\Pengelolaan Citra"
git init
git add .
git commit -m "Initial commit - OceanGuard project"
```

### B. Buat Repository di GitHub
1. Buka https://github.com/new
2. Repository name: `oceanguard-detection`
3. Visibility: **Public** (atau Private jika mau)
4. **JANGAN** centang "Add README" (sudah ada)
5. Klik **Create repository**

### C. Push ke GitHub
```bash
git remote add origin https://github.com/USERNAME/oceanguard-detection.git
git branch -M main
git push -u origin main
```
*(Ganti `USERNAME` dengan username GitHub kamu)*

---

## 🎨 STEP 2: DEPLOY FRONTEND (VERCEL)

### A. Login ke Vercel
1. Buka https://vercel.com/
2. Klik **Login** → pilih **Continue with GitHub**
3. Authorize Vercel

### B. Import Project
1. Klik **Add New...** → **Project**
2. Pilih repository: `oceanguard-detection`
3. Klik **Import**

### C. Configure Project
```
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### D. Environment Variables
**JANGAN ISI DULU** - nanti setelah backend deploy

### E. Deploy
1. Klik **Deploy**
2. Tunggu 2-3 menit
3. Setelah selesai, copy URL (contoh: `https://oceanguard-xxx.vercel.app`)
4. **SIMPAN URL INI** - nanti dipakai untuk backend CORS

---

## ⚙️ STEP 3: DEPLOY BACKEND (RAILWAY)

### A. Login ke Railway
1. Buka https://railway.app/
2. Klik **Login** → pilih **Login with GitHub**
3. Authorize Railway

### B. Create New Project
1. Klik **New Project**
2. Pilih **Deploy from GitHub repo**
3. Pilih repository: `oceanguard-detection`

### C. Configure Service
1. Setelah project dibuat, klik **Settings**
2. **Root Directory:** `backend`
3. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### D. Add Environment Variables
Klik tab **Variables**, tambahkan:
```
PORT=8000
PYTHONUNBUFFERED=1
```

### E. Generate Domain
1. Klik tab **Settings**
2. Scroll ke **Networking**
3. Klik **Generate Domain**
4. Copy URL (contoh: `https://oceanguard-backend-xxx.railway.app`)
5. **SIMPAN URL INI**

### F. Deploy
Railway akan otomatis deploy. Tunggu 5-10 menit (download dependencies besar).

---

## 🔗 STEP 4: CONNECT FRONTEND & BACKEND

### A. Update Frontend Environment Variable
1. Buka Vercel Dashboard
2. Pilih project `oceanguard-detection`
3. Klik **Settings** → **Environment Variables**
4. Tambahkan:
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://oceanguard-backend-xxx.railway.app
   ```
   *(Ganti dengan URL Railway kamu)*
5. Klik **Save**

### B. Redeploy Frontend
1. Klik tab **Deployments**
2. Klik **...** (titik tiga) di deployment terakhir
3. Klik **Redeploy**
4. Tunggu 1-2 menit

---

## ✅ STEP 5: TEST APLIKASI

### A. Buka Frontend
URL: `https://oceanguard-xxx.vercel.app`

### B. Test Backend API
URL: `https://oceanguard-backend-xxx.railway.app`

Buka di browser, harusnya muncul:
```json
{"status":"ok","message":"OceanGuard API is running"}
```

### C. Test Detection
1. Upload gambar di frontend
2. Adjust confidence threshold
3. Klik "Mulai Deteksi"
4. Harusnya muncul hasil deteksi!

---

## 🐛 TROUBLESHOOTING

### Frontend Error: "Failed to fetch"
**Solusi:**
1. Check apakah backend URL benar di environment variable
2. Check apakah backend sudah running (buka URL backend di browser)
3. Redeploy frontend setelah update env variable

### Backend Error: "Application failed to respond"
**Solusi:**
1. Check Railway logs: Dashboard → Deployments → View Logs
2. Pastikan `requirements.txt` ada dan benar
3. Pastikan `Procfile` ada dan benar

### Backend Deploy Lama (>10 menit)
**Normal!** Dependencies seperti `torch` dan `ultralytics` sangat besar (~2GB).
Railway perlu download dan install semua.

### Model Tidak Load
**Expected!** Model `best.pt` (5.6MB) tidak di-push ke GitHub karena terlalu besar.
Backend akan jalan dalam **demo mode** (return sample data).

**Solusi untuk Production:**
1. Upload `best.pt` ke Google Drive
2. Set public link
3. Tambahkan script download di backend startup
4. Atau gunakan Railway Volume untuk upload manual

---

## 💰 BIAYA

- **Vercel:** GRATIS unlimited
- **Railway:** GRATIS $5 credit/bulan (~500 jam runtime)
- **Total:** GRATIS untuk project kuliah!

---

## 📝 CATATAN PENTING

### File yang TIDAK Perlu di-Deploy:
- `model/runs/` (training results - sudah di backup)
- `model/data/` (dataset - tidak perlu di server)
- `frontend/node_modules/` (akan di-install otomatis)
- `frontend/.next/` (akan di-build otomatis)
- `docs/` (dokumentasi lokal)

### File yang WAJIB Ada:
- ✅ `backend/requirements.txt`
- ✅ `backend/Procfile`
- ✅ `backend/app/` (semua file Python)
- ✅ `frontend/package.json`
- ✅ `frontend/app/` (semua file Next.js)
- ✅ `.gitignore` (agar tidak push file besar)

---

## 🎉 SELESAI!

Aplikasi kamu sekarang sudah LIVE dan bisa diakses dari mana saja!

**Frontend URL:** https://oceanguard-xxx.vercel.app
**Backend URL:** https://oceanguard-backend-xxx.railway.app

Share link ini ke dosen atau teman untuk demo! 🚀
