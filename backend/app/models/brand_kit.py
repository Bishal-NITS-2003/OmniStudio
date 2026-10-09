from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.core.database import Base

class BrandKit(Base):
    __tablename__ = "brand_kits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    logo_url = Column(String(500), nullable=True)
    primary_color = Column(String(50), default="#6366f1")      # Indigo
    secondary_color = Column(String(50), default="#ec4899")    # Pink
    accent_color = Column(String(50), default="#06b6d4")       # Cyan
    background_color = Column(String(50), default="#0f172a")   # Slate 900
    font_family = Column(String(100), default="Inter")
    tone_of_voice = Column(String(100), default="Energetic & Modern")
    target_persona = Column(Text, default="Gen-Z and Millennials seeking innovative, reliable lifestyle products")
    guidelines = Column(JSON, default=list)                     # Reusable dos/don'ts or hashtag guidelines
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
