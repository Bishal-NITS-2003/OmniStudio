import os
import io
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import requests
from PIL import Image, ImageDraw, ImageFont
from app.core.config import settings

IMAGES_OUT_DIR = settings.STORAGE_DIR / "generated" / "images"
IMAGES_OUT_DIR.mkdir(parents=True, exist_ok=True)

POSTER_DIMENSIONS = {
    "1:1": (1080, 1080),
    "square_1_1": (1080, 1080),
    "4:5": (1080, 1350),
    "portrait_4_5": (1080, 1350),
    "16:9": (1920, 1080),
    "landscape_16_9": (1920, 1080),
    "9:16": (1080, 1920),
    "reels_9_16": (1080, 1920),
}

def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join([c * 2 for c in hex_code])
    if len(hex_code) != 6:
        return (99, 102, 241)
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4)) # type: ignore

def generate_promo_poster(
    title: str,
    tagline: str,
    price_text: str,
    product_image_url: Optional[str],
    brand_kit: Optional[Dict[str, Any]],
    output_filename: str,
    poster_format: str = "1:1"
) -> Dict[str, Any]:
    """
    Renders a single promotional marketing poster matching the user's selected screen size.
    """
    w, h = POSTER_DIMENSIONS.get(poster_format, (1080, 1080))
    primary_color = (99, 102, 241)
    bg_color = (15, 23, 42)
    accent_color = (6, 182, 212)

    if brand_kit:
        primary_color = hex_to_rgb(brand_kit.get("primary_color", "#6366f1"))
        bg_color = hex_to_rgb(brand_kit.get("background_color", "#0f172a"))
        accent_color = hex_to_rgb(brand_kit.get("accent_color", "#06b6d4"))

    # Create branded background
    base = Image.new("RGB", (w, h), bg_color)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([int(w * 0.1), int(h * 0.15), int(w * 0.9), int(h * 0.75)], fill=(*primary_color, 45))
    glow_draw.ellipse([int(w * 0.3), int(h * 0.4), int(w * 0.95), int(h * 0.9)], fill=(*accent_color, 35))
    base = Image.alpha_composite(base.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(base, "RGBA")

    # Font setup
    try:
        font_title = ImageFont.truetype("arialbd.ttf", size=max(36, int(h * 0.048)))
        font_sub = ImageFont.truetype("arial.ttf", size=max(22, int(h * 0.026)))
        font_badge = ImageFont.truetype("arialbd.ttf", size=max(18, int(h * 0.022)))
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Brand Header Pill
    brand_name = brand_kit.get("name", "OMNIPOST AI") if brand_kit else "OMNIPOST AI"
    draw.rounded_rectangle([int(w * 0.08), int(h * 0.06), int(w * 0.08) + 240, int(h * 0.06) + 42], radius=8, fill=(255, 255, 255, 25))
    draw.text((int(w * 0.08) + 16, int(h * 0.06) + 11), brand_name.upper(), font=font_badge, fill=(255, 255, 255, 240))

    # Place product image
    prod_box_size = int(min(w, h) * 0.52)
    center_x = w // 2
    center_y = int(h * 0.44)

    p_img = None
    if product_image_url:
        try:
            if product_image_url.startswith("http"):
                resp = requests.get(product_image_url, timeout=5)
                p_img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            elif os.path.exists(product_image_url):
                p_img = Image.open(product_image_url).convert("RGBA")
        except Exception:
            p_img = None

    if p_img:
        p_img.thumbnail((prod_box_size, prod_box_size), Image.Resampling.BILINEAR)
        px = center_x - (p_img.width // 2)
        py = center_y - (p_img.height // 2)

        shadow = Image.new("RGBA", (p_img.width + 40, p_img.height + 40), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.ellipse([10, 10, p_img.width + 30, p_img.height + 30], fill=(0, 0, 0, 120))
        base.paste(shadow, (px - 20, py - 10), shadow)
        base.paste(p_img, (px, py), p_img)
    else:
        draw.rounded_rectangle(
            [center_x - prod_box_size//2, center_y - prod_box_size//2, center_x + prod_box_size//2, center_y + prod_box_size//2],
            radius=24,
            fill=(*primary_color, 80),
            outline=(*accent_color, 200),
            width=3
        )

    # Price Tag Badge in Rs.
    if price_text:
        price_badge_w = 210
        price_badge_h = 52
        pbx = int(w * 0.70)
        pby = int(h * 0.20)
        draw.rounded_rectangle([pbx, pby, pbx + price_badge_w, pby + price_badge_h], radius=12, fill=(*accent_color, 240))
        draw.text((pbx + 22, pby + 14), price_text, font=font_badge, fill=(15, 23, 42, 255))

    # Bottom Content Area
    bot_y = int(h * 0.76)
    draw.text((int(w * 0.08), bot_y), title[:36], font=font_title, fill=(255, 255, 255, 255))
    if tagline:
        draw.text((int(w * 0.08), bot_y + int(h * 0.055)), tagline[:65], font=font_sub, fill=(203, 213, 225, 230))

    # CTA Button
    cta_w = 210
    cta_h = 52
    cx = int(w * 0.08)
    cy = int(h * 0.88)
    draw.rounded_rectangle([cx, cy, cx + cta_w, cy + cta_h], radius=10, fill=(*primary_color, 255))
    draw.text((cx + 36, cy + 15), "SHOP NOW →", font=font_badge, fill=(255, 255, 255, 255))

    out_path = IMAGES_OUT_DIR / output_filename
    base.save(str(out_path), quality=95)

    return {
        "filename": output_filename,
        "url": f"/api/static/generated/images/{output_filename}",
        "filepath": str(out_path),
        "dimensions": f"{w}x{h}",
        "aspect_ratio": poster_format
    }
