import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.workflows.state import MarketingWorkflowState
from app.workflows.graph import run_campaign_workflow, resume_and_publish_workflow

def test_workflow_end_to_end():
    sample_state: MarketingWorkflowState = {
        "campaign_id": 999,
        "prompt": "Test campaign for high performance wireless headphones",
        "target_audience": "Tech enthusiasts",
        "tone": "Energetic",
        "language": "English",
        "objective": "Conversions",
        "cta": "Buy Now",
        "platforms": ["instagram", "facebook", "youtube"],
        "formats": ["reels_9_16"],
        "video_format": "9:16",
        "poster_format": "1:1",
        "product_data": {
            "name": "Test SoundPro",
            "tagline": "Superior Studio Sound",
            "description": "Headphones with active noise cancelation.",
            "category": "Electronics",
            "price": 4999.0,
            "currency": "Rs.",
            "features": ["ANC 40dB", "30-hr battery"],
            "image_urls": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80"]
        },
        "brand_kit": {
            "name": "OmniBrand",
            "primary_color": "#6366f1",
            "secondary_color": "#ec4899",
            "accent_color": "#06b6d4",
            "background_color": "#0f172a"
        }
    }

    final_state = run_campaign_workflow(sample_state)

    # Validate analysis output
    assert "product_analysis" in final_state
    assert len(final_state["product_analysis"].get("key_usps", [])) > 0

    # Validate campaign plan & storyboard
    assert "campaign_plan" in final_state
    assert len(final_state["storyboard"]) > 0

    # Validate multi-format content
    assert "generated_assets" in final_state
    captions = final_state["generated_assets"].get("captions", {})
    assert "instagram" in captions
    assert "facebook" in captions
    assert "youtube" in captions

    # Validate QC check was executed before media generation
    assert "quality_report" in final_state
    assert final_state["quality_report"]["score"] >= 80
    assert final_state.get("qc_passed") is True

    # Validate media assembly (video + poster)
    assert "generated_poster" in final_state
    assert "generated_video" in final_state
    assert Path(final_state["generated_video"]["filepath"]).exists()
    assert Path(final_state["generated_poster"]["filepath"]).exists()

    # Validate human approval checkpoint
    assert final_state["status"] == "WAITING_APPROVAL"

    # Test resume & parallel publishing
    # (Instagram: 2 posts [video+poster], Facebook: 2 posts [video+poster], YouTube: 1 post [video] -> 3 platform records, 5 posts total)
    published_state = resume_and_publish_workflow(final_state)
    assert published_state["status"] == "PUBLISHED"
    assert len(published_state["published_records"]) == 3
    total_posts = sum(len(r.get("posts", [])) for r in published_state["published_records"])
    assert total_posts == 5

