from datetime import datetime

class Message:
    def __init__(self, sender, recipient, content, mtype='text', status='sent', timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.type = mtype
        self.status = status
        self.timestamp = timestamp or datetime.utcnow()

    def __repr__(self):
        return f"<Message {self.sender} -> {self.recipient} '{self.content[:20]}...' ({self.status})>"
