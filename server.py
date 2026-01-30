from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from speech_to_text import transcribe
from intent_engine import detect_intent
from language import detect_language
from tts import speak

from ultralytics import YOLO
from groq_brain import ask_groq   # your LLM function

app = FastAPI()

# Load YOLO model once
model = YOLO("yolo11n.pt")

@app.post("/process")
async def process_request(
    audio: UploadFile = File(...),
    image: UploadFile = File(None)
):
    # Save audio
    audio_path = "input.wav"
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    # Speech to text
    text = transcribe(audio_path)

    if not text:
        return JSONResponse({"error": "No speech detected"})

    # Detect intent
    intent = detect_intent(text)

    # Detect language
    lang = detect_language(text)

    # Process request
    if intent == "VISION" and image:
        image_path = "image.jpg"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        results = model(image_path, conf=0.6)
        detections = {}

        for r in results:
            for box in r.boxes:
                label = model.names[int(box.cls[0])]
                detections[label] = detections.get(label, 0) + 1

        if detections:
            reply_text = "I can see "
            reply_text += ", ".join(
                [f"{v} {k}" for k, v in detections.items()]
            )
        else:
            reply_text = "I could not detect any objects."

    else:
        reply_text = ask_groq(text)

    # Generate speech
    tts_path = "reply.mp3"
    await speak(reply_text, lang, tts_path)

    return {
        "recognized_text": text,
        "intent": intent,
        "reply": reply_text
    }


@app.get("/")
def root():
    return {"status": "AI Assistant Server Running"}
