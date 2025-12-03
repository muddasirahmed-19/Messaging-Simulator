from dataclasses import dataclass

@dataclass
class ChatSession:
    session_id: str
    participants: list
    encrypted: bool = False

class ChatSessionBuilder:
    def __init__(self):
        self._session_id = None
        self._participants = []
        self._encrypted = False

    def session_id(self, sid):
        self._session_id = sid
        return self

    def participants(self, participants):
        self._participants = participants
        return self

    def encrypted(self, val: bool):
        self._encrypted = val
        return self

    def build(self):
        if not self._session_id:
            raise ValueError("session_id required")
        return ChatSession(
            session_id=self._session_id,
            participants=self._participants,
            encrypted=self._encrypted
        )
