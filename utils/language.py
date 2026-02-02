def is_valid_speech(text: str) -> bool:
    """
    Basic sanity check for STT output.
    Prevents empty / noise-only input.
    """
    if not text:
        return False
    return len(text.strip()) >= 2
