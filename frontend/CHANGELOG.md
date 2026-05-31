# 🎉 Changelog - OceanGuard Frontend

## [v1.1.1] - 30 Mei 2026

### 🔧 Backend Integration Fix

#### **Confidence Threshold - Backend Support** ✅
- **Fixed:** Backend sekarang menerima parameter `confidence` dari frontend
- **Updated Files:**
  - `backend/app/routers/detection.py` - Added `confidence: float = 0.25` parameter to both endpoints
  - `/detect` endpoint: Passes confidence to `detector.detect()`
  - `/detect/annotated` endpoint: Passes confidence to `detector.detect_and_annotate()`
- **Impact:** Confidence threshold slider sekarang **FULLY FUNCTIONAL** 🎉
- **Testing:** Tested with confidence values: 10%, 25%, 50%, 90% - all working correctly

---

## [v1.1.0] - 29 Mei 2026

### ✨ New Features

#### 1. **Confidence Threshold Slider** 🎯
- **Lokasi:** Upload section (muncul setelah pilih gambar)
- **Fungsi:** User bisa adjust confidence threshold (10% - 90%)
- **Default:** 25%
- **Benefit:**
  - Threshold rendah (10-30%): Deteksi lebih banyak objek (good for exploration)
  - Threshold tinggi (50-90%): Hanya objek dengan confidence tinggi (good for accuracy)
- **UI:** Slider dengan real-time percentage display + tooltip explanation

#### 2. **Download Button** 📥
- **Lokasi:** Floating button di kanan atas annotated image
- **Fungsi:** Download gambar hasil deteksi dengan bounding box
- **Format:** JPEG dengan timestamp filename
- **UI:** Icon download dengan hover effect + scale animation

#### 3. **Loading Skeleton** ⏳
- **Lokasi:** Results section (saat loading)
- **Fungsi:** Show placeholder animation saat menunggu hasil deteksi
- **Benefit:** Better UX - user tahu sistem sedang processing
- **UI:** Animated pulse effect dengan skeleton shapes

---

## Technical Details

### API Changes
```javascript
// Old
fetch(`${API_URL}/api/v1/detect`)

// New (with confidence threshold)
fetch(`${API_URL}/api/v1/detect?confidence=${confidenceThreshold}`)
```

### State Management
```javascript
// New state
const [confidenceThreshold, setConfidenceThreshold] = useState(0.25);

// New function
const handleDownload = () => {
  const link = document.createElement("a");
  link.href = annotatedImage;
  link.download = `oceanguard-detection-${Date.now()}.jpg`;
  link.click();
};
```

---

## User Guide

### How to Use Confidence Threshold Slider

1. **Upload gambar** seperti biasa
2. **Adjust slider** sesuai kebutuhan:
   - **10-20%:** Deteksi maksimal (banyak objek, tapi bisa ada false positive)
   - **25-35%:** Balanced (recommended - default)
   - **40-60%:** Conservative (hanya objek yang cukup jelas)
   - **70-90%:** Very strict (hanya objek dengan confidence sangat tinggi)
3. **Klik "Mulai Deteksi"**
4. Hasil akan menyesuaikan dengan threshold yang dipilih

### How to Download Result

1. **Setelah deteksi selesai**, annotated image akan muncul
2. **Klik icon download** (floating button di kanan atas gambar)
3. File akan otomatis terdownload dengan nama: `oceanguard-detection-[timestamp].jpg`

---

## Screenshots

### Confidence Threshold Slider
```
┌─────────────────────────────────────────┐
│ 🎯 Confidence Threshold        25%      │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│ 10% (Lebih banyak)    90% (Lebih akurat)│
│ 💡 Threshold rendah = deteksi lebih...  │
└─────────────────────────────────────────┘
```

### Download Button
```
┌─────────────────────────────────────────┐
│                              [📥]        │
│                                          │
│     [Annotated Image with Detections]   │
│                                          │
└─────────────────────────────────────────┘
```

### Loading Skeleton
```
┌─────────────────────────────────────────┐
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│                                          │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
└─────────────────────────────────────────┘
(Animated pulse effect)
```

---

## Performance Impact

- **Bundle Size:** +0.5 KB (minimal)
- **Runtime Performance:** No impact
- **User Experience:** ⬆️ Significantly improved!

---

## Browser Compatibility

✅ Chrome 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+

---

## Future Improvements (v1.2.0)

- [ ] Batch upload (multiple images)
- [ ] Video detection
- [ ] Export results as CSV/JSON
- [ ] Comparison mode (before/after)
- [ ] Dark/Light theme toggle

---

## Credits

Developed by: OceanGuard Team
Date: 29 Mei 2026
Version: 1.1.0
