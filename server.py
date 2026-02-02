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

app = FastAPI()
memory = Memory()

LANG_PROMPT = "What language do you prefer? English, Hindi, or Telugu."

LANG_CONFIRM = {
    "en": "Language set to English.",
    "hi": "भाषा हिंदी में सेट कर दी गई है।",
    "te": "భాష తెలుగులో సెట్ చేయబడింది."
}

def new_tts_file():
    return f"tts_{uuid.uuid4().hex}.mp3"


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
        # SAVE AUDIO
        # --------------------------------------------------
        audio_path = f"audio_{uuid.uuid4().hex}.wav"
        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        current_lang = memory.get_language()

        locked_text, multi_text = transcribe(audio_path, current_lang)

        try:
            os.remove(audio_path)
        except:
            pass

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
        # VISION INTENT (STRICT)
        # --------------------------------------------------
        intent = detect_intent(locked_text, multi_text)
        is_vision = intent == "VISION"

        print("VISION INTENT:", is_vision)

        # Ask Android to capture image ONLY if vision intent
        if is_vision and image is None:
            print("REQUESTING IMAGE FROM ANDROID")
            return JSONResponse({"need_image": True})

        # --------------------------------------------------
        # SAVE IMAGE (ONLY IF PROVIDED)
        # --------------------------------------------------
        if image:
            image_path = f"image_{uuid.uuid4().hex}.jpg"
            with open(image_path, "wb") as f:
                shutil.copyfileobj(image.file, f)
            print("IMAGE SAVED:", image_path)

        # --------------------------------------------------
        # FINAL RESPONSE
        # --------------------------------------------------
        if is_vision and image_path:
            print("CALLING GROQ VISION")
            response = ask(locked_text, lang, image_path=image_path)
        else:
            print("CALLING GROQ TEXT")
            response = ask(locked_text, lang)

        await speak(response, lang, tts_file)

        if image_path:
            try:
                os.remove(image_path)
            except:
                pass

        return return_audio(tts_file)

    except Exception:
        print("SERVER ERROR:\n", traceback.format_exc())
        await speak("System error occurred.", "en", tts_file)
        return return_audio(tts_file)


def return_audio(path: str):
    if not os.path.exists(path):
        return JSONResponse(
            status_code=500,
            content={"error": "TTS file missing"}
        )

    with open(path, "rb") as f:
        data = f.read()

    try:
        os.remove(path)
    except:
        pass

    return Response(content=data, media_type="audio/mpeg")
