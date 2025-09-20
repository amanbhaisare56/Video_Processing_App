from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    duration = Column(Float)
    size = Column(Float)
    upload_time = Column(DateTime, default=datetime.utcnow)

    trimmed_videos = relationship("TrimmedVideo", back_populates="original")

class TrimmedVideo(Base):
    __tablename__ = "trimmed_videos"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    filename = Column(String, nullable=False)
    start_time = Column(Float)
    end_time = Column(Float)

    original = relationship("Video", back_populates="trimmed_videos")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")  # pending, processing, done, failed
    result_file = Column(String, nullable=True)
