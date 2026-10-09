import os
import math
import struct
import wave
import requests
from pathlib import Path
from typing import Optional
from app.core.config import settings

BGM_FOLDER = settings.STORAGE_DIR / "bgm"
BGM_FOLDER.mkdir(parents=True, exist_ok=True)

# Royalty-free direct public audio sources categorized by mood
MOOD_DOWNLOAD_URLS = {
    "upbeat": [
        "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=upbeat-112191.mp3",
        "https://actions.google.com/sounds/v1/sports/whistle_cheering.ogg"
    ],
    "lofi": [
        "https://cdn.pixabay.com/download/audio/2022/01/18/audio_d0a13f69d2.mp3?filename=lofi-study-112191.mp3"
    ],
    "ambient": [
        "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3?filename=ambient-piano-amp-strings-10711.mp3"
    ],
    "energetic": [
        "https://cdn.pixabay.com/download/audio/2022/10/14/audio_9939f77cb7.mp3?filename=energetic-hip-hop-8303.mp3"
    ]
}

def create_fallback_mood_track(filepath: Path, mood: str, duration: float = 12.0):
    """Generates an initial clean harmonic mood backing track in case offline."""
    sample_rate = 44100
    total_samples = int(sample_rate * duration)
    
    if "lofi" in mood:
        base_freqs = [261.63, 329.63, 392.00, 493.88] # Cmaj7
    elif "ambient" in mood or "luxury" in mood:
        base_freqs = [196.00, 293.66, 392.00, 440.00]
    else: # upbeat / energetic
        base_freqs = [261.63, 329.63, 392.00, 523.25]

    samples = []
    for i in range(total_samples):
        t = i / sample_rate
        val = 0.0
        for f in base_freqs:
            val += math.sin(2 * math.pi * f * t) * 0.25
        
        # Fade out
        fade = 1.0
        if t > (duration - 1.0):
            fade = max(0.0, (duration - t) / 1.0)
        sample_int = int(32767 * val * 0.7 * fade)
        samples.append(max(-32768, min(32767, sample_int)))

    with wave.open(str(filepath), "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(struct.pack(f"<{len(samples)}h", *samples))

def get_bgm_for_mood(mood: str = "upbeat") -> Optional[str]:
    """
    Selects or downloads royalty-free background music matching the campaign mood.
    Returns the absolute path to the local audio file.
    """
    normalized_mood = "upbeat"
    mood_lower = mood.lower()
    if "lofi" in mood_lower or "chill" in mood_lower:
        normalized_mood = "lofi"
    elif "ambient" in mood_lower or "luxury" in mood_lower or "calm" in mood_lower:
        normalized_mood = "ambient"
    elif "energetic" in mood_lower or "modern" in mood_lower:
        normalized_mood = "energetic"

    target_file = BGM_FOLDER / f"{normalized_mood}.wav"
    
    if target_file.exists() and target_file.stat().st_size > 5000:
        return str(target_file)

    # Try downloading from royalty-free source if internet available
    urls = MOOD_DOWNLOAD_URLS.get(normalized_mood, [])
    downloaded = False
    for url in urls:
        try:
            resp = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200 and len(resp.content) > 5000:
                with open(target_file, "wb") as f:
                    f.write(resp.content)
                downloaded = True
                break
        except Exception:
            continue

    if not downloaded:
        # Cache clean harmonic mood track locally
        create_fallback_mood_track(target_file, normalized_mood, duration=12.0)

    return str(target_file)
