import os
import base64
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

client = Groq(api_key=GROQ_API_KEY)

def encode_image(path: str):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def ask(text: str, lang: str, image_path: str | None = None):
    lang_map = {
        "en": "English",
        "hi": "Hindi",
        "te": "Telugu"
    }

    system_msg = f"""
You are an assistive AI for a blind user.

RULES:
1. Reply ONLY in {lang_map[lang]}.
2. Do NOT mix languages.
3. Keep answers short and clear.
4. Do NOT explain unless asked.
"""

    try:
        if image_path:
            model = "meta-llama/llama-4-scout-17b-16e-instruct"
            img = encode_image(image_path)
            messages = [
                {"role": "system", "content": system_msg},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img}"}
                        }
                    ]
                }
            ]
        else:
            model = "llama-3.3-70b-versatile"
            messages = [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text}
            ]

        res = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
            max_tokens=200
        )

        return res.choices[0].message.content.strip()

    except Exception as e:
        print("GROQ ERROR:", e)
        fallback = {
            "en": "I faced a processing issue.",
            "hi": "प्रसंस्करण में समस्या आई।",
            "te": "ప్రాసెసింగ్‌లో సమస్య ఏర్పడింది."
        }
        return fallback[lang]
