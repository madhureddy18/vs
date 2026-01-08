from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

def transcribe(audio_path):
    segments, _ = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=True
    )
    return " ".join(seg.text.strip() for seg in segments)
