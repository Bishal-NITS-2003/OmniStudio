import uuid
import concurrent.futures
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import requests
from app.core.config import settings

class InstagramPublisher:
    """Publishes BOTH video (Reel) and poster image to Instagram."""
    platform_name = "instagram"

    def publish(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        caption = payload.get("caption", "")
        video_url = payload.get("video_url")
        poster_url = payload.get("poster_url")
        access_token = settings.META_ACCESS_TOKEN

        posts_created = []

        # 1. Post Poster Image (Feed)
        if poster_url:
            mock_post_id = f"ig_post_{uuid.uuid4().hex[:8]}"
            posts_created.append({
                "type": "POSTER_POST",
                "post_id": mock_post_id,
                "url": f"https://instagram.com/p/{mock_post_id}",
                "media_url": poster_url,
                "status": "PUBLISHED"
            })

        # 2. Post Video (Reel)
        if video_url:
            mock_reel_id = f"ig_reel_{uuid.uuid4().hex[:8]}"
            posts_created.append({
                "type": "REELS_VIDEO",
                "post_id": mock_reel_id,
                "url": f"https://instagram.com/reel/{mock_reel_id}",
                "media_url": video_url,
                "status": "PUBLISHED"
            })

        return {
            "platform": "instagram",
            "status": "PUBLISHED",
            "posts": posts_created,
            "external_post_id": posts_created[0]["post_id"] if posts_created else "ig_ok",
            "post_url": posts_created[0]["url"] if posts_created else "https://instagram.com",
            "is_mock": True,
            "notes": "Published both Feed Poster and Reels Video to Instagram"
        }

class FacebookPublisher:
    """Publishes BOTH video and poster image to Facebook Page."""
    platform_name = "facebook"

    def publish(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        caption = payload.get("caption", "")
        video_url = payload.get("video_url")
        poster_url = payload.get("poster_url")

        posts_created = []

        if poster_url:
            mock_photo_id = f"fb_photo_{uuid.uuid4().hex[:8]}"
            posts_created.append({
                "type": "FEED_POSTER",
                "post_id": mock_photo_id,
                "url": f"https://facebook.com/posts/{mock_photo_id}",
                "media_url": poster_url,
                "status": "PUBLISHED"
            })

        if video_url:
            mock_vid_id = f"fb_vid_{uuid.uuid4().hex[:8]}"
            posts_created.append({
                "type": "PAGE_VIDEO",
                "post_id": mock_vid_id,
                "url": f"https://facebook.com/watch/?v={mock_vid_id}",
                "media_url": video_url,
                "status": "PUBLISHED"
            })

        return {
            "platform": "facebook",
            "status": "PUBLISHED",
            "posts": posts_created,
            "external_post_id": posts_created[0]["post_id"] if posts_created else "fb_ok",
            "post_url": posts_created[0]["url"] if posts_created else "https://facebook.com",
            "is_mock": True,
            "notes": "Published both Feed Poster and Video to Facebook"
        }

class YouTubePublisher:
    """Publishes ONLY video (Shorts / Video) to YouTube."""
    platform_name = "youtube"

    def publish(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        video_url = payload.get("video_url")
        mock_id = f"yt_{uuid.uuid4().hex[:11]}"

        return {
            "platform": "youtube",
            "status": "PUBLISHED",
            "posts": [{
                "type": "SHORTS_VIDEO",
                "post_id": mock_id,
                "url": f"https://youtube.com/shorts/{mock_id}",
                "media_url": video_url,
                "status": "PUBLISHED"
            }],
            "external_post_id": mock_id,
            "post_url": f"https://youtube.com/shorts/{mock_id}",
            "is_mock": True,
            "notes": "Published Video to YouTube Shorts"
        }

PUBLISHERS = {
    "instagram": InstagramPublisher(),
    "facebook": FacebookPublisher(),
    "youtube": YouTubePublisher(),
}

def publish_single_platform(platform: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    adapter = PUBLISHERS.get(platform.lower())
    if not adapter:
        return {
            "platform": platform,
            "status": "FAILED",
            "error_message": f"Platform '{platform}' not supported. Only YouTube, Instagram, and Facebook are supported."
        }
    return adapter.publish(payload)

def publish_to_platforms_parallel(
    platforms: List[str],
    assets: Dict[str, Any],
    fallback_prompt: str = ""
) -> List[Dict[str, Any]]:
    """
    Executes parallel publishing workflow across approved platforms (Instagram, Facebook, YouTube).
    - Instagram: posts both video and poster
    - Facebook: posts both video and poster
    - YouTube: posts only video
    """
    # Filter to only allowed platforms: youtube, instagram, facebook
    allowed = [p.lower() for p in platforms if p.lower() in ("instagram", "facebook", "youtube")]
    if not allowed:
        allowed = ["instagram", "facebook", "youtube"]

    captions = assets.get("captions", {})
    videos = assets.get("videos", [])
    posters = assets.get("posters", [])

    primary_video_url = videos[0].get("url") if videos else ""
    primary_poster_url = posters[0].get("url") if posters else ""

    tasks = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for plat in allowed:
            plat_caption = captions.get(plat, {}).get("caption", fallback_prompt)
            payload = {
                "caption": plat_caption,
                "video_url": primary_video_url,
                "poster_url": primary_poster_url
            }
            future = executor.submit(publish_single_platform, plat, payload)
            tasks[future] = plat

        results = []
        for future in concurrent.futures.as_completed(tasks):
            try:
                res = future.result()
                results.append(res)
            except Exception as e:
                plat_name = tasks[future]
                results.append({
                    "platform": plat_name,
                    "status": "FAILED",
                    "error_message": str(e)
                })

    return results
