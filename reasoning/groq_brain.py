import os
import base64
from groq import Groq

# ✅ Read API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=GROQ_API_KEY)


def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ask(text, lang="en", image_path=None):

    lang_map = {
        "en": "English",
        "hi": "Hindi",
        "te": "Telugu"
    }

    target_lang = lang_map.get(lang, "English")

    system_msg = (
        "You are an assistive 'Second Brain' for a blind person. "
        "RULE 1: Answer the user's question directly, shortly and clearly. "
        "RULE 2: Keep the answer short and useful (about 5 to 7 sentences). "
        "RULE 3: Use the image ONLY if it helps answer the question. "
        "RULE 4: Do NOT give long paragraphs. "
        "RULE 5: Do NOT describe the image unless asked. "
        "RULE 6: If the image is irrelevant, ignore it. "
        f"Reply ONLY in {target_lang}. "
        "Do NOT mix languages. Do NOT translate."
    )

    try:
        if image_path and os.path.exists(image_path):
            model_name = "meta-llama/llama-4-scout-17b-16e-instruct"
            base64_image = encode_image(image_path)

            messages = [
                {"role": "system", "content": system_msg},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        else:
            model_name = "llama-3.3-70b-versatile"
            messages = [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text}
            ]

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.1,
            max_tokens=220
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("[GROQ ERROR]", e)

        error_msgs = {
            "en": "I encountered a processing error.",
            "hi": "प्रसंस्करण में त्रुटि हुई।",
            "te": "ప్రాసెసింగ్‌లో లోपం ఏర్పడింది."
        }

        return error_msgs.get(lang, error_msgs["en"])
