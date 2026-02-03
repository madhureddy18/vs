from google.cloud import speech
import os
import concurrent.futures

LANG_CODE = {
    "en": "en-IN",
    "hi": "hi-IN",
    "te": "te-IN"
}

MAX_STT_SECONDS = 15  # hard safety limit


def get_client():
    return speech.SpeechClient()


def _recognize(client, config, audio):
    return client.recognize(config=config, audio=audio)


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

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                _recognize, client, multi_config, audio
            )
            multi_response = future.result(timeout=MAX_STT_SECONDS)
    except Exception:
        return "", ""

    multi_text = " ".join(
        r.alternatives[0].transcript
        for r in multi_response.results
        if r.alternatives
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

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    _recognize, client, locked_config, audio
                )
                locked_response = future.result(timeout=MAX_STT_SECONDS)
        except Exception:
            return multi_text, multi_text

        locked_text = " ".join(
            r.alternatives[0].transcript
            for r in locked_response.results
            if r.alternatives
        ).strip()

        return locked_text, multi_text

    return multi_text, multi_text
