# =========================================================
# Second Brain - Assistive AI Server (VISION-AWARE, STABLE)
# =========================================================

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, JSONResponse
import shutil, os, traceback, uuid

from core.intent_engine import detect_intent
from core.memory import Memory
from perception.speech_to_text import transcribe
from reasoning.groq_brain import ask
from utils.language import detect_language, is_valid_speech
from output.tts import speak

app = FastAPI()
memory = Memory()

AUDIO_IN = "input.wav"
IMAGE_IN = "client_image.jpg"

# ---------- helper ----------
def new_tts_file():
    return f"tts_{uuid.uuid4().hex}.mp3"


@app.post("/process")
async def process(
    audio: UploadFile = File(...),
    image: UploadFile = File(None)
):
    tts_file = new_tts_file()

    try:
        # 1️⃣ Save audio
        with open(AUDIO_IN, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        # 2️⃣ Speech → text
        text = transcribe(AUDIO_IN)
        if not text or not is_valid_speech(text):
            await speak("I could not understand.", "en", tts_file)
            return return_audio(tts_file)

        # 3️⃣ Detect intent
        lang = detect_language(text)
        intent = detect_intent(text)

        # 4️⃣ Ask for image ONLY if vision intent
        if intent == "VISION" and image is None:
            return JSONResponse({"need_image": True})

        image_path = None
        if image:
            with open(IMAGE_IN, "wb") as f:
                shutil.copyfileobj(image.file, f)
            image_path = IMAGE_IN

        # 5️⃣ Reasoning
        response = (
            ask(text, lang, image_path=image_path)
            if intent == "VISION"
            else ask(text, lang)
        )

        # 6️⃣ TTS (SAFE)
        await speak(response, lang, tts_file)

        # 7️⃣ Return audio
        return return_audio(tts_file)

    except Exception:
        print("SERVER ERROR:\n", traceback.format_exc())
        try:
            await speak("A system error occurred.", "en", tts_file)
            return return_audio(tts_file)
        except:
            return JSONResponse(
                status_code=500,
                content={"error": "Critical server error"}
            )


def return_audio(tts_file: str):
    if not os.path.exists(tts_file):
        return JSONResponse(
            status_code=500,
            content={"error": "TTS file missing"}
        )

    with open(tts_file, "rb") as f:
        data = f.read()

    try:
        os.remove(tts_file)
    except:
        pass

    return Response(
        content=data,
        media_type="audio/mpeg"
    )
