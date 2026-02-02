from google.cloud import speech

client = speech.SpeechClient()

LANG_CODE = {
    "en": "en-IN",
    "hi": "hi-IN",
    "te": "te-IN"
}

def transcribe(audio_path: str, lang_hint: str | None = None):
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    audio = speech.RecognitionAudio(content=audio_bytes)

    # 🔹 PASS 1: MULTI-LANG (FOR LANGUAGE CHANGE COMMANDS)
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

    # 🔹 PASS 2: LOCKED LANGUAGE (NORMAL FLOW)
    if lang_hint:
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

    # Fallback (should rarely happen)
    return multi_text, multi_text
