import edge_tts
import asyncio
import pygame
import os
import time

def speak(text, lang="en"):
    """High-quality neural TTS that supports English, Hindi, and Telugu."""
    if not text or len(text.strip()) == 0:
        return

    # Map languages to appropriate Neural Voices
    if lang == "hi":
        voice = "hi-IN-MadhurNeural"
    elif lang == "te":
        voice = "te-IN-ShrutiNeural"
    else:
        voice = "en-US-GuyNeural"
        
    output_file = "temp_voice.mp3"

    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    try:
        asyncio.run(_generate())
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.quit()
    except Exception as e:
        print(f"TTS Error: {e}")
    finally:
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass