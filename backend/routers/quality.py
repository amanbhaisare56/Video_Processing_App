from fastapi import APIRouter
from backend.tasks import process_video_ffmpeg

router = APIRouter()

@router.post("/{video_path}")
def generate_qualities(video_path: str):
    qualities = {
        "1080p": ["-vf", "scale=1920:1080"],
        "720p": ["-vf", "scale=1280:720"],
        "480p": ["-vf", "scale=854:480"]
    }
    jobs = {}
    for q, args in qualities.items():
        output = f"uploads/{q}_{video_path}"
        task = process_video_ffmpeg.delay(f"uploads/{video_path}", output, args)
        jobs[q] = task.id
    return {"jobs": jobs}
