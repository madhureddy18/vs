class Memory:
    def __init__(self):
        self.language = None  # en | hi | te

    def set_language(self, lang: str):
        if lang in {"en", "hi", "te"}:
            self.language = lang

    def get_language(self):
        return self.language

    def clear_language(self):
        self.language = None
