import pyttsx3
from gtts import gTTS
import playsound
import os
import time
import threading

# -------------------------
# INITIALIZE ENGINE ONCE
# -------------------------
_engine = pyttsx3.init()
_engine.setProperty("rate", 150)
_engine.setProperty("volume", 1.0)

_lock = threading.Lock()


def _speak_pyttsx3(text):
    with _lock:
        _engine.stop()                 # stop any previous speech
        _engine.say(text)
        _engine.runAndWait()           # BLOCK until finished
        time.sleep(0.3)                # allow audio buffer to flush


def _speak_gtts(text, lang):
    filename = "out.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    playsound.playsound(filename, block=True)
    os.remove(filename)
    time.sleep(0.3)


# -------------------------
# PUBLIC API
# -------------------------
def speak(text, lang="en"):
    """
    Guaranteed blocking TTS.
    Blind-safe: function returns ONLY after speech finishes.
    """
    if not text or len(text.strip()) == 0:
        return

    print("[TTS]", text)   # debug only

    if lang == "hi":
        _speak_gtts(text, "hi")
    else:
        _speak_pyttsx3(text)
