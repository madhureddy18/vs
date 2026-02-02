from google.cloud import speech
import os

LANG_CODE = {
    "en": "en-IN",
    "hi": "hi-IN",
    "te": "te-IN"
}

def get_client():
    """
    Create SpeechClient lazily so credentials
    are read at runtime, not import time.
    """
    return speech.SpeechClient()

def transcribe(audio_path: str, lang_hint: str | None = None):
    if not os.path.exists(audio_path):
        return "", ""

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    audio = speech.RecognitionAudio(content=audio_bytes)
    client = get_client()

    # ============================
    # PASS 1: MULTI-LANGUAGE
    # ============================
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

    # ============================
    # PASS 2: LOCKED LANGUAGE
    # ============================
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

    # fallback
    return multi_text, multi_text
