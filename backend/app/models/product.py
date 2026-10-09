from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    tagline = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), default="General")
    price = Column(Float, default=0.0)
    currency = Column(String(10), default="Rs.")
    brand_name = Column(String(100), default="OmniBrand")
    features = Column(JSON, default=list)        # list of strings
    image_urls = Column(JSON, default=list)      # list of URLs or local paths
    tags = Column(JSON, default=list)            # list of strings
    source_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
