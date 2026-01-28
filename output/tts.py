# =========================================================
# Async-safe TTS for FastAPI (edge-tts)
# ONE FILE PER REQUEST (NO COLLISION)
# =========================================================

import edge_tts
import os

async def speak(text: str, lang: str, output_file: str):
    """
    Async TTS function.
    Each request writes to its OWN mp3 file.
    """

    if not text or not text.strip():
        return

    voice = "en-US-AriaNeural"
    if lang.startswith("hi"):
        voice = "hi-IN-SwaraNeural"
    elif lang.startswith("te"):
        voice = "te-IN-ShrutiNeural"

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    await communicate.save(output_file)
