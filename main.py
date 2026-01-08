import time
import winsound
import asyncio
import pygame
import os
import edge_tts

from core.state_manager import StateManager
from core.intent_engine import detect_intent
from core.memory import Memory

from perception.audio_input import record_audio
from perception.speech_to_text import transcribe
from perception.vision import count_people

from reasoning.gemini_brain import ask
from utils.language import detect_language, is_valid_speech

# --- HIGH QUALITY NEURAL VOICE ENGINE ---
def speak(text, lang="en"):
    """Converts text to speech and plays it aloud."""
    # Select Neural Voice: hi-IN-MadhurNeural (Hindi) or en-US-GuyNeural (English)
    voice = "hi-IN-MadhurNeural" if lang == "hi" else "en-US-GuyNeural"
    output_file = "response_audio.mp3"

    async def generate_speech():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)

    # Generate the MP3 file using Edge-TTS
    asyncio.run(generate_speech())

    # Play the audio using Pygame
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.quit()
    
    # Cleanup file
    if os.path.exists(output_file):
        os.remove(output_file)

# --- AUDIO FEEDBACK (BEEPS) ---
def play_beep(freq, duration):
    winsound.Beep(freq, duration)

# -------------------------
# 1. INITIALIZE & STARTUP
# -------------------------
state = StateManager()
memory = Memory()

print("Second Brain is starting...")

# Startup Cue: Beep + Voice
play_beep(1000, 500) 
speak("Hi, how can I help you?", "en")

# -------------------------
# 2. LISTENING STATE
# -------------------------
state.set_state(StateManager.LISTENING)
play_beep(800, 200) # Small "ready" beep
print("System is listening...")
record_audio("input.wav", duration=5)

# -------------------------
# 3. PROCESSING STATE
# -------------------------
state.set_state(StateManager.PROCESSING)
play_beep(600, 300) # Processing beep
text = transcribe("input.wav")
print("User said:", text)

if not is_valid_speech(text):
    speak("I'm sorry, I didn't catch that. Please repeat clearly.", "en")
    exit()

lang = detect_language(text)
intent = detect_intent(text)

# -------------------------
# 4. RESPONDING STATE
# -------------------------
state.set_state(StateManager.RESPONDING)

if intent == "VISION":
    count = count_people()
    if count is None:
        response = "The camera is not accessible right now." if lang == "en" else "कैमरा उपलब्ध नहीं है।"
    else:
        response = (
            f"There are {count} people in front of you."
            if lang == "en"
            else f"आपके सामने {count} लोग हैं।"
        )
else:
    # Get response from Gemini Brain
    response = ask(text, lang)

# 🔊 SPEAK THE ANSWER LOUDLY
print("Brain Response:", response)
speak(response, lang)

# -------------------------
# 5. BACK TO IDLE
# -------------------------
state.set_state(StateManager.IDLE)
play_beep(400, 200) # Closing beep
print("System Idle.")