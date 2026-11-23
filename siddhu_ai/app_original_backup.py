import json
import os
import queue
import re
import threading
import time
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

import pyautogui
import pyttsx3

APP_NAME = "SIDDHU AI"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = os.environ.get("SIDDHU_AI_MODEL", "qwen2.5:3b")
VOSK_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models", "vosk-model-small-en-us-0.15")

SYSTEM_PROMPT = r'''You are SIDDHU AI, a helpful Windows desktop assistant. You can chat and propose a small set of computer actions.
Return ONLY one valid JSON object with this exact shape:
{"reply":"brief natural-language response","action":null}
or
{"reply":"brief explanation","action":{"type":"open_app","name":"notepad"}}
or
{"reply":"brief explanation","action":{"type":"open_website","url":"https://example.com"}}
or
{"reply":"brief explanation","action":{"type":"type_text","text":"text to type"}}
or
{"reply":"brief explanation","action":{"type":"hotkey","keys":["ctrl","l"]}}
Allowed app names: notepad, calculator, explorer, chrome, edge, vscode.
Allowed hotkeys only: ctrl+l, ctrl+c, ctrl+v, ctrl+z, ctrl+s, alt+tab, win+e.
Never propose shell commands, PowerShell, deleting files, changing security settings, sending messages, purchases, or actions outside this allowlist. If a request is unsafe or unsupported, set action to null and explain. Do not claim an action has happened; it must be approved by the user first.'''

APP_COMMANDS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "explorer": ["explorer.exe"],
    "chrome": ["cmd", "/c", "start", "", "chrome"],
    "edge": ["cmd", "/c", "start", "", "msedge"],
    "vscode": ["cmd", "/c", "start", "", "code"],
}
ALLOWED_HOTKEYS = {
    ("ctrl", "l"): ("ctrl", "l"),
    ("ctrl", "c"): ("ctrl", "c"),
    ("ctrl", "v"): ("ctrl", "v"),
    ("ctrl", "z"): ("ctrl", "z"),
    ("ctrl", "s"): ("ctrl", "s"),
    ("alt", "tab"): ("alt", "tab"),
    ("win", "e"): ("win", "e"),
}
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.15


def ollama_chat(messages):
    payload = {"model": MODEL, "messages": messages, "stream": False,
               "format": "json", "options": {"temperature": 0.2}}
    req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))
    content = data.get("message", {}).get("content", "")
    return json.loads(content)


def validate_action(action):
    if action is None:
        return None
    if not isinstance(action, dict):
        raise ValueError("Invalid action format.")
    kind = action.get("type")
    if kind == "open_app":
        name = str(action.get("name", "")).lower()
        if name not in APP_COMMANDS:
            raise ValueError("That app is not in the approved app list.")
        return {"type": kind, "name": name}
    if kind == "open_website":
        url = str(action.get("url", "")).strip()
        if not re.fullmatch(r"https?://[^\s]+", url, flags=re.I):
            raise ValueError("Only complete http:// or https:// website addresses are allowed.")
        return {"type": kind, "url": url}
    if kind == "type_text":
        text = action.get("text")
        if not isinstance(text, str) or not text or len(text) > 1000:
            raise ValueError("Text must be between 1 and 1000 characters.")
        return {"type": kind, "text": text}
    if kind == "hotkey":
        keys = action.get("keys")
        if not isinstance(keys, list):
            raise ValueError("Invalid shortcut.")
        key = tuple(str(k).lower() for k in keys)
        if key not in ALLOWED_HOTKEYS:
            raise ValueError("That keyboard shortcut is not allowed.")
        return {"type": kind, "keys": list(ALLOWED_HOTKEYS[key])}
    raise ValueError("Unsupported action. Only approved action types can run.")


def execute_action(action):
    action = validate_action(action)
    if action["type"] == "open_app":
        import subprocess
        subprocess.Popen(APP_COMMANDS[action["name"]], shell=False)
    elif action["type"] == "open_website":
        webbrowser.open(action["url"])
    elif action["type"] == "type_text":
        time.sleep(5)  # time to focus the destination window
        pyautogui.write(action["text"], interval=0.02)
    elif action["type"] == "hotkey":
        time.sleep(3)
        pyautogui.hotkey(*action["keys"])


