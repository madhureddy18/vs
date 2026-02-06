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
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img}"
                            }
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
            max_tokens=400
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
















# import os
# import base64
# import google.generativeai as genai


# # ---------------- CONFIG ----------------

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise RuntimeError("GEMINI_API_KEY not set")

# genai.configure(api_key=GEMINI_API_KEY)


# # ---------------- HELPERS ----------------

# def encode_image(path: str) -> dict:
#     with open(path, "rb") as f:
#         return {
#             "mime_type": "image/jpeg",
#             "data": base64.b64encode(f.read()).decode("utf-8")
#         }


# # ---------------- MAIN ASK ----------------

# def ask(text: str, lang: str, image_path: str | None = None):
#     lang_map = {
#         "en": "English",
#         "hi": "Hindi",
#         "te": "Telugu"
#     }

#     system_prompt = f"""
# You are an assistive AI for a blind user.

# RULES:
# 1. Reply ONLY in {lang_map[lang]}.
# 2. Do NOT mix languages.
# 3. Keep answers short, clear, and practical.
# 4. Focus on safety first.
# 5. Do NOT explain unless explicitly asked.
# """

#     try:
#         # ---------------- VISION + TEXT ----------------
#         if image_path:
#             model = genai.GenerativeModel(
#                 model_name="gemini-2.0-flash-lite-001",
#                 system_instruction=system_prompt
#             )

#             image_part = encode_image(image_path)

#             response = model.generate_content(
#                 [
#                     {"text": text},
#                     image_part
#                 ],
#                 generation_config={
#                     "temperature": 0.1,
#                     "max_output_tokens": 300
#                 }
#             )

#             return response.text.strip()

#         # ---------------- TEXT ONLY ----------------
#         else:
#             model = genai.GenerativeModel(
#                 model_name="gemini-2.0-flash-lite-001",
#                 system_instruction=system_prompt
#             )

#             response = model.generate_content(
#                 text,
#                 generation_config={
#                     "temperature": 0.1,
#                     "max_output_tokens": 200
#                 }
#             )

#             return response.text.strip()

#     except Exception as e:
#         print("GEMINI ERROR:", e)
#         fallback = {
#             "en": "I’m having trouble right now. Please try again.",
#             "hi": "अभी समस्या हो रही है। कृपया फिर कोशिश करें।",
#             "te": "ప్రస్తుతం సమస్య ఉంది. దయచేసి మళ్లీ ప్రయత్నించండి."
#         }
#         return fallback[lang]
