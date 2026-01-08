from langdetect import detect

def detect_language(text):
    try:
        lang = detect(text)
        if lang not in ["en", "hi"]:
            return "en"
        return lang
    except:
        return "en"

def is_valid_speech(text):
    return len(text.strip().split()) >= 3
