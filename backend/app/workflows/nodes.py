import concurrent.futures
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.workflows.state import MarketingWorkflowState
from app.services.ai_providers import get_ai_provider
from app.services.media_generator import generate_promo_poster
from app.services.bgm_manager import get_bgm_for_mood
from app.services.video_engine import assemble_single_product_video
from app.services.social_publishers import publish_to_platforms_parallel

def add_log(state: MarketingWorkflowState, step_name: str, message: str) -> List[Dict[str, Any]]:
    logs = list(state.get("step_logs", []))
    logs.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "step": step_name,
        "message": message
    })
    return logs

def node_analyze_product(state: MarketingWorkflowState) -> Dict[str, Any]:
    """1. Extracts product USPs, positioning, and buyer persona."""
    ai = get_ai_provider()
    product = state.get("product_data", {})
    prompt = state.get("prompt", "")

    analysis = ai.analyze_product(product, prompt)
    logs = add_log(state, "analyze_product", f"Extracted {len(analysis.get('key_usps', []))} USPs for {product.get('name', 'product')}.")

    return {
        "status": "IN_PROGRESS",
        "current_step": "analyze_product",
        "product_analysis": analysis,
        "step_logs": logs
    }

def node_plan_campaign(state: MarketingWorkflowState) -> Dict[str, Any]:
    """2. Plans creative narrative theme and scene-by-scene storyboard."""
    ai = get_ai_provider()
    analysis = state.get("product_analysis", {})
    meta = {
        "cta": state.get("cta", "Shop Now"),
        "tone": state.get("tone", "Energetic & Modern"),
        "objective": state.get("objective", "Conversions"),
        "language": state.get("language", "English")
    }

    plan = ai.plan_campaign(analysis, meta)
    storyboard = plan.get("storyboard", [])
    logs = add_log(state, "plan_campaign", f"Designed '{plan.get('creative_theme')}' with {len(storyboard)} storyboard scenes.")

    return {
        "current_step": "plan_campaign",
        "campaign_plan": plan,
        "storyboard": storyboard,
        "step_logs": logs
    }

def node_generate_content(state: MarketingWorkflowState) -> Dict[str, Any]:
    """3. Generates platform copy for Instagram, Facebook, and YouTube."""
    ai = get_ai_provider()
    plan = state.get("campaign_plan", {})
    platforms = state.get("platforms", ["instagram", "facebook", "youtube"])
    brand_kit = state.get("brand_kit", {})

    content = ai.generate_social_content(plan, platforms, brand_kit)
    logs = add_log(state, "generate_content", f"Generated content for {', '.join(platforms)}.")

    existing_assets = dict(state.get("generated_assets", {}))
    existing_assets["captions"] = content.get("captions", {})
    existing_assets["carousel_slides"] = content.get("carousel_slides", [])

    return {
        "current_step": "generate_content",
        "generated_assets": existing_assets,
        "step_logs": logs
    }

def node_quality_check(state: MarketingWorkflowState) -> Dict[str, Any]:
    """
    4. Audits text claims and storyboard for compliance BEFORE any media is generated.
    If score is below threshold, routes back to generate_content up to max_qc_retries!
    """
    ai = get_ai_provider()
    product = state.get("product_data", {})
    campaign_data = {
        "analysis": state.get("product_analysis", {}),
        "plan": state.get("campaign_plan", {}),
        "captions": state.get("generated_assets", {}).get("captions", {})
    }

    report = ai.evaluate_quality(campaign_data, product)
    score = report.get("score", 95)
    retries = state.get("qc_retry_count", 0) + 1
    max_retries = state.get("max_qc_retries", 3)

    passed = (score >= 85) or (retries >= max_retries)
    log_msg = f"QC Audit: {score}/100. {'Approved for Media Generation' if passed else f'Revision needed (Attempt {retries}/{max_retries})'}."
    logs = add_log(state, "quality_check", log_msg)

    return {
        "current_step": "quality_check",
        "quality_report": report,
        "qc_passed": passed,
        "qc_retry_count": retries,
        "step_logs": logs
    }

