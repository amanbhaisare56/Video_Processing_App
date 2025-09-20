from fastapi import FastAPI
from backend.routers import upload, trim, overlay, job, quality
from backend.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Video Processing API")

# Include routers
app.include_router(upload.router, prefix="/videos", tags=["Videos"])
app.include_router(trim.router, prefix="/trim", tags=["Trim"])
app.include_router(overlay.router, prefix="/overlay", tags=["Overlay"])
app.include_router(job.router, prefix="/jobs", tags=["Jobs"])
app.include_router(quality.router, prefix="/quality", tags=["Quality"])
