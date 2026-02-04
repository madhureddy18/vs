def detect_language_command(text: str):
    t = text.lower()

    # English
    if "english" in t or "inglish" in t:
        return "en"

    # Hindi
    if "hindi" in t or "हिंदी" in t:
        return "hi"

    # Telugu (script + phonetic)
    if (
        "telugu" in t or
        "తెలుగు" in t or
        "telugulo" in t or
        "telugulo set" in t
    ):
        return "te"

    return None
