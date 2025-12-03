from message import Message

class MessageFactory:
    def create(self, mtype, sender, recipient, content, **kwargs):
        if mtype == "text":
            return Message(sender, recipient, content, mtype="text", status=kwargs.get("status", "sent"))
        elif mtype == "system":
            return Message(sender, recipient, content, mtype="system", status=kwargs.get("status", "info"))
        else:
            raise ValueError("Unknown message type")
