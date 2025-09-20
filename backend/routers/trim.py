from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import subprocess
from backend.database import SessionLocal
from backend import models

router = APIRouter()
UPLOAD_DIR = "uploads"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def trim_video(video_id: int, start: float, end: float, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        return {"error": "Video not found"}

    input_path = f"{UPLOAD_DIR}/{video.filename}"
    output_path = f"{UPLOAD_DIR}/trimmed_{video.filename}"

    subprocess.run([
        "ffmpeg", "-i", input_path, "-ss", str(start), "-to", str(end), "-c", "copy", output_path
    ])

    trimmed = models.TrimmedVideo(
        video_id=video.id,
        filename=f"trimmed_{video.filename}",
        start_time=start,
        end_time=end
    )
    db.add(trimmed)
    db.commit()
    return {"trimmed_id": trimmed.id, "filename": trimmed.filename}
