from google import genai
import os

client = genai.Client(api_key="AIzaSyC807jBvYDHYGgl8TfzXt98nKIxqHhZEbQ")

def ask(text, lang="en"):
    if lang == "hi":
        prompt = f"प्रश्न का उत्तर सरल हिंदी में दीजिए:\n{text}"
    else:
        prompt = f"Answer clearly in English:\n{text}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()
