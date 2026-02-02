import sys
import time

from perception.audio_input import record_audio  # laptop mic
from perception.speech_to_text import transcribe
from perception.vision import get_vision_data

from reasoning.groq_brain import ask
from output.tts import speak
from utils.language import is_valid_speech
from core.intent_engine import detect_intent

# ===============================
# CONFIG (LAPTOP TESTING ONLY)
# ===============================
LANGUAGE = "en"   # change to "hi" or "te" if needed
AUDIO_FILE = "input.wav"

print("🧠 Second Brain (Laptop Mode)")
print("Press Ctrl+C to exit\n")


def run_once():
    print("\n🎙 Listening...")
    record_audio(AUDIO_FILE, duration=5)

    print("📝 Transcribing...")
    text, _ = transcribe(AUDIO_FILE, LANGUAGE)
    print("User:", text)

    if not is_valid_speech(text):
        print("⚠️ Invalid speech")
        speak("I could not understand.", LANGUAGE)
        return

    if text.lower() in {"exit", "quit", "stop"}:
        speak("Shutting down. Goodbye.", LANGUAGE)
        sys.exit(0)

    intent = detect_intent(text)

    # ===============================
    # VISION FLOW (LAPTOP CAMERA)
    # ===============================
    if intent == "VISION":
        print("📷 Capturing image...")
        speak("Analyzing the environment. Please hold steady.", LANGUAGE)

        detections, image_path = get_vision_data()

        if not image_path:
            response = "Camera is not available."
        else:
            response = ask(text, LANGUAGE, image_path=image_path)

    # ===============================
    # NORMAL QUESTION
    # ===============================
    else:
        response = ask(text, LANGUAGE)

    print("🤖 Brain:", response)
    speak(response, LANGUAGE)


if __name__ == "__main__":
    try:
        while True:
            run_once()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Exiting Second Brain")
