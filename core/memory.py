class Memory:
    def __init__(self):
        self.language = None   # en | hi | te
        self.last_intent = None  # VISION | KNOWLEDGE

    def set_language(self, lang: str):
        if lang in {"en", "hi", "te"}:
            self.language = lang

    def get_language(self):
        return self.language

    def set_intent(self, intent: str):
        self.last_intent = intent

    def get_intent(self):
        return self.last_intent

    def clear(self):
        self.language = None
        self.last_intent = None
