from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class CampaignBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    prompt: str = Field(..., min_length=3)
    product_ids: List[int] = Field(default_factory=list)
    brand_kit_id: Optional[int] = None
    target_audience: str = "General Tech Enthusiasts"
    tone: str = "Energetic & Modern"
    language: str = "English"
    objective: str = "Conversions & Brand Awareness"
    cta: str = "Shop Now"
    platforms: List[str] = Field(default_factory=lambda: ["instagram", "facebook", "youtube"])
    video_format: str = Field(default="9:16", description="Single selected video screen size (e.g. 9:16, 16:9, 1:1)")
    poster_format: str = Field(default="1:1", description="Single selected poster screen size (e.g. 1:1, 4:5, 16:9, 9:16)")

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    title: Optional[str] = None
    prompt: Optional[str] = None
    product_ids: Optional[List[int]] = None
    brand_kit_id: Optional[int] = None
    target_audience: Optional[str] = None
    tone: Optional[str] = None
    language: Optional[str] = None
    objective: Optional[str] = None
    cta: Optional[str] = None
    platforms: Optional[List[str]] = None
    video_format: Optional[str] = None
    poster_format: Optional[str] = None

class CampaignResponse(CampaignBase):
    id: int
    status: str
    current_step: str
    qc_retry_count: int
    step_logs: List[Dict[str, Any]]
    product_analysis: Dict[str, Any]
    campaign_plan: Dict[str, Any]
    storyboard: List[Dict[str, Any]]
    quality_report: Dict[str, Any]
    generated_assets: Dict[str, Any]
    published_records: List[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ApprovalRequest(BaseModel):
    approved: bool
    feedback: Optional[str] = None

class PublishTriggerRequest(BaseModel):
    platforms: Optional[List[str]] = None
    scheduled_for: Optional[datetime] = None
