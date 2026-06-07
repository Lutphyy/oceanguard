"use client";

import { useState, useRef, useCallback } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Color mapping for each detection class
const CLASS_COLORS = {
  plastic: "#ff4d6d",
  bottle: "#0099e6",
  can: "#f59e0b",
  net: "#8b5cf6",
  bag: "#10b981",
  rope: "#ec4899",
  others: "#6b7280",
  default: "#0099e6",
};

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [detectionResult, setDetectionResult] = useState(null);
  const [annotatedImage, setAnnotatedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.40); // NEW: Confidence threshold (default 40%)
  const fileInputRef = useRef(null);

  const handleFileSelect = useCallback((file) => {
    if (!file) return;
    const validTypes = ["image/jpeg", "image/png", "image/webp", "image/jpg"];
    if (!validTypes.includes(file.type)) {
      setError("Format file tidak didukung. Gunakan JPG, PNG, atau WebP.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError("Ukuran file maksimal 10MB.");
      return;
    }
    setError(null);
    setSelectedFile(file);
    setDetectionResult(null);
    setAnnotatedImage(null);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  }, []);

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setIsDragOver(false);
      const file = e.dataTransfer.files[0];
      handleFileSelect(file);
    },
    [handleFileSelect]
  );

  const handleDetect = async () => {
    if (!selectedFile) return;
    setIsLoading(true);
    setError(null);

    try {
      // Request JSON detection results with confidence threshold
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(
        `${API_URL}/api/v1/detect?confidence=${confidenceThreshold}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setDetectionResult(data);

      // Request annotated image with confidence threshold
      const formData2 = new FormData();
      formData2.append("file", selectedFile);

      const imgResponse = await fetch(
        `${API_URL}/api/v1/detect/annotated?confidence=${confidenceThreshold}`,
        {
          method: "POST",
          body: formData2,
        }
      );

      if (imgResponse.ok) {
        const blob = await imgResponse.blob();
        const imgUrl = URL.createObjectURL(blob);
        setAnnotatedImage(imgUrl);
      }
    } catch (err) {
      setError(
        `Gagal mendeteksi: ${err.message}. Pastikan backend API berjalan di ${API_URL}`
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setDetectionResult(null);
    setAnnotatedImage(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  // Count detections per class
  const getClassStats = () => {
    if (!detectionResult?.detections) return {};
    const stats = {};
    detectionResult.detections.forEach((d) => {
      stats[d.class_name] = (stats[d.class_name] || 0) + 1;
    });
    return stats;
  };

  // NEW: Download annotated image
  const handleDownload = () => {
    if (!annotatedImage) return;
    const link = document.createElement("a");
    link.href = annotatedImage;
    link.download = `oceanguard-detection-${Date.now()}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <main className="min-h-screen">
      {/* ===== NAVBAR ===== */}
      <nav className="glass sticky top-0 z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-ocean-500 to-seagreen-500 flex items-center justify-center text-xl">
              🌊
            </div>
            <div>
              <h1 className="text-lg font-bold gradient-text">OceanGuard</h1>
              <p className="text-xs text-slate-400">
                Marine Debris Detection System
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4 text-sm text-slate-400">
            <span className="hidden sm:inline">Powered by YOLOv8</span>
            <div className="w-2 h-2 rounded-full bg-seagreen-400 animate-pulse" />
          </div>
        </div>
      </nav>

      {/* ===== HERO SECTION ===== */}
      <section className="relative px-6 pt-16 pb-12 overflow-hidden">
        {/* Background gradient orbs */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-ocean-500/10 rounded-full blur-[128px] pointer-events-none" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-seagreen-500/10 rounded-full blur-[128px] pointer-events-none" />

        <div className="max-w-4xl mx-auto text-center relative z-10 animate-fade-in-up">
          <h2 className="text-4xl sm:text-5xl font-bold mb-4">
            Deteksi{" "}
            <span className="gradient-text">Sampah Laut</span> dengan AI
          </h2>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10">
            Upload gambar bawah laut atau pesisir pantai, dan biarkan model
            YOLOv8 mendeteksi serta mengklasifikasi sampah secara otomatis.
          </p>
        </div>
      </section>

      {/* ===== UPLOAD SECTION ===== */}
      <section className="px-6 pb-16">
        <div className="max-w-5xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left: Upload Area */}
            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
                📤 Upload Gambar
              </h3>

              {/* Dropzone */}
              <div
                id="dropzone"
                onDrop={handleDrop}
                onDragOver={(e) => {
                  e.preventDefault();
                  setIsDragOver(true);
                }}
                onDragLeave={() => setIsDragOver(false)}
                onClick={() => fileInputRef.current?.click()}
                className={`
                  relative rounded-2xl border-2 border-dashed cursor-pointer
                  transition-all duration-300 overflow-hidden
                  ${
                    isDragOver
                      ? "border-ocean-500 bg-ocean-500/10 dropzone-active"
                      : previewUrl
                        ? "border-slate-700 bg-slate-900/50"
                        : "border-slate-700 bg-slate-900/50 hover:border-ocean-500/50 hover:bg-slate-900"
                  }
                  ${previewUrl ? "p-2" : "p-12"}
                `}
              >
                {previewUrl ? (
                  <img
                    src={previewUrl}
                    alt="Preview"
                    className="w-full rounded-xl object-contain max-h-[400px]"
                  />
                ) : (
                  <div className="text-center">
                    <div className="text-5xl mb-4">📷</div>
                    <p className="text-slate-300 font-medium mb-2">
                      Drag & drop gambar di sini
                    </p>
                    <p className="text-sm text-slate-500">
                      atau klik untuk memilih file (JPG, PNG, WebP — maks 10MB)
                    </p>
                  </div>
                )}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  className="hidden"
                  onChange={(e) => handleFileSelect(e.target.files[0])}
                />
              </div>

              {/* Confidence Threshold Slider - NEW! */}
              {selectedFile && (
                <div className="glass rounded-xl p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-semibold text-slate-300">
                      🎯 Confidence Threshold
                    </label>
                    <span className="text-sm font-mono font-bold text-ocean-400">
                      {(confidenceThreshold * 100).toFixed(0)}%
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0.01"
                    max="0.99"
                    step="0.01"
                    value={confidenceThreshold}
                    onChange={(e) =>
                      setConfidenceThreshold(parseFloat(e.target.value))
                    }
                    className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-ocean-500"
                  />
                  <div className="flex justify-between text-xs text-slate-500">
                    <span>1% (Lebih banyak deteksi)</span>
                    <span>99% (Lebih akurat)</span>
                  </div>
                  <p className="text-xs text-slate-400">
                    💡 Threshold rendah = deteksi lebih banyak objek (tapi bisa
                    ada false positive). Threshold tinggi = hanya objek dengan
                    confidence tinggi.
                  </p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-3">
                <button
                  id="btn-detect"
                  onClick={handleDetect}
                  disabled={!selectedFile || isLoading}
                  className={`
                    flex-1 py-3 px-6 rounded-xl font-semibold text-sm
                    transition-all duration-300
                    ${
                      !selectedFile || isLoading
                        ? "bg-slate-800 text-slate-500 cursor-not-allowed"
                        : "bg-gradient-to-r from-ocean-500 to-seagreen-500 text-white hover:shadow-lg hover:shadow-ocean-500/25 hover:-translate-y-0.5 active:translate-y-0"
                    }
                  `}
                >
                  {isLoading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg
                        className="w-5 h-5 spin-slow"
                        viewBox="0 0 24 24"
                        fill="none"
                      >
                        <circle
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="3"
                          strokeDasharray="40 20"
                        />
                      </svg>
                      Mendeteksi...
                    </span>
                  ) : (
                    "🔍 Mulai Deteksi"
                  )}
                </button>
                {selectedFile && (
                  <button
                    id="btn-reset"
                    onClick={handleReset}
                    className="py-3 px-6 rounded-xl font-semibold text-sm bg-slate-800 text-slate-300 hover:bg-slate-700 transition-all"
                  >
                    ↻ Reset
                  </button>
                )}
              </div>

              {/* Error Message */}
              {error && (
                <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
                  ⚠️ {error}
                </div>
              )}
            </div>

            {/* Right: Results */}
            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
                📊 Hasil Deteksi
              </h3>

              {/* Annotated Image or Placeholder */}
              <div className="rounded-2xl border border-slate-800 bg-slate-900/50 overflow-hidden relative">
                {isLoading ? (
                  /* Loading Skeleton - NEW! */
                  <div className="p-12 space-y-4 animate-pulse">
                    <div className="h-64 bg-slate-800 rounded-lg"></div>
                    <div className="space-y-2">
                      <div className="h-4 bg-slate-800 rounded w-3/4"></div>
                      <div className="h-4 bg-slate-800 rounded w-1/2"></div>
                      <div className="h-4 bg-slate-800 rounded w-2/3"></div>
                    </div>
                  </div>
                ) : annotatedImage ? (
                  <>
                    <img
                      src={annotatedImage}
                      alt="Detection Result"
                      className="w-full object-contain max-h-[400px]"
                    />
                    {/* Download Button - NEW! */}
                    <button
                      onClick={handleDownload}
                      className="absolute top-4 right-4 p-3 rounded-xl bg-slate-900/90 backdrop-blur-sm border border-slate-700 text-white hover:bg-ocean-500 hover:border-ocean-500 transition-all duration-300 hover:scale-110 active:scale-95 shadow-lg"
                      title="Download gambar hasil deteksi"
                    >
                      <svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                        />
                      </svg>
                    </button>
                  </>
                ) : (
                  <div className="p-12 text-center">
                    <div className="text-5xl mb-4 opacity-30">🎯</div>
                    <p className="text-slate-500 text-sm">
                      Hasil deteksi akan muncul di sini
                    </p>
                  </div>
                )}
              </div>

              {/* Detection Stats */}
              {isLoading ? (
                /* Loading Skeleton for Stats - NEW! */
                <div className="animate-pulse space-y-3">
                  <div className="glass rounded-xl p-4 space-y-3">
                    <div className="h-4 bg-slate-800 rounded w-1/3"></div>
                    <div className="grid grid-cols-3 gap-3">
                      <div className="h-20 bg-slate-800 rounded-lg"></div>
                      <div className="h-20 bg-slate-800 rounded-lg"></div>
                      <div className="h-20 bg-slate-800 rounded-lg"></div>
                    </div>
                  </div>
                  <div className="glass rounded-xl p-4 space-y-2">
                    <div className="h-4 bg-slate-800 rounded w-1/2"></div>
                    <div className="h-3 bg-slate-800 rounded w-full"></div>
                    <div className="h-3 bg-slate-800 rounded w-full"></div>
                    <div className="h-3 bg-slate-800 rounded w-full"></div>
                  </div>
                </div>
              ) : (
                detectionResult && (
                <div className="animate-fade-in-up space-y-3">
                  {/* Summary */}
                  <div className="glass rounded-xl p-4">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm font-semibold text-slate-300">
                        Ringkasan Deteksi
                      </span>
                      <span className="text-xs text-slate-500">
                        {detectionResult.inference_time_ms?.toFixed(0)}ms
                      </span>
                    </div>
                    <div className="grid grid-cols-3 gap-3">
                      <div className="text-center p-3 rounded-lg bg-ocean-500/10">
                        <div className="text-2xl font-bold text-ocean-400">
                          {detectionResult.detections?.length || 0}
                        </div>
                        <div className="text-xs text-slate-400 mt-1">
                          Total Objek
                        </div>
                      </div>
                      <div className="text-center p-3 rounded-lg bg-seagreen-500/10">
                        <div className="text-2xl font-bold text-seagreen-400">
                          {Object.keys(getClassStats()).length}
                        </div>
                        <div className="text-xs text-slate-400 mt-1">
                          Jenis Sampah
                        </div>
                      </div>
                      <div className="text-center p-3 rounded-lg bg-coral-500/10">
                        <div className="text-2xl font-bold text-coral-400">
                          {detectionResult.detections?.length > 0
                            ? (
                                detectionResult.detections.reduce(
                                  (sum, d) => sum + d.confidence,
                                  0
                                ) / detectionResult.detections.length
                              ).toFixed(1)
                            : "0"}
                          %
                        </div>
                        <div className="text-xs text-slate-400 mt-1">
                          Avg Confidence
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Per-class breakdown */}
                  <div className="glass rounded-xl p-4">
                    <span className="text-sm font-semibold text-slate-300 block mb-3">
                      Distribusi per Kelas
                    </span>
                    <div className="space-y-2">
                      {Object.entries(getClassStats()).map(
                        ([className, count]) => (
                          <div
                            key={className}
                            className="flex items-center gap-3"
                          >
                            <div
                              className="w-3 h-3 rounded-full flex-shrink-0"
                              style={{
                                backgroundColor:
                                  CLASS_COLORS[className.toLowerCase()] ||
                                  CLASS_COLORS.default,
                              }}
                            />
                            <span className="text-sm text-slate-300 flex-1 capitalize">
                              {className}
                            </span>
                            <span className="text-sm font-mono font-bold text-white">
                              {count}
                            </span>
                            <div className="w-24 h-2 rounded-full bg-slate-800 overflow-hidden">
                              <div
                                className="h-full rounded-full transition-all duration-500"
                                style={{
                                  width: `${(count / (detectionResult.detections?.length || 1)) * 100}%`,
                                  backgroundColor:
                                    CLASS_COLORS[className.toLowerCase()] ||
                                    CLASS_COLORS.default,
                                }}
                              />
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  </div>

                  {/* Detection Table */}
                  {detectionResult.detections?.length > 0 && (
                    <div className="glass rounded-xl p-4 overflow-x-auto">
                      <span className="text-sm font-semibold text-slate-300 block mb-3">
                        Detail Objek Terdeteksi
                      </span>
                      <table className="w-full text-xs">
                        <thead>
                          <tr className="text-slate-500 border-b border-slate-800">
                            <th className="py-2 text-left">#</th>
                            <th className="py-2 text-left">Kelas</th>
                            <th className="py-2 text-right">Confidence</th>
                          </tr>
                        </thead>
                        <tbody>
                          {detectionResult.detections
                            .slice(0, 10)
                            .map((det, i) => (
                              <tr
                                key={i}
                                className="border-b border-slate-800/50 hover:bg-slate-800/30"
                              >
                                <td className="py-2 text-slate-500">{i + 1}</td>
                                <td className="py-2">
                                  <span className="flex items-center gap-2">
                                    <div
                                      className="w-2 h-2 rounded-full"
                                      style={{
                                        backgroundColor:
                                          CLASS_COLORS[
                                            det.class_name?.toLowerCase()
                                          ] || CLASS_COLORS.default,
                                      }}
                                    />
                                    <span className="capitalize text-slate-200">
                                      {det.class_name}
                                    </span>
                                  </span>
                                </td>
                                <td className="py-2 text-right font-mono text-seagreen-400">
                                  {(det.confidence * 100).toFixed(1)}%
                                </td>
                              </tr>
                            ))}
                        </tbody>
                      </table>
                      {detectionResult.detections.length > 10 && (
                        <p className="text-xs text-slate-500 mt-2 text-center">
                          ... dan{" "}
                          {detectionResult.detections.length - 10} objek lainnya
                        </p>
                      )}
                    </div>
                  )}
                </div>
              )
              )}
            </div>
          </div>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer className="mt-auto px-6 py-8 border-t border-slate-800">
        <div className="max-w-5xl mx-auto text-center">
          <p className="text-sm text-slate-500">
            🌊 OceanGuard — Sistem Deteksi Sampah Laut Berbasis YOLOv8
          </p>
          <p className="text-xs text-slate-600 mt-1">
            Proyek Mata Kuliah Pengolahan Citra Digital • 2025/2026
          </p>
        </div>
      </footer>
    </main>
  );
}
