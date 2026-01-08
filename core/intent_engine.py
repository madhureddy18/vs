def detect_intent(text):
    text = text.lower()

    vision_keywords = [
        "how many people",
        "around me",
        "in front of me",
        "मेरे आसपास",
        "कितने लोग"
    ]

    for kw in vision_keywords:
        if kw in text:
            return "VISION"

    return "KNOWLEDGE"
