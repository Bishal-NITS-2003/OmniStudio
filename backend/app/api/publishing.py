import io
import zipfile
import json
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.publishing import PublishingAccount, PublishingLog
from app.models.campaign import Campaign
from app.schemas.publishing import AccountResponse, AccountConnectRequest, PublishingLogResponse

router = APIRouter(prefix="/publishing", tags=["Publishing"])

DEFAULT_ACCOUNTS = [
    {
        "platform": "instagram",
        "display_name": "Instagram Business",
        "handle": "@omnipost_studio",
        "avatar_url": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=120&q=80",
        "is_connected": True,
        "is_mock": True,
        "credentials_mask": "Demo Sandbox Token",
        "account_metadata": {"followers": "24.8K", "tier": "Creator"}
    },
    {
        "platform": "facebook",
        "display_name": "Facebook Page",
        "handle": "OmniPost Official Page",
        "avatar_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=120&q=80",
        "is_connected": True,
        "is_mock": True,
        "credentials_mask": "Demo Sandbox Token",
        "account_metadata": {"followers": "18.5K", "tier": "Business Page"}
    },
    {
        "platform": "youtube",
        "display_name": "YouTube Shorts Channel",
        "handle": "OmniPost Official",
        "avatar_url": "https://images.unsplash.com/photo-1611162618071-b39a2ec055fb?w=120&q=80",
        "is_connected": True,
        "is_mock": True,
        "credentials_mask": "Demo Sandbox Token",
        "account_metadata": {"subscribers": "15.9K", "tier": "Partner"}
    }
]

def ensure_default_accounts(db: Session):
    existing = {acc.platform for acc in db.query(PublishingAccount).all()}
    for acc in DEFAULT_ACCOUNTS:
        if acc["platform"] not in existing:
            new_acc = PublishingAccount(**acc)
            db.add(new_acc)
    db.commit()

@router.get("/accounts", response_model=List[AccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    ensure_default_accounts(db)
    return db.query(PublishingAccount).all()

@router.post("/accounts/connect", response_model=AccountResponse)
def connect_account(payload: AccountConnectRequest, db: Session = Depends(get_db)):
    acc = db.query(PublishingAccount).filter(PublishingAccount.platform == payload.platform).first()
    if not acc:
        acc = PublishingAccount(
            platform=payload.platform,
            display_name=payload.display_name or payload.platform.capitalize(),
            handle=payload.handle or f"@{payload.platform}_account"
        )
        db.add(acc)
    
    acc.is_connected = True
    acc.is_mock = payload.is_mock
    if payload.display_name:
        acc.display_name = payload.display_name
    if payload.handle:
        acc.handle = payload.handle
    if payload.access_token:
        acc.credentials_mask = f"Bearer ••••{payload.access_token[-4:]}"
    
    db.commit()
    db.refresh(acc)
    return acc

@router.get("/logs", response_model=List[PublishingLogResponse])
def get_publishing_logs(db: Session = Depends(get_db)):
    return db.query(PublishingLog).order_by(PublishingLog.id.desc()).all()

@router.get("/download/{campaign_id}")
def download_campaign_assets(campaign_id: int, db: Session = Depends(get_db)):
    """Packages all campaign outputs (videos, poster cards, captions, storyboard) into a ZIP."""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Add Storyboard & Plan JSON
        metadata_content = {
            "title": campaign.title,
            "objective": campaign.objective,
            "tone": campaign.tone,
            "cta": campaign.cta,
            "product_analysis": campaign.product_analysis,
            "campaign_plan": campaign.campaign_plan,
            "storyboard": campaign.storyboard,
            "quality_report": campaign.quality_report
        }
        zip_file.writestr("campaign_plan_and_storyboard.json", json.dumps(metadata_content, indent=2))

        # 2. Add Platform Captions as text files
        assets = campaign.generated_assets or {}
        captions = assets.get("captions", {})
        for plat, c_data in captions.items():
            text_body = f"PLATFORM: {plat.upper()}\n"
            text_body += f"HOOK: {c_data.get('hook', '')}\n"
            text_body += f"CTA: {c_data.get('cta', '')}\n\n"
            text_body += f"CAPTION:\n{c_data.get('caption', '')}\n\n"
            text_body += f"HASHTAGS:\n{' '.join(c_data.get('hashtags', []))}\n"
            zip_file.writestr(f"captions_{plat}.txt", text_body)

        # 3. Add Carousel Slides
        carousels = assets.get("carousel_slides", [])
        if carousels:
            zip_file.writestr("carousel_slides.json", json.dumps(carousels, indent=2))

        # 4. Add Videos if on disk
        videos = assets.get("videos", [])
        for v in videos:
            v_filepath = v.get("filepath")
            if v_filepath and Path(v_filepath).exists():
                zip_file.write(v_filepath, arcname=f"media/{Path(v_filepath).name}")

        # 5. Add Posters if on disk
        posters = assets.get("posters", [])
        for p in posters:
            p_filepath = p.get("filepath")
            if p_filepath and Path(p_filepath).exists():
                zip_file.write(p_filepath, arcname=f"media/{Path(p_filepath).name}")

    zip_buffer.seek(0)
    zip_bytes = zip_buffer.getvalue()

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=omnipost_campaign_{campaign_id}_assets.zip"}
    )
