from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class AccountResponse(BaseModel):
    id: int
    platform: str
    display_name: str
    handle: str
    avatar_url: Optional[str] = None
    is_connected: bool
    is_mock: bool
    credentials_mask: str
    account_metadata: Dict[str, Any]
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AccountConnectRequest(BaseModel):
    platform: str
    display_name: Optional[str] = None
    handle: Optional[str] = None
    access_token: Optional[str] = None
    is_mock: bool = False

class PublishingLogResponse(BaseModel):
    id: int
    campaign_id: int
    platform: str
    status: str
    external_post_id: Optional[str] = None
    post_url: Optional[str] = None
    error_message: Optional[str] = None
    scheduled_for: Optional[datetime] = None
    published_at: datetime

    model_config = ConfigDict(from_attributes=True)
