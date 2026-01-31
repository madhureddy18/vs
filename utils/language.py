TELUGU_PHONETIC = [
    "undi", "ledu", "enti", "idi", "adi", "chudu",
    "choodandi", "mundu", "akkada", "ikkada"
]

HINGLISH_KEYWORDS = [
    "kya", "samne", "mere", "hai", "ka", "ke", "ki"
]


def normalize_language(text: str, stt_lang: str) -> str:
    t = text.lower()

    if stt_lang in {"hi", "te"}:
        return stt_lang

    # Hinglish → Hindi
    for w in HINGLISH_KEYWORDS:
        if w in t:
            return "hi"

    # Phonetic Telugu → Telugu
    for w in TELUGU_PHONETIC:
        if w in t:
            return "te"

    return "en"


def is_valid_speech(text: str) -> bool:
    return bool(text and len(text.strip()) >= 2)
