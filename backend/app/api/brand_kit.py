from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.brand_kit import BrandKit
from app.schemas.brand_kit import BrandKitCreate, BrandKitUpdate, BrandKitResponse

router = APIRouter(prefix="/brand-kit", tags=["Brand Kit"])

def get_or_create_default_brand(db: Session) -> BrandKit:
    brand = db.query(BrandKit).first()
    if not brand:
        brand = BrandKit(
            name="OmniNova Studio",
            logo_url="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=200&q=80",
            primary_color="#6366f1",
            secondary_color="#ec4899",
            accent_color="#06b6d4",
            background_color="#0f172a",
            font_family="Inter",
            tone_of_voice="Energetic, Confident & Modern",
            target_persona="Digital pioneers and tech-forward consumers",
            guidelines=[
                "Always lead with bold visual contrast and clear benefits",
                "Keep captions punchy, engaging, and action-oriented",
                "Ensure call-to-action is crystal clear across all media"
            ]
        )
        db.add(brand)
        db.commit()
        db.refresh(brand)
    return brand

@router.get("", response_model=BrandKitResponse)
def get_brand_kit(db: Session = Depends(get_db)):
    return get_or_create_default_brand(db)

@router.put("", response_model=BrandKitResponse)
def update_brand_kit(payload: BrandKitUpdate, db: Session = Depends(get_db)):
    brand = get_or_create_default_brand(db)
    update_data = payload.dict(exclude_unset=True)
    for key, val in update_data.items():
        setattr(brand, key, val)
    db.commit()
    db.refresh(brand)
    return brand
