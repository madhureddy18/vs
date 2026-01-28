from langdetect import detect

def detect_language(text: str):
    try:
        lang = detect(text)

        # Force only 3 languages
        if lang.startswith("hi"):
            return "hi"
        elif lang.startswith("te"):
            return "te"
        else:
            return "en"

    except:
        return "en"


def is_valid_speech(text: str):
    if not text:
        return False
    if len(text.strip()) < 2:
        return False
    return True
