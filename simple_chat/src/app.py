import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from message_factory import MessageFactory
from chat_engine import ChatEngine
from decorator import MessageRenderer, TimestampDecorator, StatusDecorator
from builder import ChatSessionBuilder
import threading, time

class GUIObserver:
    def __init__(self, app):
        self.app = app

    def update(self, session_id, message):
        self.app.root.after(0, lambda: self.app.on_incoming_message(session_id, message))

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Chat / Messaging Simulator")

        self.engine = ChatEngine()
        self.factory = MessageFactory()

        self.renderer = StatusDecorator(TimestampDecorator(MessageRenderer()))

        builder = ChatSessionBuilder().session_id("default").participants(["Alice", "Bob"])
        self.session = builder.build()

        self.engine.create_session(self.session.session_id, self.session.participants)
        self.engine.register_observer(GUIObserver(self))

        self._build_ui()
        self._typing = False
        self._typing_timer = None

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill="both", expand=True)

        self.chat_display = scrolledtext.ScrolledText(top, wrap="word", width=60, height=20, state="disabled")
        self.chat_display.grid(row=0, column=0, columnspan=3, pady=(0, 8))

        self.typing_label = ttk.Label(top, text="")
        self.typing_label.grid(row=1, column=0, sticky="w")

        self.entry = ttk.Entry(top, width=50)
        self.entry.grid(row=2, column=0, sticky="we", padx=(0, 8))
        self.entry.bind("<Key>", self._typing_indicator)

        send_btn = ttk.Button(top, text="Send", command=self.send_message)
        send_btn.grid(row=2, column=1)

        simulate_btn = ttk.Button(top, text="Click for BOT reply", command=self.simulate_incoming)
        simulate_btn.grid(row=2, column=2)

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(top, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=3, column=0, pady=(8, 0), sticky="w")
        search_btn = ttk.Button(top, text="Search", command=self.search_messages)
        search_btn.grid(row=3, column=1, sticky="w")

    def _typing_indicator(self, event):
        if not self._typing:
            self._typing = True
            self.typing_label.config(text="Typing...")

        if self._typing_timer:
            self.root.after_cancel(self._typing_timer)

        self._typing_timer = self.root.after(1000, self._clear_typing)

    def _clear_typing(self):
        self._typing = False
        self.typing_label.config(text="")

    def append_text(self, text):
        self.chat_display["state"] = "normal"
        self.chat_display.insert("end", text + "\n")
        self.chat_display.see("end")
        self.chat_display["state"] = "disabled"

    def send_message(self):
        content = self.entry.get().strip()
        if not content:
            return

        msg = self.factory.create("text", "You", "Bob", content, status="sent")
        self.engine.send_message(self.session.session_id, msg)
        self.entry.delete(0, "end")
        self._clear_typing()

    def on_incoming_message(self, session_id, message):
        rendered = self.renderer.render(message)
        self.append_text(rendered)

    def simulate_incoming(self):
        def worker():
            time.sleep(1)
            msg = self.factory.create("text", "Bob", "You", "Hello there!", status="delivered")
            self.engine.send_message(self.session.session_id, msg)

        threading.Thread(target=worker, daemon=True).start()

    def search_messages(self):
        q = self.search_var.get().strip()
        if not q:
            messagebox.showinfo("Search", "Enter text to search.")
            return

        results = self.engine.search_messages(self.session.session_id, q)

        win = tk.Toplevel(self.root)
        win.title("Search Results")

        st = scrolledtext.ScrolledText(win, width=60, height=15)
        st.pack(padx=8, pady=8)

        if not results:
            st.insert("end", "No results found.")
        else:
            for m in results:
                st.insert("end", self.renderer.render(m) + "\n")

        st["state"] = "disabled"

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
