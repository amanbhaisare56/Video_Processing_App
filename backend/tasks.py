from celery import Celery
import subprocess

celery_app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@celery_app.task
def process_video_ffmpeg(input_path, output_path, ffmpeg_args):
    cmd = ["ffmpeg", "-i", input_path] + ffmpeg_args + [output_path]
    subprocess.run(cmd)
    return output_path