class SiddhuAI:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("850x650")
        self.root.minsize(650, 500)
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.pending_action = None
        self.voice_queue = queue.Queue()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 175)
        self._build_ui()
        self._append("SIDDHU AI", f"Ready. Local model: {MODEL}. Type a request or use Voice.")

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text="SIDDHU AI", font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Label(header, text=f"LOCAL AI  •  {MODEL}").pack(side="right")
        self.chat = tk.Text(self.root, wrap="word", state="disabled", font=("Segoe UI", 10),
                            padx=12, pady=12)
        self.chat.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        self.chat.tag_config("speaker", foreground="#1769aa", font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("warning", foreground="#a05a00")
        action_frame = ttk.LabelFrame(self.root, text="Action approval", padding=8)
        action_frame.pack(fill="x", padx=12, pady=4)
        self.action_label = ttk.Label(action_frame, text="No pending action")
        self.action_label.pack(side="left", fill="x", expand=True)
        self.approve_btn = ttk.Button(action_frame, text="Approve", command=self.approve_action, state="disabled")
        self.approve_btn.pack(side="right", padx=4)
        self.reject_btn = ttk.Button(action_frame, text="Reject", command=self.reject_action, state="disabled")
        self.reject_btn.pack(side="right", padx=4)
        bottom = ttk.Frame(self.root, padding=12)
        bottom.pack(fill="x")
        self.entry = ttk.Entry(bottom, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry.bind("<Return>", lambda _e: self.send_message())
        ttk.Button(bottom, text="Send", command=self.send_message).pack(side="left", padx=3)
        ttk.Button(bottom, text="Voice", command=self.listen_voice).pack(side="left", padx=3)
        ttk.Button(bottom, text="Speak last reply", command=self.speak_last).pack(side="left", padx=3)
        ttk.Button(bottom, text="Emergency stop", command=self.emergency_stop).pack(side="left", padx=3)
        ttk.Label(self.root, text="Safety: actions require approval. Move mouse to top-left to trigger PyAutoGUI failsafe.",
                  foreground="#8a4b08").pack(anchor="w", padx=14, pady=(0, 8))

    def _append(self, speaker, text, warning=False):
        self.chat.configure(state="normal")
        self.chat.insert("end", speaker + ": ", "speaker")
        self.chat.insert("end", text + "\n\n", "warning" if warning else "")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def send_message(self, preset=None):
        text = preset if preset is not None else self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._append("You", text)
        self.messages.append({"role": "user", "content": text})
        self._set_busy(True)
        threading.Thread(target=self._ask_model, daemon=True).start()

    def _set_busy(self, busy):
        self.root.after(0, lambda: self.entry.configure(state="disabled" if busy else "normal"))

    def _ask_model(self):
        try:
            result = ollama_chat(self.messages)
            reply = str(result.get("reply", "I couldn't form a response."))
            action = validate_action(result.get("action"))
            self.messages.append({"role": "assistant", "content": json.dumps(result)})
            self.root.after(0, lambda: self._model_result(reply, action))
        except Exception as exc:
            self.root.after(0, lambda: self._append("Error", f"{exc}\nCheck that Ollama is running and model {MODEL} is installed.", True))
        finally:
            self._set_busy(False)

    def _model_result(self, reply, action):
        self._append("SIDDHU AI", reply)
        self.last_reply = reply
        if action:
            self.pending_action = action
            self.action_label.configure(text="Proposed: " + json.dumps(action, ensure_ascii=False))
            self.approve_btn.configure(state="normal")
            self.reject_btn.configure(state="normal")
        else:
            self.pending_action = None
            self.action_label.configure(text="No pending action")
            self.approve_btn.configure(state="disabled")
            self.reject_btn.configure(state="disabled")

    def approve_action(self):
        action = self.pending_action
        if not action:
            return
        if not messagebox.askyesno("Confirm computer action", "Run this action?\n\n" + json.dumps(action, indent=2) +
                                   "\n\nTyping and shortcuts act on whichever window you focus."):
            return
        self.pending_action = None
        self.action_label.configure(text="Approved. Executing…")
        self.approve_btn.configure(state="disabled")
        self.reject_btn.configure(state="disabled")
        try:
            execute_action(action)
            self.action_label.configure(text="Action executed")
            self._append("SIDDHU AI", "The approved action was sent to Windows.")
        except Exception as exc:
            self.action_label.configure(text="Action failed")
            self._append("Action error", str(exc), True)

    def reject_action(self):
        self.pending_action = None
        self.action_label.configure(text="Action rejected")
        self.approve_btn.configure(state="disabled")
        self.reject_btn.configure(state="disabled")
        self._append("SIDDHU AI", "I did not perform that action.")

    def emergency_stop(self):
        self.pending_action = None
        self.action_label.configure(text="Pending action cleared")
        self.approve_btn.configure(state="disabled")
        self.reject_btn.configure(state="disabled")
        self._append("Safety", "Pending action cancelled. If automation is in progress, move the mouse to the top-left screen corner.", True)

    def speak_last(self):
        text = getattr(self, "last_reply", "There is no reply to speak yet.")
        threading.Thread(target=lambda: self._tts_speak(text), daemon=True).start()

    def _tts_speak(self, text):
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as exc:
            self.root.after(0, lambda: self._append("Voice error", str(exc), True))

    def listen_voice(self):
        if not os.path.isdir(VOSK_MODEL_DIR):
            messagebox.showerror("Offline voice model missing",
                "Download and extract vosk-model-small-en-us-0.15 into:\n" + VOSK_MODEL_DIR)
            return
        self._append("Voice", "Listening for up to 10 seconds…")
        threading.Thread(target=self._listen_vosk, daemon=True).start()

    def _listen_vosk(self):
        try:
            import sounddevice as sd
            from vosk import Model, KaldiRecognizer
            model = Model(VOSK_MODEL_DIR)
            recognizer = KaldiRecognizer(model, 16000)
            audio_q = queue.Queue()
            def callback(indata, frames, time_info, status):
                audio_q.put(bytes(indata))
            chunks = []
            started = time.time()
            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback):
                while time.time() - started < 10:
                    try:
                        data = audio_q.get(timeout=1)
                    except queue.Empty:
                        continue
                    if recognizer.AcceptWaveform(data):
                        phrase = json.loads(recognizer.Result()).get("text", "")
                        if phrase:
                            chunks.append(phrase)
                            break
                if not chunks:
                    chunks.append(json.loads(recognizer.FinalResult()).get("text", ""))
            phrase = " ".join(chunks).strip()
            if phrase:
                self.root.after(0, lambda: self.send_message(phrase))
            else:
                self.root.after(0, lambda: self._append("Voice", "I didn't hear a clear phrase. Please try again."))
        except Exception as exc:
            self.root.after(0, lambda: self._append("Voice error", str(exc), True))


def main():
    root = tk.Tk()
    SiddhuAI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
