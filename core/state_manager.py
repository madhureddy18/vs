class StateManager:
    IDLE = "IDLE"
    LISTENING = "LISTENING"
    PROCESSING = "PROCESSING"
    RESPONDING = "RESPONDING"

    def __init__(self):
        self.state = self.IDLE

    def set_state(self, new_state):
        print(f"[STATE] {self.state} → {new_state}")
        self.state = new_state
