# =========================================================
# Second Brain - Voice Only Assistive AI Server
# Audio + Image IN  →  Spoken Audio OUT
# SINGLE FILE (Copy–Paste Ready)
# =========================================================

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
import uuid
import traceback

# ---------- IMPORT YOUR EXISTING LOGIC ----------
from core.intent_engine import detect_intent
from core.memory import Memory
from perception.speech_to_text import transcribe
from reasoning.groq_brain import ask
from utils.language import detect_language, is_valid_speech
from output.tts import speak   # Uses edge-tts internally

# ---------- INITIALIZE ----------
app = FastAPI(title="Second Brain Assistive Server")
memory = Memory()

AUDIO_IN = "input.wav"
IMAGE_IN = "client_image.jpg"
TEMP_TTS = "temp_voice.mp3"

# ---------- HEALTH CHECK ----------
@app.get("/")
def health():
    return {"status": "Second Brain server running"}

# ---------- MAIN ENDPOINT ----------
@app.post("/process")
async def process(
    audio: UploadFile = File(...),
    image: UploadFile = File(None)
):
    """
    Blind-friendly endpoint:
    - audio: REQUIRED (mic)
    - image: OPTIONAL (camera)
    - returns: SPOKEN AUDIO (mp3)
    """

    try:
        # 1️⃣ Save incoming audio
        with open(AUDIO_IN, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        # 2️⃣ Speech → Text
        text = transcribe(AUDIO_IN)

        if not text or not is_valid_speech(text):
            speak("I could not understand. Please try again.", "en")
            return FileResponse(TEMP_TTS, media_type="audio/mpeg")

        # 3️⃣ Language + Intent
        lang = detect_language(text)
        intent = detect_intent(text)

        memory.remember("last_text", text)

        # 4️⃣ Save image if present
        image_path = None
        if image:
            with open(IMAGE_IN, "wb") as f:
                shutil.copyfileobj(image.file, f)
            image_path = IMAGE_IN

        # 5️⃣ Reasoning
        if intent == "VISION" and image_path:
            response_text = ask(text, lang, image_path=image_path)
        else:
            response_text = ask(text, lang)

        # 6️⃣ Generate speech
        speak(response_text, lang)

        if not os.path.exists(TEMP_TTS):
            return JSONResponse(
                status_code=500,
                content={"error": "TTS generation failed"}
            )

        # 7️⃣ Return audio
        output_file = f"response_{uuid.uuid4().hex}.mp3"
        os.rename(TEMP_TTS, output_file)

        return FileResponse(
            output_file,
            media_type="audio/mpeg",
            filename="response.mp3"
        )

    except Exception as e:
        print("SERVER ERROR:", traceback.format_exc())
        speak("A system error occurred.", "en")
        return FileResponse(TEMP_TTS, media_type="audio/mpeg")
