from langdetect import detect

def detect_language(text):
    try:
        lang = detect(text)
        # Added Telugu ('te') support as per your project goals
        if lang in ["en", "hi", "te"]:
            return lang
        return "en"
    except:
        return "en"

def is_valid_speech(text):
    # Reduced threshold to handle short phrases in various languages
    return len(text.strip()) > 0