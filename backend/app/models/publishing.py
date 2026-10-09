from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from app.core.database import Base

class PublishingAccount(Base):
    __tablename__ = "publishing_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), unique=True, index=True, nullable=False) # instagram, youtube, tiktok, linkedin, facebook
    display_name = Column(String(100), nullable=False)
    handle = Column(String(100), default="@omnipost_demo")
    avatar_url = Column(String(500), nullable=True)
    is_connected = Column(Boolean, default=False)
    is_mock = Column(Boolean, default=True)
    credentials_mask = Column(String(100), default="Demo Mode (Simulation)")
    account_metadata = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PublishingLog(Base):
    __tablename__ = "publishing_logs"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, index=True, nullable=False)
    platform = Column(String(50), nullable=False)
    status = Column(String(50), default="PENDING") # PENDING, PUBLISHED, FAILED, SCHEDULED
    external_post_id = Column(String(100), nullable=True)
    post_url = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)
    payload_snapshot = Column(JSON, default=dict)
    scheduled_for = Column(DateTime, nullable=True)
    published_at = Column(DateTime, default=datetime.utcnow)
