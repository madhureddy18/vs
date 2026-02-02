import os
import json
from google.cloud import speech
from google.oauth2 import service_account

# ==========================================
# CREATE GOOGLE SPEECH CLIENT (RAILWAY SAFE)
# ==========================================

def create_speech_client():
    """
    Creates a Google Speech client using:
    - GOOGLE_APPLICATION_CREDENTIALS_JSON (Railway / cloud)
    - Fallback to default credentials (local dev)
    """
    creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")

    if creds_json:
        creds_info = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(
            creds_info
        )
        return speech.SpeechClient(credentials=credentials)

    # Local fallback (for laptop testing only)
    return speech.SpeechClient()


client = create_speech_client()

# ==========================================
# LANGUAGE MAP
# ==========================================

LANG_CODE = {
    "en": "en-IN",
    "hi": "hi-IN",
    "te": "te-IN"
}

# ==========================================
# TRANSCRIBE (DUAL PASS)
# ==========================================

def transcribe(audio_path: str, lang_hint: str | None = None):
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    audio = speech.RecognitionAudio(content=audio_bytes)

    # -------------------------------
    # PASS 1: MULTI-LANG (COMMANDS)
    # -------------------------------
    multi_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-IN",
        alternative_language_codes=["hi-IN", "te-IN"],
        enable_automatic_punctuation=True
    )

    multi_response = client.recognize(
        config=multi_config,
        audio=audio
    )

    multi_text = " ".join(
        r.alternatives[0].transcript
        for r in multi_response.results
    ).strip()

    # -------------------------------
    # PASS 2: LOCKED LANGUAGE
    # -------------------------------
    if lang_hint and lang_hint in LANG_CODE:
        locked_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=LANG_CODE[lang_hint],
            enable_automatic_punctuation=True
        )

        locked_response = client.recognize(
            config=locked_config,
            audio=audio
        )

        locked_text = " ".join(
            r.alternatives[0].transcript
            for r in locked_response.results
        ).strip()

        return locked_text, multi_text

    # Fallback (should be rare)
    return multi_text, multi_text
