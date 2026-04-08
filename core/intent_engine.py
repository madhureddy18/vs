#CORE: INTENT ENGINE

import re
from typing import Optional


# ---------------- NORMALIZATION ----------------

def normalize(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    # keep english + hindi + telugu scripts
    text = re.sub(r"[^a-z\u0900-\u097F\u0C00-\u0C7F\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------- VISION KEYWORDS ----------------
# Any strong match => VISION

VISION_TOKENS = [

    # ========= SAFETY =========
    # English
    "obstacle", "block", "danger", "safe", "unsafe",
    "vehicle", "car", "bike", "bus", "truck", "traffic",
    "coming", "approaching",
    "fire", "smoke", "water", "wet",

    # Hindi
    "rukavat", "khatra", "surakshit",
    "gadi", "aag", "dhua", "pani",

    # Telugu
    "అడ్డంకి", "ప్రమాదం", "సురక్షితం",
    "వాహనం", "మంట", "పొగ", "నీరు",

    # ========= NAVIGATION =========
    # English
    "front", "ahead", "near", "around", "beside",
    "road", "path", "walk", "walking",
    "left", "right", "step", "stair",
    "door", "open", "closed",

    # Hindi
    "samne", "aage", "raste", "chalna",
    "baaye", "daaye", "seedhi", "darwaza",

    # Telugu
    "ముందు", "ముందుకు", "దారి", "నడవ",
    "ఎడమ", "కుడి", "మెట్టు", "తలుపు",

    # ========= PEOPLE / CROWD =========
    # English
    "person", "people", "crowd", "queue", "line",

    # Hindi
    "aadmi", "log", "bheed", "line",

    # Telugu
    "వ్యక్తి", "జనం", "గుంపు", "క్యూ",

    # ========= OBJECT / DESCRIPTION =========
    # English
    "what is this", "what is that",
    "describe", "describe this", "describe the object",
    "what am i holding", "nearest object",

    # Hindi
    "ye kya hai", "isko batao", "varnan karo",
    "ye vastu kya hai",

    # Telugu
    "ఇది ఏమిటి", "వివరించు",
    "ఈ వస్తువు ఏమిటి", "నేను ఏమి పట్టుకున్నాను",

    # ========= COLOR / ATTRIBUTES (NEW) =========
    # English
    "color", "colour", "what color", "what colour",
    "color of this", "color of the object",

    # Hindi
    "rang", "kis rang", "rang kya",

    # Telugu
    "రంగు", "ఏ రంగు", "రంగు ఏమిటి",

    # ========= TEXT / LABEL / MEDICINE =========
    # English
    "read this", "what is written", "label",
    "medicine", "expiry", "dosage",

    # Hindi
    "padho", "kya likha hai", "dawai", "expiry",

    # Telugu
    "చదువు", "ఏమి వ్రాయబడింది",
    "మందు", "గడువు",

    # ========= PHONETIC (STT ERROR TOLERANT) =========
    # English broken
    "front off", "front of mi", "ahead of mi",
    "discribe", "discribe object", "discribe d object",
    "describe d object", "d object",
    "color d object", "colour d object",

    # Hindi phonetic
    "mere samne", "aage kya", "samne kya",

    # Telugu phonetic (VERY IMPORTANT)
    "mundu", "na mundu", "mundu em",
    "emundi", "ram mundu", "mundem"
]


# ---------------- INTENT DETECTOR ----------------

def detect_intent(
    locked_text: str,
    multi_text: str,
    image_present: Optional[bool] = False
) -> str:
    """
    Returns: VISION | KNOWLEDGE
    """

    # 🔥 HARD OVERRIDE
    # If image exists, user clearly wants vision
    if image_present:
        return "VISION"

    combined = normalize(f"{locked_text} {multi_text}")

    # 🔥 SMART OBJECT RULE (NEW)
    # Handles: "describe object", "color of object", broken STT
    if (
        ("describe" in combined or "discribe" in combined)
        and "object" in combined
    ):
        return "VISION"

    if "color" in combined or "colour" in combined or "rang" in combined or "రంగు" in combined:
        return "VISION"

    # Fast keyword scan
    for token in VISION_TOKENS:
        if token in combined:
            return "VISION"

    return "KNOWLEDGE"
