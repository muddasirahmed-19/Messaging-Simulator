class MessageRenderer:
    def render(self, message):
        return f"{message.sender}: {message.content}"

class MessageDecorator(MessageRenderer):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def render(self, message):
        return self._wrapped.render(message)

class TimestampDecorator(MessageDecorator):
    def render(self, message):
        base = self._wrapped.render(message)
        ts = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{ts}] {base}"

class StatusDecorator(MessageDecorator):
    def render(self, message):
        base = self._wrapped.render(message)
        return f"{base} ({message.status})"