def node_generate_poster(state: MarketingWorkflowState) -> Dict[str, Any]:
    """
    5a. Generates a single poster matching the user's selected poster screen size.
    Runs in parallel with video generation.
    """
    c_id = state.get("campaign_id", 1)
    product = state.get("product_data", {})
    brand_kit = state.get("brand_kit", {})
    poster_format = state.get("poster_format", "1:1")

    product_images = product.get("image_urls", [])
    primary_image = product_images[0] if product_images else None

    price_str = f"Rs. {int(product.get('price', 4999)):,}"
    poster_filename = f"poster_c{c_id}_{poster_format.replace(':', '_')}.jpg"

    poster_info = generate_promo_poster(
        title=product.get("name", "Product Launch"),
        tagline=product.get("tagline", "Special Release"),
        price_text=price_str,
        product_image_url=primary_image,
        brand_kit=brand_kit,
        output_filename=poster_filename,
        poster_format=poster_format
    )

    logs = add_log(state, "generate_poster", f"Rendered single promotional poster ({poster_format} format).")
    return {
        "generated_poster": poster_info,
        "step_logs": logs
    }

def node_generate_video(state: MarketingWorkflowState) -> Dict[str, Any]:
    """
    5b. Generates a single video matching the user's selected video screen size.
    Uses branded background canvas, cycles product images, and changes slide text.
    Runs in parallel with poster generation.
    """
    c_id = state.get("campaign_id", 1)
    product = state.get("product_data", {})
    brand_kit = state.get("brand_kit", {})
    storyboard = state.get("storyboard", [])
    video_format = state.get("video_format", "9:16")

    # Select mood background music from local library / internet
    bgm_path = get_bgm_for_mood(state.get("tone", "upbeat"))

    price_str = f"Rs. {int(product.get('price', 4999)):,}"
    video_filename = f"video_c{c_id}_{video_format.replace(':', '_')}.mp4"

    video_info = assemble_single_product_video(
        product_images=product.get("image_urls", []),
        scenes_metadata=storyboard,
        output_filename=video_filename,
        aspect_ratio=video_format,
        price_tag=price_str,
        brand_kit=brand_kit,
        audio_path=bgm_path,
        fps=20,
        seconds_per_image=2.5,
        transition_seconds=0.5
    )

    logs = add_log(state, "generate_video", f"Rendered product video ({video_format}) with branded slides and mood audio.")
    return {
        "generated_video": video_info,
        "step_logs": logs
    }

def node_combine_media(state: MarketingWorkflowState) -> Dict[str, Any]:
    """Combines parallel outputs from poster and video generation."""
    assets = dict(state.get("generated_assets", {}))
    
    if state.get("generated_poster"):
        assets["posters"] = [state["generated_poster"]]
    if state.get("generated_video"):
        assets["videos"] = [state["generated_video"]]

    logs = add_log(state, "combine_media", "Parallel video & poster generation completed successfully.")

    return {
        "current_step": "media_assembled",
        "generated_assets": assets,
        "step_logs": logs
    }

def node_human_approval(state: MarketingWorkflowState) -> Dict[str, Any]:
    """6. Checkpoint awaiting explicit human approval."""
    approval = state.get("approval_status", "PENDING")
    logs = add_log(state, "human_approval", f"Awaiting human approval gate. Status: {approval}.")

    if approval == "APPROVED":
        status = "APPROVED"
    elif approval == "REJECTED":
        status = "FAILED"
    else:
        status = "WAITING_APPROVAL"

    return {
        "status": status,
        "current_step": "human_approval",
        "step_logs": logs
    }

def node_publish_parallel(state: MarketingWorkflowState) -> Dict[str, Any]:
    """
    7. Parallel publishing upon Human Approval:
       - Instagram: posts both video and poster
       - Facebook: posts both video and poster
       - YouTube: posts only video
    """
    platforms = state.get("platforms", ["instagram", "facebook", "youtube"])
    assets = state.get("generated_assets", {})
    prompt = state.get("prompt", "")

    records = publish_to_platforms_parallel(platforms, assets, fallback_prompt=prompt)
    logs = add_log(state, "publish_parallel", f"Published in parallel to {len(records)} channels (IG, FB, YouTube).")

    return {
        "status": "PUBLISHED",
        "current_step": "published",
        "published_records": records,
        "step_logs": logs
    }
