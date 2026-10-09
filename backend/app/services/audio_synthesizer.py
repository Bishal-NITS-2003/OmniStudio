import math
import struct
import wave
from pathlib import Path
from app.core.config import settings

AUDIO_CACHE_DIR = settings.STORAGE_DIR / "generated" / "audio"
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)

def generate_background_music(mood: str = "upbeat", duration_seconds: float = 12.0) -> str:
    """
    Generates a procedural background music WAV file with chord progressions and rhythm.
    Supports 'upbeat', 'lofi', 'electronic', 'ambient'.
    Returns the absolute path to the generated WAV file.
    """
    mood = mood.lower()
    filename = f"bgm_{mood}_{int(duration_seconds)}s.wav"
    filepath = AUDIO_CACHE_DIR / filename
    if filepath.exists() and filepath.stat().st_size > 1000:
        return str(filepath)

    sample_rate = 44100
    total_samples = int(sample_rate * duration_seconds)

    # Chord root frequencies (in Hz)
    # E.g. Upbeat: C - G - Am - F progression
    if "lofi" in mood:
        chords = [
            [261.63, 329.63, 392.00, 493.88],  # Cmaj7
            [220.00, 261.63, 329.63, 392.00],  # Am7
            [174.61, 220.00, 261.63, 329.63],  # Fmaj7
            [196.00, 246.94, 293.66, 349.23],  # G7
        ]
        tempo_bpm = 85
    elif "electronic" in mood or "energetic" in mood or "upbeat" in mood:
        chords = [
            [261.63, 329.63, 392.00, 523.25],  # C
            [196.00, 246.94, 293.66, 392.00],  # G
            [220.00, 261.63, 329.63, 440.00],  # Am
            [174.61, 220.00, 261.63, 349.23],  # F
        ]
        tempo_bpm = 124
    else: # Ambient / Luxury
        chords = [
            [196.00, 293.66, 392.00, 440.00],
            [174.61, 261.63, 349.23, 440.00],
            [220.00, 261.63, 329.63, 392.00],
            [146.83, 220.00, 293.66, 369.99],
        ]
        tempo_bpm = 95

    seconds_per_beat = 60.0 / tempo_bpm
    samples_per_beat = int(sample_rate * seconds_per_beat)
    beats_per_chord = 4

    samples = []
    current_chord_idx = 0

    for i in range(total_samples):
        beat_idx = i // samples_per_beat
        chord_idx = (beat_idx // beats_per_chord) % len(chords)
        active_chord = chords[chord_idx]

        # Pos in beat (for rhythmic percussion)
        sub_beat_pos = (i % samples_per_beat) / samples_per_beat

        # 1. Harmonic synthesis (soft sine + slight warm harmonic)
        t = i / sample_rate
        chord_signal = 0.0
        for freq in active_chord:
            note_env = 0.7 + 0.3 * math.sin(2 * math.pi * 3 * t)  # subtle chorus tremolo
            chord_signal += (math.sin(2 * math.pi * freq * t) * 0.4 +
                             math.sin(2 * math.pi * (freq * 2) * t) * 0.15) * note_env

        chord_signal = chord_signal / len(active_chord)

        # 2. Rhythmic bass pulse on downbeats
        bass_freq = active_chord[0] / 2.0
        bass_decay = math.exp(-6.0 * sub_beat_pos)
        bass_signal = math.sin(2 * math.pi * bass_freq * t) * bass_decay * 0.4

        # 3. Soft click / hi-hat on every 8th note
        eighth_pos = ((i * 2) % samples_per_beat) / (samples_per_beat / 2)
        hihat = (math.sin(2 * math.pi * 3200 * t) * math.exp(-25.0 * eighth_pos)) * 0.12

        # Combined signal
        signal = (chord_signal * 0.5 + bass_signal * 0.35 + hihat * 0.15)

        # Smooth fade-in (1st 0.5s) and fade-out (last 1.0s)
        fade = 1.0
        if t < 0.5:
            fade = t / 0.5
        elif t > (duration_seconds - 1.0):
            fade = max(0.0, (duration_seconds - t) / 1.0)

        sample_val = int(32767 * 0.8 * signal * fade)
        sample_val = max(-32768, min(32767, sample_val))
        samples.append(sample_val)

    with wave.open(str(filepath), "w") as wav_out:
        wav_out.setnchannels(1)
        wav_out.setsampwidth(2)
        wav_out.setframerate(sample_rate)
        # Pack frames
        raw_bytes = struct.pack(f"<{len(samples)}h", *samples)
        wav_out.writeframes(raw_bytes)

    return str(filepath)
