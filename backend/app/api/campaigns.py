import threading
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db, SessionLocal
from app.models.campaign import Campaign
from app.models.product import Product
from app.models.brand_kit import BrandKit
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    ApprovalRequest,
    PublishTriggerRequest
)
from app.workflows.graph import run_campaign_workflow, resume_and_publish_workflow
from app.workflows.state import MarketingWorkflowState

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

def run_workflow_worker(campaign_id: int):
    """Background worker executing the LangGraph workflow pipeline."""
    db = SessionLocal()
    try:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            return

        # Fetch product and brand data
        product = None
        if campaign.product_ids:
            product = db.query(Product).filter(Product.id == campaign.product_ids[0]).first()

        brand = None
        if campaign.brand_kit_id:
            brand = db.query(BrandKit).filter(BrandKit.id == campaign.brand_kit_id).first()
        else:
            brand = db.query(BrandKit).first()

        product_dict = {
            "id": product.id if product else 0,
            "name": product.name if product else campaign.title,
            "tagline": product.tagline if product else "",
            "description": product.description if product else "",
            "category": product.category if product else "General",
            "price": product.price if product else 4999.0,
            "currency": product.currency if product else "Rs.",
            "features": product.features if product else [],
            "image_urls": product.image_urls if product else []
        }

        brand_dict = {
            "name": brand.name if brand else "OmniBrand",
            "primary_color": brand.primary_color if brand else "#6366f1",
            "secondary_color": brand.secondary_color if brand else "#ec4899",
            "accent_color": brand.accent_color if brand else "#06b6d4",
            "background_color": brand.background_color if brand else "#0f172a",
            "tone_of_voice": brand.tone_of_voice if brand else "Energetic"
        }

        initial_state: MarketingWorkflowState = {
            "campaign_id": campaign.id,
            "product_ids": campaign.product_ids or [],
            "brand_kit_id": campaign.brand_kit_id,
            "prompt": campaign.prompt,
            "target_audience": campaign.target_audience,
            "tone": campaign.tone,
            "language": campaign.language,
            "objective": campaign.objective,
            "cta": campaign.cta,
            "platforms": campaign.platforms or ["instagram", "facebook", "youtube"],
            "video_format": campaign.video_format or "9:16",
            "poster_format": campaign.poster_format or "1:1",
            "qc_retry_count": campaign.qc_retry_count or 0,
            "max_qc_retries": 3,
            "status": "IN_PROGRESS",
            "current_step": "analyze_product",
            "step_logs": list(campaign.step_logs or []),
            "product_data": product_dict,
            "brand_kit": brand_dict,
            "approval_status": "PENDING"
        }

        def sync_db(state: MarketingWorkflowState):
            camp = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if camp:
                camp.status = state.get("status", camp.status)
                camp.current_step = state.get("current_step", camp.current_step)
                camp.qc_retry_count = state.get("qc_retry_count", camp.qc_retry_count)
                camp.step_logs = list(state.get("step_logs", []))
                camp.product_analysis = state.get("product_analysis", {})
                camp.campaign_plan = state.get("campaign_plan", {})
                camp.storyboard = list(state.get("storyboard", []))
                camp.generated_assets = state.get("generated_assets", {})
                camp.quality_report = state.get("quality_report", {})
                camp.published_records = list(state.get("published_records", []))
                db.commit()

        run_campaign_workflow(initial_state, db_updater=sync_db)
    except Exception as e:
        camp = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if camp:
            camp.status = "FAILED"
            camp.error_message = str(e)
            logs = list(camp.step_logs or [])
            logs.append({"step": "error", "message": f"Pipeline failure: {str(e)}"})
            camp.step_logs = logs
            db.commit()
    finally:
        db.close()

@router.get("", response_model=List[CampaignResponse])
def get_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).order_by(Campaign.id.desc()).all()

@router.post("", response_model=CampaignResponse)
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    db_campaign = Campaign(**payload.dict())
    db_campaign.status = "DRAFT"
    db_campaign.current_step = "created"
    db_campaign.step_logs = [{"step": "created", "message": "Campaign draft initialized."}]
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.post("/{campaign_id}/generate", response_model=CampaignResponse)
def trigger_generation(campaign_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.status = "IN_PROGRESS"
    campaign.current_step = "starting"
    campaign.step_logs = [{"step": "start", "message": "Triggered LangGraph autonomous marketing agent."}]
    db.commit()
    db.refresh(campaign)

    # Launch worker in background thread
    threading.Thread(target=run_workflow_worker, args=(campaign_id,), daemon=True).start()

    return campaign

@router.post("/{campaign_id}/approve", response_model=CampaignResponse)
def approve_campaign(campaign_id: int, payload: ApprovalRequest, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    logs = list(campaign.step_logs or [])
    if payload.approved:
        campaign.status = "APPROVED"
        campaign.current_step = "approved"
        logs.append({"step": "approval", "message": f"Campaign approved by user. Notes: {payload.feedback or 'None'}"})
    else:
        campaign.status = "DRAFT"
        campaign.current_step = "revision_requested"
        logs.append({"step": "approval", "message": f"Revision requested: {payload.feedback or 'User requested adjustments'}"})

    campaign.step_logs = logs
    db.commit()
    db.refresh(campaign)
    return campaign

@router.post("/{campaign_id}/publish", response_model=CampaignResponse)
def publish_campaign(campaign_id: int, payload: PublishTriggerRequest, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    platforms_to_publish = payload.platforms or campaign.platforms or ["instagram"]

    state: MarketingWorkflowState = {
        "campaign_id": campaign.id,
        "prompt": campaign.prompt,
        "platforms": platforms_to_publish,
        "generated_assets": campaign.generated_assets or {},
        "step_logs": list(campaign.step_logs or []),
        "approval_status": "APPROVED"
    }

    def sync_db(s: MarketingWorkflowState):
        camp = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if camp:
            camp.status = s.get("status", camp.status)
            camp.current_step = s.get("current_step", camp.current_step)
            camp.step_logs = list(s.get("step_logs", []))
            camp.published_records = list(s.get("published_records", []))
            db.commit()

    resume_and_publish_workflow(state, db_updater=sync_db)
    db.refresh(campaign)
    return campaign

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(campaign)
    db.commit()
    return {"message": "Campaign deleted successfully"}
