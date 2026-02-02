def detect_intent(text: str) -> str:
    if not text:
        return "KNOWLEDGE"

    t = text.lower()

    # ---------- ENGLISH ----------
    en_vision = [
        "what is in front", "what's in front", "in front of me",
        "what do you see", "describe", "describe the object",
        "what is this", "what am i holding", "read this",
        "how many"
    ]

    # ---------- HINDI (DEVANAGARI) ----------
    hi_vision = [
        "मेरे सामने", "यह क्या है", "क्या दिख रहा है",
        "विवरण बताओ", "क्या है", "पढ़ो", "कितने"
    ]

    # ---------- TELUGU (NATIVE SCRIPT) ----------
    te_vision = [
        "నా ముందు", "ఇది ఏమిటి", "ఏముంది",
        "వివరించు", "చూపించు", "ఎన్ని", "చదువు"
    ]

    for kw in en_vision + hi_vision + te_vision:
        if kw in t:
            return "VISION"

    return "KNOWLEDGE"
