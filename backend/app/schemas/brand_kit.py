from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class BrandKitBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    logo_url: Optional[str] = None
    primary_color: str = "#6366f1"
    secondary_color: str = "#ec4899"
    accent_color: str = "#06b6d4"
    background_color: str = "#0f172a"
    font_family: str = "Inter"
    tone_of_voice: str = "Energetic & Modern"
    target_persona: str = "Modern digitally-native buyers"
    guidelines: List[str] = Field(default_factory=list)

class BrandKitCreate(BrandKitBase):
    pass

class BrandKitUpdate(BaseModel):
    name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    background_color: Optional[str] = None
    font_family: Optional[str] = None
    tone_of_voice: Optional[str] = None
    target_persona: Optional[str] = None
    guidelines: Optional[List[str]] = None

class BrandKitResponse(BrandKitBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
