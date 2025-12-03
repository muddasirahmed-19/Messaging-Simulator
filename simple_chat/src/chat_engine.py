import threading
from message import Message

class ChatEngine:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        self.chat_logs = {}       # session_id → list[Message]
        self.sessions = {}        # session_id → participants
        self._observers = []      # engine observers

    # -------- Observer handling --------
    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, session_id, message):
        for obs in list(self._observers):
            try:
                obs.update(session_id, message)
            except:
                pass

    # -------- Session / Chat Logic --------
    def create_session(self, session_id, participants):
        self.sessions[session_id] = participants
        self.chat_logs.setdefault(session_id, [])

    def send_message(self, session_id, message: Message):
        self.chat_logs.setdefault(session_id, []).append(message)
        self._notify(session_id, message)

    def get_logs(self, session_id):
        return list(self.chat_logs.get(session_id, []))

    def search_messages(self, session_id, query):
        logs = self.get_logs(session_id)
        return [m for m in logs if query.lower() in m.content.lower()]
