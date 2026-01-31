from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, JSONResponse
import shutil, os, uuid, traceback

from core.memory import Memory
from core.language_commands import detect_language_command
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
async def process(audio: UploadFile = File(None)):
    """
    Handles three cases:
    1. Init / onboarding (audio=None, language not set)
    2. Init ping (audio=None, language already set)
    3. Normal audio request
    """
    tts_file = new_tts_file()
    audio_path = None

    try:
        # =====================================================
        # CASE 1 & 2: NO AUDIO (INIT / ONBOARDING REQUEST)
        # =====================================================
        if audio is None:
            # Language NOT set yet → ask preference
            if memory.get_language() is None:
                await speak(LANG_PROMPT, "en", tts_file)
                return return_audio(tts_file)

            # Language already set → silent OK (DO NOTHING)
            return JSONResponse({"status": "ok"})

        # =====================================================
        # CASE 3: NORMAL AUDIO FLOW
        # =====================================================
        audio_path = f"audio_{uuid.uuid4().hex}.wav"
        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

        lang_hint = memory.get_language()
        text, _ = transcribe(audio_path, lang_hint)

        try:
            os.remove(audio_path)
        except:
            pass

        print("STT TEXT:", text)
        print("CURRENT LANGUAGE:", lang_hint)

        # Invalid / empty speech
        if not text or not is_valid_speech(text):
            await speak("I could not understand.", "en", tts_file)
            return return_audio(tts_file)

        # -----------------------------------------------------
        # LANGUAGE SET / CHANGE BY VOICE
        # -----------------------------------------------------
        new_lang = detect_language_command(text)
        if new_lang:
            memory.set_language(new_lang)
            await speak(LANG_CONFIRM[new_lang], new_lang, tts_file)
            return return_audio(tts_file)

        # -----------------------------------------------------
        # LANGUAGE STILL NOT SET (edge case)
        # -----------------------------------------------------
        if memory.get_language() is None:
            await speak(LANG_PROMPT, "en", tts_file)
            return return_audio(tts_file)

        # -----------------------------------------------------
        # NORMAL QUESTION ANSWERING
        # -----------------------------------------------------
        lang = memory.get_language()
        response = ask(text, lang)
        await speak(response, lang, tts_file)

        return return_audio(tts_file)

    except Exception:
        # This should now be RARE
        print("SERVER ERROR:\n", traceback.format_exc())
        await speak("System error occurred.", "en", tts_file)
        return return_audio(tts_file)


def return_audio(path: str):
    if not os.path.exists(path):
        return JSONResponse(status_code=500, content={"error": "TTS file missing"})

    with open(path, "rb") as f:
        data = f.read()

    try:
        os.remove(path)
    except:
        pass

    return Response(content=data, media_type="audio/mpeg")
