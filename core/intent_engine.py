def detect_intent(text):
    text = text.lower()

    vision_keywords = [
        # English
        "see", "look", "what is", "describe", "camera", "vision",
        "objects", "items", "holding", "read", "how many",

        # Hindi
        "मेरे सामने", "क्या है", "देखो", "आसपास", "कितने",

        # Telugu (NEW)
        "చూడ", "చూడగలవా", "ఇది ఏమిటి", "వివరించు",
        "కెమెరా", "చిత్రం", "చూపించు", "ఎన్ని", "నా ముందు"
    ]

    for kw in vision_keywords:
        if kw in text:
            return "VISION"

    return "KNOWLEDGE"
