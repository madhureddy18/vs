def detect_intent(text: str) -> str:
    t = text.lower()

    # English vision keywords
    en_vision = [
        "see", "look", "in front", "what is in front",
        "describe", "camera", "image", "picture",
        "how many", "read"
    ]

    # Hinglish (Hindi in English letters)
    hi_vision = [
        "mere samne", "samne kya", "samne kya hai",
        "mere aage", "dikhao", "dekho"
    ]

    # Telugu (English letters – rough phonetics)
    te_vision = [
        "na mundu", "em undi", "chudu", "choodandi",
        "idi enti", "chupinchu"
    ]

    for kw in en_vision + hi_vision + te_vision:
        if kw in t:
            return "VISION"

    return "KNOWLEDGE"
