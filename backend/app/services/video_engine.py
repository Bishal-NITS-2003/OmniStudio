import os
import io
import math
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import requests
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from app.core.config import settings

VIDEO_OUT_DIR = settings.STORAGE_DIR / "generated" / "videos"
VIDEO_OUT_DIR.mkdir(parents=True, exist_ok=True)

ASPECT_RATIOS = {
    "9:16": (720, 1280),
    "16:9": (1280, 720),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
}

_IMAGE_CACHE: Dict[str, Image.Image] = {}

def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join([c * 2 for c in hex_code])
    if len(hex_code) != 6:
        return (99, 102, 241)
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4)) # type: ignore

def load_image(src: str) -> Image.Image:
    """Load image from a local path, URL, or fallback placeholder."""
    if src in _IMAGE_CACHE:
        return _IMAGE_CACHE[src].copy()

    if src.startswith("http://") or src.startswith("https://"):
        try:
            resp = requests.get(src, timeout=5)
            if resp.status_code == 200:
                img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
                _IMAGE_CACHE[src] = img
                return img.copy()
        except Exception:
            pass
    elif os.path.exists(src):
        try:
            img = Image.open(src).convert("RGBA")
            _IMAGE_CACHE[src] = img
            return img.copy()
        except Exception:
            pass

    # Fallback placeholder
    img = Image.new("RGBA", (800, 800), color=(30, 27, 75, 255))
    return img

