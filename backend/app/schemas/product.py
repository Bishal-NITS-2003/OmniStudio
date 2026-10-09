from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    tagline: Optional[str] = None
    description: str = Field(..., min_length=5)
    category: str = "General"
    price: float = 0.0
    currency: str = "Rs."
    brand_name: str = "OmniBrand"
    features: List[str] = Field(default_factory=list)
    image_urls: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    source_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    brand_name: Optional[str] = None
    features: Optional[List[str]] = None
    image_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    source_url: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductImportRequest(BaseModel):
    url: str

class ProductImportResponse(BaseModel):
    name: str
    tagline: Optional[str] = None
    description: str
    category: str
    price: float
    currency: str = "Rs."
    brand_name: str
    features: List[str]
    image_urls: List[str]
    source_url: str
    extracted_source: str
    confidence_score: float
