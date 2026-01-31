def detect_language_command(text: str):
    t = text.lower()

    # English
    if "english" in t:
        return "en"

    # Hindi
    if "hindi" in t or "हिंदी" in t:
        return "hi"

    # Telugu
    if "telugu" in t or "తెలుగు" in t:
        return "te"

    return None