def create_branded_background(
    target_size: Tuple[int, int],
    brand_kit: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """
    Creates a premium commercial branded background canvas using the brand kit colors
    of the exact required video aspect ratio.
    """
    w, h = target_size
    bg_rgb = hex_to_rgb(brand_kit.get("background_color", "#0f172a")) if brand_kit else (15, 23, 42)
    prim_rgb = hex_to_rgb(brand_kit.get("primary_color", "#6366f1")) if brand_kit else (99, 102, 241)
    accent_rgb = hex_to_rgb(brand_kit.get("accent_color", "#06b6d4")) if brand_kit else (6, 182, 212)

    # Base background
    canvas = Image.new("RGBA", (w, h), (*bg_rgb, 255))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Radial ambient glow top-left (Primary brand color)
    draw.ellipse(
        [-int(w * 0.2), -int(h * 0.1), int(w * 0.8), int(h * 0.5)],
        fill=(*prim_rgb, 50)
    )

    # Radial ambient glow center-right (Accent brand color)
    draw.ellipse(
        [int(w * 0.3), int(h * 0.4), int(w * 1.3), int(h * 0.95)],
        fill=(*accent_rgb, 40)
    )

    # Bottom dark gradient vignette for readable text
    gradient_height = int(h * 0.42)
    for y in range(gradient_height):
        alpha = int(220 * (y / gradient_height))
        draw.line([(0, h - gradient_height + y), (w, h - gradient_height + y)], fill=(11, 15, 25, alpha))

    # Subtle top brand bar
    draw.line([(0, 0), (w, 0)], fill=(*prim_rgb, 255), width=4)

    return Image.alpha_composite(canvas, overlay)

def render_slide_frame(
    branded_bg: Image.Image,
    product_img: Image.Image,
    title: str = "",
    subtitle: str = "",
    badge: str = "",
    price_tag: str = "",
    brand_kit: Optional[Dict[str, Any]] = None,
    zoom_progress: float = 0.0
) -> Image.Image:
    """
    Composes a single slide:
    - Uses the persistent branded background
    - Pastes the product image in the center/upper frame with smooth subtle zoom
    - Overlays changing scene badge, title, subtitle, and price
    """
    canvas = branded_bg.copy()
    w, h = canvas.size
    prim_rgb = hex_to_rgb(brand_kit.get("primary_color", "#6366f1")) if brand_kit else (99, 102, 241)

    # Fonts
    try:
        font_large = ImageFont.truetype("arialbd.ttf", size=max(26, int(h * 0.036)))
        font_small = ImageFont.truetype("arial.ttf", size=max(18, int(h * 0.024)))
        font_badge = ImageFont.truetype("arialbd.ttf", size=max(15, int(h * 0.018)))
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # 1. Product Showcase Area (Center / Upper)
    p_box_size = int(min(w, h) * 0.52 * (1.0 + 0.04 * zoom_progress))
    p_copy = product_img.copy()
    p_copy.thumbnail((p_box_size, p_box_size), Image.Resampling.BILINEAR)

    center_x = w // 2
    center_y = int(h * 0.44) if h > w else int(h * 0.48)
    px = center_x - (p_copy.width // 2)
    py = center_y - (p_copy.height // 2)

    # Drop shadow below product
    shadow = Image.new("RGBA", (p_copy.width + 30, p_copy.height + 30), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([10, 10, p_copy.width + 20, p_copy.height + 20], fill=(0, 0, 0, 120))
    canvas.paste(shadow, (px - 15, py - 5), shadow)
    canvas.paste(p_copy, (px, py), p_copy)

    draw = ImageDraw.Draw(canvas, "RGBA")

    # 2. Top Scene Badge
    if badge:
        b_text = badge.upper()
        bbox = draw.textbbox((0, 0), b_text, font=font_badge)
        bw = bbox[2] - bbox[0] + 28
        bh = bbox[3] - bbox[1] + 14
        bx = int(w * 0.08)
        by = int(h * 0.08)

        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(*prim_rgb, 240))
        draw.text((bx + 14, by + 7), b_text, font=font_badge, fill=(255, 255, 255, 255))

    # 3. Price Tag Pill (if provided)
    if price_tag:
        p_text = price_tag
        bbox_p = draw.textbbox((0, 0), p_text, font=font_badge)
        pw = bbox_p[2] - bbox_p[0] + 24
        ph = bbox_p[3] - bbox_p[1] + 12
        pbx = w - int(w * 0.08) - pw
        pby = int(h * 0.08)
        draw.rounded_rectangle([pbx, pby, pbx + pw, pby + ph], radius=8, fill=(15, 23, 42, 220), outline=(*prim_rgb, 200), width=1)
        draw.text((pbx + 12, pby + 6), p_text, font=font_badge, fill=(255, 255, 255, 255))

    # 4. Bottom Changing Slide Text (Title & Subtitle)
    if title or subtitle:
        text_y = int(h * 0.76)
        text_x = int(w * 0.08)

        if title:
            draw.text((text_x + 2, text_y + 2), title[:40], font=font_large, fill=(0, 0, 0, 220))
            draw.text((text_x, text_y), title[:40], font=font_large, fill=(255, 255, 255, 255))
            text_y += int(h * 0.052)

        if subtitle:
            draw.text((text_x + 1, text_y + 1), subtitle[:65], font=font_small, fill=(0, 0, 0, 180))
            draw.text((text_x, text_y), subtitle[:65], font=font_small, fill=(226, 232, 240, 240))

    return canvas.convert("RGB")

def crossfade_frames(
    img1: Image.Image,
    img2: Image.Image,
    steps: int
) -> List[Image.Image]:
    """Blends between two frames for smooth slide transitions."""
    frames = []
    for step in range(steps):
        alpha = (step + 1) / (steps + 1)
        blended = Image.blend(img1, img2, alpha)
        frames.append(blended)
    return frames

def assemble_single_product_video(
    product_images: List[str],
    scenes_metadata: List[Dict[str, Any]],
    output_filename: str,
    aspect_ratio: str = "9:16",
    price_tag: str = "",
    brand_kit: Optional[Dict[str, Any]] = None,
    audio_path: Optional[str] = None,
    fps: int = 20,
    seconds_per_image: float = 2.5,
    transition_seconds: float = 0.5
) -> Dict[str, Any]:
    """
    Assembles the product video based on user's exact specification:
    - Creates a branded background of the requested size based on brand kit colors.
    - Reuses the SAME branded background across multiple slides.
    - Pastes one product image per slide, cycling through available product images.
    - Changes the text on each slide as per the storyboard.
    - Renders smooth transitions and muxes mood background music.
    """
    target_size = ASPECT_RATIOS.get(aspect_ratio, (720, 1280))
    tw, th = target_size
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # Create the persistent branded background
    branded_bg = create_branded_background(target_size, brand_kit)

    # Pre-load product images
    if not product_images:
        product_images = ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80"]
    loaded_product_imgs = [load_image(src) for src in product_images]

    frames_per_scene = int(fps * seconds_per_image)
    transition_frames_count = max(3, int(fps * transition_seconds))

    num_scenes = max(len(scenes_metadata), len(loaded_product_imgs), 3)
    rendered_frames: List[Image.Image] = []

    for i in range(num_scenes):
        meta = scenes_metadata[i] if i < len(scenes_metadata) else {}
        title = meta.get("title", f"Feature Highlight 0{i+1}")
        subtitle = meta.get("subtitle", "Engineered for maximum reliability")
        badge = meta.get("badge", f"SLIDE 0{i+1}")

        # Cycle product image across slides
        p_img = loaded_product_imgs[i % len(loaded_product_imgs)]

        # Generate frames for current slide
        slide_frames = []
        for f in range(frames_per_scene):
            progress = f / max(1, frames_per_scene - 1)
            frame = render_slide_frame(
                branded_bg=branded_bg,
                product_img=p_img,
                title=title,
                subtitle=subtitle,
                badge=badge,
                price_tag=price_tag,
                brand_kit=brand_kit,
                zoom_progress=progress
            )
            slide_frames.append(frame)

        if i < num_scenes - 1:
            # Prepare start of next slide for transition
            next_meta = scenes_metadata[i + 1] if (i + 1) < len(scenes_metadata) else {}
            next_p_img = loaded_product_imgs[(i + 1) % len(loaded_product_imgs)]
            next_start_frame = render_slide_frame(
                branded_bg=branded_bg,
                product_img=next_p_img,
                title=next_meta.get("title", f"Feature 0{i+2}"),
                subtitle=next_meta.get("subtitle", ""),
                badge=next_meta.get("badge", f"SLIDE 0{i+2}"),
                price_tag=price_tag,
                brand_kit=brand_kit,
                zoom_progress=0.0
            )

            rendered_frames.extend(slide_frames[:-transition_frames_count])
            transitions = crossfade_frames(
                slide_frames[-1],
                next_start_frame,
                steps=transition_frames_count
            )
            rendered_frames.extend(transitions)
        else:
            rendered_frames.extend(slide_frames)

    total_frames = len(rendered_frames)
    duration_secs = round(total_frames / fps, 2)

    output_path = VIDEO_OUT_DIR / output_filename
    temp_video_path = VIDEO_OUT_DIR / f"temp_{output_filename}"
    target_mp4 = temp_video_path if (audio_path and os.path.exists(audio_path)) else output_path

    # Pipe raw frames to FFmpeg
    cmd_video = [
        ffmpeg_exe,
        "-y",
        "-loglevel", "quiet",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{tw}x{th}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "ultrafast",
        "-crf", "24",
        str(target_mp4)
    ]

    proc = subprocess.Popen(cmd_video, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for frame in rendered_frames:
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    proc.wait()

    # Mux BGM audio if available
    if audio_path and os.path.exists(audio_path):
        cmd_mux = [
            ffmpeg_exe,
            "-y",
            "-loglevel", "quiet",
            "-i", str(temp_video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            str(output_path)
        ]
        subprocess.run(cmd_mux, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if temp_video_path.exists():
            try:
                temp_video_path.unlink()
            except Exception:
                pass

    return {
        "filename": output_filename,
        "url": f"/api/static/generated/videos/{output_filename}",
        "filepath": str(output_path),
        "aspect_ratio": aspect_ratio,
        "resolution": f"{tw}x{th}",
        "duration_seconds": duration_secs,
        "fps": fps,
        "num_scenes": num_scenes,
        "has_audio": bool(audio_path and os.path.exists(audio_path))
    }
