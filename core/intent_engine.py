import re

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\u0C00-\u0C7F\u0900-\u097F\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# High-confidence VISION indicators (ANY hit = VISION)
VISION_TOKENS = [
    # English (fuzzy)
    "front", "ahead", "near", "around", "beside",
    "road", "path", "walking", "walk", "safe",
    "object", "thing", "something", "anything",
    "person", "people", "car", "bike", "bus",
    "vehicle", "traffic", "moving", "coming",
    "what is this", "what is there",

    # Hindi (script + phonetic)
    "samne", "aage", "raste", "road", "kya hai",
    "mere samne", "aage kya",

    # Telugu (script)
    "ముందు", "ముందే", "నా ముందు", "రహదారి",
    "ఏముంది", "చుట్టూ", "సమీపంలో",

    # Telugu (phonetic – VERY IMPORTANT)
    "mund", "mundu", "munde", "ram mundu",
    "emu ndi", "emundi"
]


def detect_intent(locked_text: str, multi_text: str) -> str:
    combined = normalize(f"{locked_text} {multi_text}")

    # STRONG RULE:
    # If user is talking about space, direction, surroundings → VISION
    for token in VISION_TOKENS:
        if token in combined:
            return "VISION"

    return "KNOWLEDGE"
