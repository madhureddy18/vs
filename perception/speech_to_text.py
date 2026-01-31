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

    if lang_hint:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=LANG_CODE[lang_hint],
            enable_automatic_punctuation=True
        )
        used_lang = lang_hint
    else:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-IN",
            alternative_language_codes=["hi-IN", "te-IN"],
            enable_automatic_punctuation=True
        )
        used_lang = "en"

    response = client.recognize(config=config, audio=audio)

    if not response.results:
        return "", used_lang

    text = " ".join(r.alternatives[0].transcript for r in response.results)
    return text.strip(), used_lang
