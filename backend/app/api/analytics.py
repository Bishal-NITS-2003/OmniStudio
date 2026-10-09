from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.product import Product
from app.models.campaign import Campaign
from app.models.publishing import PublishingAccount

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    products_count = db.query(Product).count()
    campaigns = db.query(Campaign).all()
    accounts_count = db.query(PublishingAccount).filter(PublishingAccount.is_connected == True).count()

    total_campaigns = len(campaigns)
    published_count = sum(1 for c in campaigns if c.status == "PUBLISHED")
    waiting_approval_count = sum(1 for c in campaigns if c.status == "WAITING_APPROVAL")
    in_progress_count = sum(1 for c in campaigns if c.status == "IN_PROGRESS")

    total_videos = 0
    qc_scores = []
    platform_counts = {"instagram": 0, "tiktok": 0, "youtube": 0, "linkedin": 0}

    for c in campaigns:
        assets = c.generated_assets or {}
        videos = assets.get("videos", [])
        total_videos += len(videos)

        qc = c.quality_report or {}
        if "score" in qc:
            qc_scores.append(qc["score"])

        for plat in (c.platforms or []):
            if plat in platform_counts:
                platform_counts[plat] += 1

    avg_qc_score = round(sum(qc_scores) / len(qc_scores), 1) if qc_scores else 95.0

    return {
        "products_count": products_count,
        "total_campaigns": total_campaigns,
        "published_campaigns": published_count,
        "waiting_approval": waiting_approval_count,
        "in_progress": in_progress_count,
        "connected_accounts": accounts_count,
        "total_videos_rendered": total_videos,
        "average_qc_score": avg_qc_score,
        "platform_distribution": platform_counts,
        "estimated_reach_multiplier": f"{round(1.4 + (published_count * 0.3), 1)}x"
    }
