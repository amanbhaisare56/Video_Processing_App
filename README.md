📦 Setup
1. Clone repo
git clone https://github.com/your-repo/video-processing-app.git
cd video-processing-app

2. Run with Docker
docker-compose up --build


This starts backend (FastAPI) on http://localhost:9000, plus Redis, Postgres, and Celery worker.

🧪 Quick Demo Workflow
1️⃣ Upload a video
curl -X POST "http://localhost:9000/videos/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@D:/Projects/New Video Processing app/sample video/sample.mp4;type=video/mp4"


Response:

{
  "video_id": "1234-uuid",
  "filename": "sample.mp4"
}

2️⃣ Trim the video
curl -X POST "http://localhost:9000/videos/1234-uuid/trim" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"start_time": 0, "end_time": 10}'


Response:

{
  "job_id": "abcd-task-uuid",
  "status": "PENDING"
}

3️⃣ Check job status
curl "http://localhost:9000/jobs/abcd-task-uuid"


Response example:

{
  "job_id": "abcd-task-uuid",
  "status": "SUCCESS",
  "result": {
    "output_file": "processed/sample_trimmed.mp4"
  }
}

4️⃣ Download result
curl -O "http://localhost:9000/videos/download/processed/sample_trimmed.mp4"


This saves the processed video locally.
