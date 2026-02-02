import os
from google.cloud import speech

print("GOOGLE_APPLICATION_CREDENTIALS =", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

client = speech.SpeechClient()
print("Speech client created successfully")


client = speech.SpeechClient()
print(client.transport._credentials.project_id)
