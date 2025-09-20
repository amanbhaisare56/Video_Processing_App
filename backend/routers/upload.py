from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
import shutil, os
import subprocess
from backend.database import SessionLocal
from backend import models

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
def upload_video(file: UploadFile, db: Session = Depends(get_db)):
    filepath = f"{UPLOAD_DIR}/{file.filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Get metadata using ffprobe
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size", "-of", "default=noprint_wrappers=1:nokey=1", filepath
    ], capture_output=True, text=True)

    duration, size = probe.stdout.splitlines()
    video = models.Video(
        filename=file.filename,
        duration=float(duration),
        size=float(size)
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return {"id": video.id, "filename": video.filename, "duration": video.duration}

@router.get("/")
def list_videos(db: Session = Depends(get_db)):
    return db.query(models.Video).all()
