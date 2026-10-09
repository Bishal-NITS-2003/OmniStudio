from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.core.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    prompt = Column(Text, nullable=False)
    product_ids = Column(JSON, default=list)       # list of int product IDs
    brand_kit_id = Column(Integer, nullable=True)
    target_audience = Column(String(255), default="General Tech Enthusiasts")
    tone = Column(String(100), default="Energetic & Modern")
    language = Column(String(50), default="English")
    objective = Column(String(100), default="Conversions & Brand Awareness")
    cta = Column(String(100), default="Shop Now")
    
    # Specific Platforms (Strictly YouTube, Instagram, Facebook)
    platforms = Column(JSON, default=lambda: ["instagram", "facebook", "youtube"])
    
    # Specific user-selected format specifications (one video format, one poster format)
    video_format = Column(String(50), default="9:16")    # "9:16", "16:9", "1:1"
    poster_format = Column(String(50), default="1:1")   # "1:1", "4:5", "16:9", "9:16"
    
    # Workflow Status
    # DRAFT | IN_PROGRESS | WAITING_APPROVAL | APPROVED | PUBLISHED | FAILED
    status = Column(String(50), default="DRAFT")
    current_step = Column(String(100), default="draft")
    qc_retry_count = Column(Integer, default=0)
    step_logs = Column(JSON, default=list)
    
    # LangGraph Output Artifacts
    product_analysis = Column(JSON, default=dict)
    campaign_plan = Column(JSON, default=dict)
    storyboard = Column(JSON, default=list)
    quality_report = Column(JSON, default=dict)
    generated_assets = Column(JSON, default=dict)  # {"videos": [...], "posters": [...], "captions": {...}}
    published_records = Column(JSON, default=list) # [{"platform": "instagram", "posts": [...]}]
    
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
