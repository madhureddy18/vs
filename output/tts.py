import edge_tts
import os
import asyncio

TMP_DIR = "/tmp"
os.makedirs(TMP_DIR, exist_ok=True)

TTS_TIMEOUT = 15  # seconds


async def speak(text: str, lang: str, output_file: str):
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

    await asyncio.wait_for(
        communicate.save(output_file),
        timeout=TTS_TIMEOUT
    )
