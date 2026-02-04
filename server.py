from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, JSONResponse
import shutil, os, uuid, traceback

from core.memory import Memory
from core.language_commands import detect_language_command
from core.intent_engine import detect_intent
from perception.speech_to_text import transcribe
from reasoning.groq_brain import ask
from output.tts import speak
from utils.language import is_valid_speech

# --------------------------------------------------
# APP INIT
# --------------------------------------------------
app = FastAPI()
memory = Memory()

LANG_PROMPT = "What language do you prefer? English, Hindi, or Telugu."

LANG_CONFIRM = {
    "en": "Language set to English.",
    "hi": "भाषा हिंदी में सेट कर दी गई है।",
    "te": "భాష తెలుగులో సెట్ చేయబడింది."
}

TMP_DIR = "/tmp"

# Ensure temp directory exists (Windows + Linux safe)
os.makedirs(TMP_DIR, exist_ok=True)


# --------------------------------------------------
# UTILITIES
# --------------------------------------------------
def new_tts_file():
    return f"{TMP_DIR}/tts_{uuid.uuid4().hex}.mp3"


def safe_remove(path: str):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except:
        pass


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------
@app.get("/")
def health():
    return {"status": "SECOND_BRAIN running"}


# --------------------------------------------------
# MAIN ENDPOINT
# --------------------------------------------------
@app.post("/process")
async def process(
    audio: UploadFile = File(None),
    image: UploadFile = File(None)
):
    tts_file = new_tts_file()
    audio_path = None
    image_path = None

    try:
        print("=== NEW REQUEST ===")
        print("AUDIO RECEIVED:", audio is not None)
        print("IMAGE RECEIVED:", image is not None)

        # --------------------------------------------------
        # INIT / ONBOARDING
        # --------------------------------------------------
        if audio is None or audio.file is None:
            if memory.get_language() is None:
                await speak(LANG_PROMPT, "en", tts_file)
                return return_audio(tts_file)
            return JSONResponse({"status": "ok"})

        # --------------------------------------------------
        # SAVE AUDIO (Cloud Run safe)
        # --------------------------------------------------
        audio_path = f"{TMP_DIR}/audio_{uuid.uuid4().hex}.wav"
        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        current_lang = memory.get_language()

        locked_text, multi_text = transcribe(audio_path, current_lang)

        safe_remove(audio_path)

        print("LOCKED STT :", locked_text)
        print("MULTI STT  :", multi_text)
        print("LANGUAGE   :", current_lang)

        # --------------------------------------------------
        # LANGUAGE CHANGE (ALWAYS ALLOWED)
        # --------------------------------------------------
        new_lang = detect_language_command(multi_text)
        if new_lang:
            memory.set_language(new_lang)
            await speak(LANG_CONFIRM[new_lang], new_lang, tts_file)
            return return_audio(tts_file)

        # --------------------------------------------------
        # LANGUAGE NOT SET SAFETY
        # --------------------------------------------------
        if memory.get_language() is None:
            await speak(LANG_PROMPT, "en", tts_file)
            return return_audio(tts_file)

        lang = memory.get_language()

        # --------------------------------------------------
        # INVALID SPEECH
        # --------------------------------------------------
        if not is_valid_speech(locked_text):
            await speak("I could not understand.", lang, tts_file)
            return return_audio(tts_file)

        # --------------------------------------------------
        # INTENT DETECTION
        # --------------------------------------------------
        intent = detect_intent(locked_text, multi_text)

        # Once vision is detected, remember it
        if intent == "VISION":
            memory.set_intent("VISION")

        is_vision = memory.get_intent() == "VISION"

        print("VISION INTENT:", is_vision)

        # Ask client to capture image if needed (only once)
        if is_vision and image is None:
            return JSONResponse({"need_image": True})

        # --------------------------------------------------
        # SAVE IMAGE (ONLY IF PROVIDED)
        # --------------------------------------------------
        if image:
            image_path = f"{TMP_DIR}/image_{uuid.uuid4().hex}.jpg"
            with open(image_path, "wb") as f:
                shutil.copyfileobj(image.file, f)
            print("IMAGE SAVED:", image_path)

        # --------------------------------------------------
        # FINAL RESPONSE
        # --------------------------------------------------
        # --------------------------------------------------
        # FINAL RESPONSE
        # --------------------------------------------------
        if is_vision and image_path:
            response = ask(locked_text, lang, image_path=image_path)

            # Vision completed → clear intent
            memory.set_intent(None)
        else:
            response = ask(locked_text, lang)

        await speak(response, lang, tts_file)

        safe_remove(image_path)

        return return_audio(tts_file)


    except Exception:
        print("SERVER ERROR:\n", traceback.format_exc())
        await speak("System error occurred.", "en", tts_file)
        return return_audio(tts_file)


# --------------------------------------------------
# AUDIO RESPONSE
# --------------------------------------------------
def return_audio(path: str):
    if not os.path.exists(path):
        return JSONResponse(
            status_code=500,
            content={"error": "TTS file missing"}
        )

    with open(path, "rb") as f:
        data = f.read()

    safe_remove(path)

    return Response(content=data, media_type="audio/mpeg")


# --------------------------------------------------
# ENTRYPOINT (Cloud Run + Local + ngrok)
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
