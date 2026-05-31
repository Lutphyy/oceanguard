"""
OceanGuard Backend - FastAPI Application
"""
import sys
from pathlib import Path

# Add backend dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import detection

app = FastAPI(
    title="OceanGuard API",
    description="API untuk deteksi sampah laut menggunakan YOLOv8",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router sudah punya prefix /api/v1 di dalamnya
app.include_router(detection.router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "OceanGuard API is running"}
