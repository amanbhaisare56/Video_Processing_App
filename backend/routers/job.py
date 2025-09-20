from fastapi import APIRouter
from backend.tasks import process_video_ffmpeg
import os

router = APIRouter()

@router.post("/submit")
def submit_job():
    result = process_video_ffmpeg.delay("uploads/input.mp4", "uploads/out.mp4", ["-vf", "scale=1280:720"])
    return {"job_id": result.id}

@router.get("/status/{job_id}")
def job_status(job_id: str):
    task = process_video_ffmpeg.AsyncResult(job_id)
    return {"id": job_id, "status": task.status}

@router.get("/result/{job_id}")
def job_result(job_id: str):
    task = process_video_ffmpeg.AsyncResult(job_id)
    if task.status == "SUCCESS":
        return {"file": task.result}
    return {"status": task.status}
