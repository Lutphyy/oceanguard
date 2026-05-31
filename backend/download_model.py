"""
Download model weights from Google Drive on startup
"""
import os
import sys
from pathlib import Path
import urllib.request

def download_file_from_google_drive(file_id, destination):
    """Download file from Google Drive"""
    URL = "https://drive.google.com/uc?export=download"
    
    session = urllib.request.urlopen(f"{URL}&id={file_id}")
    
    # Save to file
    with open(destination, 'wb') as f:
        f.write(session.read())
    
    print(f"✅ Model downloaded to: {destination}")

def ensure_model_exists():
    """Ensure model weights exist, download if not"""
    # Path to model weights
    weights_dir = Path(__file__).parent.parent / "model" / "weights"
    weights_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = weights_dir / "best.pt"
    
    # Check if model already exists
    if model_path.exists():
        print(f"✅ Model already exists: {model_path}")
        return str(model_path)
    
    # Get Google Drive file ID from environment variable
    file_id = os.getenv("MODEL_DRIVE_ID")
    
    if not file_id:
        print("⚠️  MODEL_DRIVE_ID not set. Backend will run in DEMO MODE.")
        print("   To enable real detection, set MODEL_DRIVE_ID environment variable.")
        return None
    
    print(f"📥 Downloading model from Google Drive...")
    print(f"   File ID: {file_id}")
    
    try:
        download_file_from_google_drive(file_id, str(model_path))
        return str(model_path)
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        print("   Backend will run in DEMO MODE.")
        return None

if __name__ == "__main__":
    ensure_model_exists()
