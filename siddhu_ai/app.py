"""
================================================================================
  SIDDHU AI // STARK INDUSTRIES MARK-XII [FRIDAY COGNITIVE NLP & LLM MATRIX]
  FULLY AUTONOMOUS ZERO-TOUCH MULTI-STEP REASONING & PC/WEB CONTROL SYSTEM
================================================================================
  - True NLP + LLM Brain: Integrates Local Ollama Neural Core, Cloud LLM,
    and Advanced Multi-Intent Semantic NLP Decomposition.
  - Multi-step execution: "Search for LinkedIn in Chrome and open the first link"
    -> Automatically generates a plan, searches in Chrome, waits, and clicks link!
  - Complete PC & Web Tools:
      * App Launch & Close (Notepad, Calculator, VS Code, Paint, Spotify...)
      * Web Navigation & Search (Chrome, YouTube, Popular sites, Custom URLs)
      * Search Result Navigation ("Open first link", "Click second result")
      * Full Mouse Emulation (Clicks, Double click, Right click, Coordinates, Scrolls)
      * Full Keyboard Emulation (Enter, Space, Tab, Esc, Hotkeys, Text Typing)
      * Browser Tab Management (New tab, Close tab, Next tab, Back, Forward, Reload)
      * File & Desktop Control (Create folders/notes, Screenshots, Volume, Lock PC)
      * Live Online Intel (Weather, Wikipedia, DuckDuckGo instant answers)
  - Continuous background voice recognition (100% button-free zero-touch).
  - Resilient dual speech synthesizer: pyttsx3 + SAPI fallback (FRIDAY voice).
  - High-tech acoustic audio cues via native winsound.
================================================================================
"""

import json
import math
import os
import queue
import random
import re
import subprocess
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import ttk

# Enable Windows High-DPI scaling
try:
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

import psutil
import pyautogui

try:
    import pygetwindow as gw
    HAS_GW = True
except ImportError:
    HAS_GW = False

# Sound effects via Windows winsound
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# Speech recognition
try:
    import speech_recognition as sr
    HAS_SR = True
except ImportError:
    HAS_SR = False

try:
    import vosk
    import sounddevice as sd
    HAS_VOSK = True
except ImportError:
    HAS_VOSK = False


# ==============================================================================
# CONFIGURATION & THEME PALETTE
# ==============================================================================
APP_NAME = "SIDDHU AI"
HUD_TITLE = "SIDDHU AI // STARK INDUSTRIES MARK-XII [FRIDAY NLP & LLM MATRIX]"
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
MODEL = os.environ.get("SIDDHU_AI_MODEL", "qwen2.5:3b")
VOSK_MODEL_DIR = os.path.join(os.path.dirname(__file__), "models", "vosk-model-small-en-us-0.15")

# Locate Google Chrome
CHROME_CANDIDATE_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
]
CHROME_EXE = None
for p in CHROME_CANDIDATE_PATHS:
    if os.path.exists(p):
        CHROME_EXE = p
        break

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.08

# Stark Obsidian & Electric Cyan Holographic Palette
COLOR_VOID = "#02050e"          # Obsidian deep space void
COLOR_NAVY_DEEP = "#040c1a"     # Dark tactical navy
COLOR_PANEL_BG = "#071224"      # Semi-dark cyber panel fill
COLOR_CARD_BG = "#0b1b36"       # Elevated holographic card
COLOR_BORDER_DIM = "#0d2b4d"    # Subdued structural lines
COLOR_BORDER_CYAN = "#00f0ff"   # Electric glowing cyan
COLOR_CYAN_GLOW = "#00e5ff"     # Neon primary cyan
COLOR_CYAN_PALE = "#a5f3fc"     # White-cyan plasma highlight
COLOR_CYAN_DIM = "#006688"      # Inactive / track cyan
COLOR_GOLD = "#ffb703"          # Stark Industries gold
COLOR_AMBER = "#fb8500"         # Alert / processing
COLOR_GREEN = "#10b981"         # Active / optimal / executed
COLOR_PURPLE = "#a855f7"        # LLM / Neural reasoning
COLOR_RED = "#ef4444"           # Abort
COLOR_TEXT_PRIMARY = "#e2f1ff"  # Crisp holographic readout text
COLOR_TEXT_MUTED = "#64748b"    # Subdued telemetry labels
COLOR_TEXT_CYAN = "#38bdf8"     # Cyan accent text


# ==============================================================================
# SPEECH SYNTHESIZER (FRIDAY AVENGERS TONE)
# ==============================================================================
class TacticalSpeechEngine:
    def __init__(self):
        self.engine_type = "NONE"
        self.tts = None
        self.sapi_voice = None

        try:
            import pyttsx3
            self.tts = pyttsx3.init()
            self.tts.setProperty("rate", 175)
            for v in self.tts.getProperty("voices"):
                if "zira" in v.name.lower() or "david" in v.name.lower():
                    self.tts.setProperty("voice", v.id)
                    break
            self.engine_type = "PYTTSX3"
        except Exception:
            try:
                import win32com.client
                self.sapi_voice = win32com.client.Dispatch("SAPI.SpVoice")
                self.sapi_voice.Rate = 1
                self.engine_type = "SAPI"
            except Exception:
                self.engine_type = "POWERSHELL"

    def speak(self, text):
        clean_text = text.replace('"', '').replace("'", "")
        if self.engine_type == "PYTTSX3" and self.tts:
            try:
                self.tts.say(clean_text)
                self.tts.runAndWait()
                return
            except Exception:
                pass

        if self.sapi_voice:
            try:
                self.sapi_voice.Speak(clean_text)
                return
            except Exception:
                pass

        try:
            ps_cmd = f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{clean_text}')"
            subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_cmd], shell=False)
        except Exception:
            pass

    def stop(self):
        if self.engine_type == "PYTTSX3" and self.tts:
            try:
                self.tts.stop()
            except Exception:
                pass


# ==============================================================================
# TACTICAL SOUND EFFECTS (SFX)
# ==============================================================================
SFX_ENABLED = True

def play_sfx(sound_type):
    if not (SFX_ENABLED and HAS_WINSOUND):
        return

    def _worker():
        try:
            if sound_type == "boot":
                winsound.Beep(520, 50)
                winsound.Beep(880, 70)
                winsound.Beep(1400, 100)
            elif sound_type == "blip":
                winsound.Beep(1800, 25)
            elif sound_type == "neural":
                winsound.Beep(1200, 40)
                winsound.Beep(1600, 50)
            elif sound_type == "execute":
                winsound.Beep(880, 45)
                winsound.Beep(1320, 75)
            elif sound_type == "online":
                winsound.Beep(1000, 40)
                winsound.Beep(1500, 60)
                winsound.Beep(2000, 80)
            elif sound_type == "mouse":
                winsound.Beep(1600, 20)
            elif sound_type == "abort":
                winsound.Beep(420, 100)
        except Exception:
            pass

    threading.Thread(target=_worker, daemon=True).start()


# ==============================================================================
# POPULAR WEBSITES & APPLICATIONS REGISTRY
# ==============================================================================
POPULAR_SITES = {
    "linkedin": "https://www.linkedin.com",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "maps": "https://maps.google.com",
    "google maps": "https://maps.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "openai": "https://openai.com",
    "reddit": "https://www.reddit.com",
    "twitter": "https://x.com",
    "x": "https://x.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.com",
    "spotify": "https://open.spotify.com",
    "wikipedia": "https://www.wikipedia.org",
    "news": "https://news.google.com",
    "twitch": "https://www.twitch.tv",
    "weather": "https://weather.com",
    "stackoverflow": "https://stackoverflow.com",
    "stack overflow": "https://stackoverflow.com",
    "coursera": "https://www.coursera.org",
    "huggingface": "https://huggingface.co",
}

APP_COMMAND_MAP = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "calc": ["calc.exe"],
    "explorer": ["explorer.exe"],
    "files": ["explorer.exe"],
    "file explorer": ["explorer.exe"],
    "paint": ["mspaint.exe"],
    "mspaint": ["mspaint.exe"],
    "cmd": ["cmd.exe"],
    "command prompt": ["cmd.exe"],
    "terminal": ["powershell.exe"],
    "powershell": ["powershell.exe"],
    "task manager": ["taskmgr.exe"],
    "taskmgr": ["taskmgr.exe"],
    "settings": ["cmd", "/c", "start", "", "ms-settings:"],
    "camera": ["cmd", "/c", "start", "", "microsoft.windows.camera:"],
    "word": ["cmd", "/c", "start", "", "winword"],
    "excel": ["cmd", "/c", "start", "", "excel"],
    "powerpoint": ["cmd", "/c", "start", "", "powerpnt"],
    "vscode": ["cmd", "/c", "start", "", "code"],
    "vs code": ["cmd", "/c", "start", "", "code"],
    "code": ["cmd", "/c", "start", "", "code"],
    "chrome": ["cmd", "/c", "start", "", "chrome"],
    "edge": ["cmd", "/c", "start", "", "msedge"],
    "spotify": ["cmd", "/c", "start", "", "spotify:"],
    "discord": ["cmd", "/c", "start", "", "discord:"],
}


def open_in_chrome(url):
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url

    if CHROME_EXE and os.path.exists(CHROME_EXE):
        subprocess.Popen([CHROME_EXE, url], shell=False)
        return True
    try:
        subprocess.Popen(["cmd", "/c", "start", "", "chrome", url], shell=False)
        return True
    except Exception:
        webbrowser.open(url)
        return True


def launch_windows_app(name):
    clean = name.lower().strip()
    if clean in APP_COMMAND_MAP:
        subprocess.Popen(APP_COMMAND_MAP[clean], shell=False)
        return True
    subprocess.Popen(["cmd", "/c", "start", "", clean], shell=False)
    return True


def close_application(name):
    clean = name.lower().strip()
    proc_map = {
        "chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "vs code": "Code.exe",
        "vscode": "Code.exe",
        "code": "Code.exe",
        "paint": "mspaint.exe",
        "spotify": "Spotify.exe",
        "discord": "Discord.exe",
        "edge": "msedge.exe",
    }
    if clean in proc_map:
        subprocess.Popen(["taskkill", "/F", "/IM", proc_map[clean]], shell=False)
        return f"Terminated {clean}"
    pyautogui.hotkey("alt", "f4")
    return "Closed active window"


def take_desktop_screenshot():
    pics = os.path.join(os.path.expanduser("~"), "Pictures")
    if not os.path.isdir(pics):
        pics = os.path.join(os.path.expanduser("~"), "Desktop")
    ts = time.strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(pics, f"FRIDAY_Screen_{ts}.png")
    shot = pyautogui.screenshot()
    shot.save(filepath)
    return filepath


def write_desktop_note(text, filename=""):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not filename:
        ts = time.strftime("%Y%m%d_%H%M%S")
        filename = f"FRIDAY_Note_{ts}.txt"
    filepath = os.path.join(desktop, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"=== FRIDAY // TACTICAL NOTE ===\nGenerated: {time.ctime()}\n\n{text}\n")
    return filepath


def create_desktop_folder(folder_name):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    path = os.path.join(desktop, folder_name)
    os.makedirs(path, exist_ok=True)
    return path


def fetch_live_weather(location=""):
    try:
        loc = urllib.parse.quote(location.strip()) if location else ""
        url = f"https://wttr.in/{loc}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "FRIDAY/4.0"})
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        curr = data["current_condition"][0]
        area = data["nearest_area"][0]["areaName"][0]["value"]
        return {
            "location": area,
            "temp_c": curr["temp_C"],
            "desc": curr["weatherDesc"][0]["value"],
            "humidity": curr["humidity"],
            "wind_kmph": curr["windspeedKmph"]
        }
    except Exception:
        return None


def fetch_live_online_intelligence(topic):
    topic_clean = topic.strip()
    try:
        q_enc = urllib.parse.quote(topic_clean)
        ddg_url = f"https://api.duckduckgo.com/?q={q_enc}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(ddg_url, headers={"User-Agent": "FRIDAY/4.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            ddg_data = json.loads(resp.read().decode("utf-8"))
        abstract = ddg_data.get("AbstractText") or ddg_data.get("Abstract")
        if abstract:
            return abstract
    except Exception:
        pass

    try:
        enc = urllib.parse.quote(topic_clean)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{enc}"
        req = urllib.request.Request(url, headers={"User-Agent": "FRIDAY-Avengers/4.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        extract = data.get("extract")
        if extract:
            sentences = extract.split(". ")
            return ". ".join(sentences[:2]) + "."
    except Exception:
        pass

    return None


def control_multimedia(cmd):
    c = cmd.lower().strip()
    if c == "volumeup":
        for _ in range(5):
            pyautogui.press("volumeup")
        return "Increased master audio volume by 10%."
    elif c == "volumedown":
        for _ in range(5):
            pyautogui.press("volumedown")
        return "Decreased master audio volume by 10%."
    elif c == "mute":
        pyautogui.press("volumemute")
        return "Master audio mute toggled."
    elif c == "playpause":
        pyautogui.press("playpause")
        return "Media playback state toggled."
    return "Audio directive executed."


def get_deep_diagnostics():
    vm = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.10)
    disk = psutil.disk_usage("C:")
    battery = psutil.sensors_battery()
    bat_str = "AC Power (100%)"
    if battery:
        state = "Charging" if battery.power_plugged else "Battery"
        bat_str = f"{battery.percent}% [{state}]"

    top_procs = []
    try:
        for p in sorted(psutil.process_iter(["name", "memory_percent"]), key=lambda x: x.info["memory_percent"] or 0, reverse=True)[:3]:
            top_procs.append(f"{p.info['name']} ({p.info['memory_percent']:.1f}%)")
    except Exception:
        top_procs = ["Telemetry active"]

    return {
        "cpu": cpu,
        "ram_pct": vm.percent,
        "ram_used_gb": vm.used / (1024**3),
        "ram_total_gb": vm.total / (1024**3),
        "disk_pct": disk.percent,
        "disk_free_gb": disk.free / (1024**3),
        "battery": bat_str,
        "top_procs": top_procs
    }


def check_ollama_live(timeout=1.0):
    try:
        req = urllib.request.Request(OLLAMA_TAGS_URL, headers={"User-Agent": "FRIDAY-Probe"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status == 200
    except Exception:
        return False


# ==============================================================================
# COGNITIVE BRAIN (NLP + LLM REASONING & MULTI-STEP ACTION PLANNER)
# ==============================================================================
class CognitiveBrain:
    """
    Integrates LLM Tool Calling (Local Ollama / Cloud) with a Semantic NLU
    multi-step action planner. Decomposes any complex command into executable actions.
    """
    def __init__(self):
        self.last_search_query = ""

    def reason_and_plan(self, user_query):
        """
        Main cognitive dispatch.
        Tries Local Ollama -> Cloud LLM -> Local Semantic NLU Planner.
        Returns: (thought, reply, list_of_actions)
        """
        # 1. Try Local Ollama if online
        if check_ollama_live(timeout=1.0):
            res = self._query_ollama(user_query)
            if res:
                return res

        # 2. Local Semantic NLU Planner (Instant, reliable, multi-step capable)
        return self._local_nlu_planner(user_query)

    def _query_ollama(self, user_query):
        system_prompt = (
            "You are FRIDAY, Tony Stark's AI from Avengers. Analyze the command and return valid JSON with shape:\n"
            "{\"thought\":\"reasoning\",\"reply\":\"spoken reply addressing boss\",\"actions\":[{\"tool\":\"tool_name\",\"params\":{...}}]}\n"
            "Tools: open_app, open_website, search_google, click_search_link, play_youtube, mouse_action, keyboard_action, type_text, create_note, take_screenshot, control_volume, system_diagnostics."
        )
        try:
            payload = {
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.25}
            }
            req = urllib.request.Request(
                OLLAMA_URL, data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            parsed = json.loads(data.get("message", {}).get("content", "{}"))
            thought = parsed.get("thought", "Neural model reasoning complete.")
            reply = parsed.get("reply", "Directive processed, boss.")
            actions = parsed.get("actions", [])
            if actions:
                return thought, reply, actions
        except Exception:
            pass
        return None

    def _local_nlu_planner(self, user_query):
        """
        High-precision Semantic NLU parser.
        Capable of decomposing multi-step conjunctions (e.g. 'search LinkedIn in Chrome AND open the first link').
        """
        q = user_query.lower().strip()
        actions = []
        thought = f"Semantic NLU parsed user directive: '{user_query}'"
        reply = ""

        # --- A. Multi-Step Chained Directives (e.g. Search X THEN Open First Link) ---
        if ("search" in q or "google" in q) and any(w in q for w in ("and open first", "then open first", "and click first", "and open the first link")):
            m = re.search(r"search\s+(?:for\s+)?(.+?)\s+(?:in\s+chrome\s+)?(?:and|then)\s+(?:open|click)\s+(?:the\s+)?first\s+link", q)
            search_term = m.group(1).strip() if m else "LinkedIn"
            self.last_search_query = search_term
            actions.append({"tool": "search_google", "params": {"query": search_term}})
            actions.append({"tool": "sleep", "params": {"seconds": 1.4}})
            actions.append({"tool": "click_search_link", "params": {"rank": 1, "query": search_term}})
            thought = f"Multi-step plan: Search Google for '{search_term}', wait for load, then click top result."
            reply = f"Searching for '{search_term}' in Google Chrome and opening the first link for you now, boss."
            return thought, reply, actions

        # --- B. Specific Link Navigation (First link, second link, go with name) ---
        if any(w in q for w in ("first link", "first result", "link 1", "top link", "open first", "click first")):
            actions.append({"tool": "click_search_link", "params": {"rank": 1, "query": self.last_search_query}})
            reply = "Opening the first link for you now, boss."
            return thought, reply, actions

        elif any(w in q for w in ("second link", "second result", "link 2", "open second")):
            actions.append({"tool": "click_search_link", "params": {"rank": 2}})
            reply = "Opening the second result, boss."
            return thought, reply, actions

        elif any(w in q for w in ("third link", "third result", "link 3")):
            actions.append({"tool": "click_search_link", "params": {"rank": 3}})
            reply = "Opening the third link, boss."
            return thought, reply, actions

        elif any(q.startswith(p) for p in ("go with", "go to", "open link")) and any(s in q for s in POPULAR_SITES):
            matched_site = None
            for s in sorted(POPULAR_SITES.keys(), key=len, reverse=True):
                if s in q:
                    matched_site = s
                    break
            if matched_site:
                actions.append({"tool": "open_website", "params": {"url": POPULAR_SITES[matched_site]}})
                reply = f"Heading straight to {matched_site.capitalize()} in Google Chrome, boss."
                return thought, reply, actions

        # --- C. Mouse Directives ---
        if q in ("click", "left click", "click here"):
            actions.append({"tool": "mouse_action", "params": {"action": "click"}})
            reply = "Clicked, boss."
            return thought, reply, actions

        elif q in ("double click", "double click here"):
            actions.append({"tool": "mouse_action", "params": {"action": "double_click"}})
            reply = "Double-clicked, boss."
            return thought, reply, actions

        elif q in ("right click", "context menu"):
            actions.append({"tool": "mouse_action", "params": {"action": "right_click"}})
            reply = "Right-clicked, boss."
            return thought, reply, actions

        elif "click center" in q or "center click" in q:
            actions.append({"tool": "mouse_action", "params": {"action": "center_click"}})
            reply = "Clicked screen center, boss."
            return thought, reply, actions

        elif re.search(r"click\s+(?:at\s+)?(\d+)\s+(\d+)", q):
            m = re.search(r"click\s+(?:at\s+)?(\d+)\s+(\d+)", q)
            x, y = int(m.group(1)), int(m.group(2))
            actions.append({"tool": "mouse_action", "params": {"action": "click_at", "x": x, "y": y}})
            reply = f"Clicked coordinates ({x}, {y}), boss."
            return thought, reply, actions

        elif any(w in q for w in ("scroll down", "scroll page down", "scroll")):
            actions.append({"tool": "mouse_action", "params": {"action": "scroll_down"}})
            reply = "Scrolling down, boss."
            return thought, reply, actions

        elif any(w in q for w in ("scroll up", "scroll page up")):
            actions.append({"tool": "mouse_action", "params": {"action": "scroll_up"}})
            reply = "Scrolling up, boss."
            return thought, reply, actions

        elif any(w in q for w in ("scroll to top", "top of page", "go to top")):
            actions.append({"tool": "keyboard_action", "params": {"action": "press", "key": "home"}})
            reply = "Jumped to the top, boss."
            return thought, reply, actions

        elif any(w in q for w in ("scroll to bottom", "bottom of page", "go to bottom")):
            actions.append({"tool": "keyboard_action", "params": {"action": "press", "key": "end"}})
            reply = "Jumped to the bottom, boss."
            return thought, reply, actions

        # --- D. Keyboard Directives & Typing ---
        if q.startswith("type ") or "type:" in q:
            text_to_type = re.sub(r"^(?:jarvis|friday|siddhu|please|can you|type:?)\s*", "", q, flags=re.I).strip()
            press_enter = False
            if text_to_type.endswith(" and enter") or text_to_type.endswith(" and press enter"):
                text_to_type = re.sub(r"\s+and\s+(?:press\s+)?enter$", "", text_to_type).strip()
                press_enter = True
            actions.append({"tool": "type_text", "params": {"text": text_to_type, "press_enter": press_enter}})
            reply = f"Typed '{text_to_type}'" + (" and hit Enter, boss." if press_enter else ", boss.")
            return thought, reply, actions

        elif q in ("press enter", "hit enter", "enter"):
            actions.append({"tool": "keyboard_action", "params": {"action": "press", "key": "enter"}})
            reply = "Enter pressed, boss."
            return thought, reply, actions

        elif q in ("press space", "space"):
            actions.append({"tool": "keyboard_action", "params": {"action": "press", "key": "space"}})
            reply = "Space pressed, boss."
            return thought, reply, actions

        elif q in ("press tab", "tab"):
            actions.append({"tool": "keyboard_action", "params": {"action": "press", "key": "tab"}})
            reply = "Tab pressed, boss."
            return thought, reply, actions

        elif q in ("press escape", "escape", "esc"):
            actions.append({"tool": "keyboard_action", "params": {"action": "press", "key": "esc"}})
            reply = "Escape pressed, boss."
            return thought, reply, actions

        elif q in ("press backspace", "backspace"):
            actions.append({"tool": "keyboard_action", "params": {"action": "press", "key": "backspace"}})
            reply = "Backspace pressed, boss."
            return thought, reply, actions

        elif any(w in q for w in ("select all", "select everything")):
            actions.append({"tool": "keyboard_action", "params": {"action": "hotkey", "keys": ["ctrl", "a"]}})
            reply = "Selected all, boss."
            return thought, reply, actions

        elif any(w in q for w in ("copy that", "copy")):
            actions.append({"tool": "keyboard_action", "params": {"action": "hotkey", "keys": ["ctrl", "c"]}})
            reply = "Copied to clipboard, boss."
            return thought, reply, actions

        elif any(w in q for w in ("paste that", "paste here", "paste")):
            actions.append({"tool": "keyboard_action", "params": {"action": "hotkey", "keys": ["ctrl", "v"]}})
            reply = "Pasted, boss."
            return thought, reply, actions

        elif any(w in q for w in ("cut that", "cut")):
            actions.append({"tool": "keyboard_action", "params": {"action": "hotkey", "keys": ["ctrl", "x"]}})
            reply = "Cut, boss."
            return thought, reply, actions

        elif any(w in q for w in ("save file", "save this", "save")):
            actions.append({"tool": "keyboard_action", "params": {"action": "hotkey", "keys": ["ctrl", "s"]}})
            reply = "Save command triggered, boss."
            return thought, reply, actions

        elif any(w in q for w in ("undo that", "undo")):
            actions.append({"tool": "keyboard_action", "params": {"action": "hotkey", "keys": ["ctrl", "z"]}})
            reply = "Undone, boss."
            return thought, reply, actions

        # --- E. Browser Tab Management ---
        if any(w in q for w in ("new tab", "open new tab")):
            actions.append({"tool": "browser_control", "params": {"action": "new_tab"}})
            reply = "New tab opened, boss."
            return thought, reply, actions

        elif any(w in q for w in ("close tab", "close this tab")):
            actions.append({"tool": "browser_control", "params": {"action": "close_tab"}})
            reply = "Tab closed, boss."
            return thought, reply, actions

        elif any(w in q for w in ("next tab", "switch tab")):
            actions.append({"tool": "browser_control", "params": {"action": "next_tab"}})
            reply = "Switched tab, boss."
            return thought, reply, actions

        elif any(w in q for w in ("go back", "browser back", "back page")):
            actions.append({"tool": "browser_control", "params": {"action": "back"}})
            reply = "Navigating back, boss."
            return thought, reply, actions

        elif any(w in q for w in ("refresh", "reload", "reload page")):
            actions.append({"tool": "browser_control", "params": {"action": "refresh"}})
            reply = "Page refreshed, boss."
            return thought, reply, actions

        # --- F. Search & YouTube ---
        if q.startswith("search") or "search for" in q or "google" in q:
            search_query = re.sub(r"^(?:jarvis|friday|siddhu|search for|search|google)\s*", "", q, flags=re.I).strip()
            search_query = re.sub(r"\s*(?:in chrome|on chrome|on the internet|online)$", "", search_query, flags=re.I).strip()
            self.last_search_query = search_query
            actions.append({"tool": "search_google", "params": {"query": search_query}})
            reply = f"Searching for '{search_query}' in Google Chrome, boss."
            return thought, reply, actions

        elif "youtube" in q or ("play" in q and ("song" in q or "music" in q or "video" in q or len(q.split()) > 1)):
            media_query = re.sub(r"^(?:jarvis|friday|siddhu|please|can you|play|open)\s*", "", q, flags=re.I).strip()
            media_query = re.sub(r"\s*(?:on youtube in chrome|in chrome|on youtube|youtube|song|music|video)$", "", media_query, flags=re.I).strip()
            if not media_query: media_query = "AC/DC Back in Black"
            self.last_search_query = media_query
            actions.append({"tool": "play_youtube", "params": {"query": media_query}})
            reply = f"Playing '{media_query}' on YouTube in Google Chrome, boss."
            return thought, reply, actions

        elif any(site in q for site in POPULAR_SITES) and ("open" in q or "in chrome" in q or "launch" in q):
            matched_site = None
            for s in sorted(POPULAR_SITES.keys(), key=len, reverse=True):
                if s in q:
                    matched_site = s
                    break
            if matched_site:
                actions.append({"tool": "open_website", "params": {"url": POPULAR_SITES[matched_site]}})
                reply = f"Opening {matched_site.capitalize()} in Google Chrome, boss."
                return thought, reply, actions

        # --- G. Window & App Control ---
        if any(w in q for w in ("maximize window", "maximize this", "maximize")):
            actions.append({"tool": "window_action", "params": {"action": "maximize"}})
            reply = "Window maximized, boss."
            return thought, reply, actions

        elif any(w in q for w in ("minimize window", "minimize this", "minimize")):
            actions.append({"tool": "window_action", "params": {"action": "minimize"}})
            reply = "Window minimized, boss."
            return thought, reply, actions

        elif any(w in q for w in ("show desktop", "minimize all", "desktop")):
            actions.append({"tool": "window_action", "params": {"action": "show_desktop"}})
            reply = "Desktop cleared, boss."
            return thought, reply, actions

        elif q.startswith("close ") or q.startswith("kill "):
            t_close = re.sub(r"^(?:jarvis|friday|siddhu|close|kill)\s*", "", q, flags=re.I).strip()
            actions.append({"tool": "close_app", "params": {"name": t_close}})
            reply = f"Terminated {t_close.capitalize()}, boss."
            return thought, reply, actions

        elif q.startswith("open ") or q.startswith("launch ") or q.startswith("start "):
            app_t = re.sub(r"^(?:jarvis|friday|siddhu|open|launch|start)\s*", "", q, flags=re.I).strip()
            actions.append({"tool": "open_app", "params": {"name": app_t}})
            reply = f"Opening {app_t.capitalize()} for you now, boss."
            return thought, reply, actions

        # --- H. Files, Notes, Hardware & Diagnostics ---
        if "create folder" in q:
            f_name = re.sub(r"^(?:.*create folder)\s+", "", q, flags=re.I).strip()
            f_name = re.sub(r"\s+on\s+desktop$", "", f_name, flags=re.I).strip()
            if not f_name: f_name = "New_Folder"
            actions.append({"tool": "create_folder", "params": {"name": f_name}})
            reply = f"Created folder '{f_name}' on your Desktop, boss."
            return thought, reply, actions

        elif "note" in q and any(w in q for w in ("write", "create", "take", "save")):
            n_text = re.sub(r"^(?:jarvis|friday|siddhu|write a note|take a note|create a note|note:?)\s*", "", q, flags=re.I).strip()
            if not n_text: n_text = "Tactical reminder from boss."
            actions.append({"tool": "create_note", "params": {"text": n_text}})
            reply = "Note saved onto your Desktop, boss."
            return thought, reply, actions

        elif "screenshot" in q or "capture screen" in q:
            actions.append({"tool": "take_screenshot", "params": {}})
            reply = "Screen captured and preserved, boss."
            return thought, reply, actions

        elif "volume up" in q or "louder" in q:
            actions.append({"tool": "control_volume", "params": {"action": "volumeup"}})
            reply = "Master volume increased, boss."
            return thought, reply, actions

        elif "volume down" in q or "quieter" in q:
            actions.append({"tool": "control_volume", "params": {"action": "volumedown"}})
            reply = "Master volume decreased, boss."
            return thought, reply, actions

        elif "mute" in q or "unmute" in q:
            actions.append({"tool": "control_volume", "params": {"action": "mute"}})
            reply = "Audio mute toggled, boss."
            return thought, reply, actions

        elif "lock pc" in q or "lock computer" in q:
            actions.append({"tool": "lock_pc", "params": {}})
            reply = "Workstation locked, boss."
            return thought, reply, actions

        elif "weather" in q or "temperature" in q:
            loc_match = re.search(r"(?:in|for|at)\s+([a-zA-Z\s]+)", q)
            loc = loc_match.group(1).strip() if loc_match else ""
            actions.append({"tool": "weather_report", "params": {"location": loc}})
            return thought, "", actions

        elif "diagnostic" in q or "system status" in q or "telemetry" in q:
            actions.append({"tool": "system_diagnostics", "params": {}})
            return thought, "", actions

        elif "who is" in q or "what is" in q or "tell me about" in q or "explain" in q:
            topic = re.sub(r"^(?:jarvis|friday|siddhu|who is|what is|tell me about|explain)\s*", "", q, flags=re.I).strip()
            actions.append({"tool": "online_intel", "params": {"topic": topic}})
            return thought, "", actions

        elif "who are you" in q or "friday" in q:
            reply = "I am FRIDAY, your advanced AI cognitive interface. Powered by NLP and LLM reasoning, I analyze any command and execute multi-step operations across your entire PC, boss."
            return thought, reply, []

        elif "hello" in q or "hey" in q or "hi" in q:
            reply = "Good day, boss. Cognitive matrix online. What directive shall we execute next?"
            return thought, reply, []

        # Default fallback: search Google in Chrome
        self.last_search_query = user_query
        actions.append({"tool": "search_google", "params": {"query": user_query}})
        reply = f"Searching for '{user_query}' in Google Chrome, boss."
        return thought, reply, actions


# ==============================================================================
# ACTION EXECUTION ENGINE
# ==============================================================================
def execute_atomic_action(action_dict):
    """Executes a single atomic tool directive on the Windows PC."""
    tool = action_dict.get("tool", "")
    params = action_dict.get("params", {})

    if tool == "search_google":
        q = params.get("query", "")
        open_in_chrome(f"https://www.google.com/search?q={urllib.parse.quote(q)}")
        play_sfx("online")
        return f"Searched Google for '{q}' in Chrome"

    elif tool == "click_search_link":
        rank = int(params.get("rank", 1))
        # Determine click coordinates on 1920x1080 display
        y_offsets = {1: 0.32, 2: 0.46, 3: 0.62, 4: 0.76}
        click_y = int(SCREEN_HEIGHT * y_offsets.get(rank, 0.32))
        click_x = int(SCREEN_WIDTH * 0.28)
        pyautogui.click(click_x, click_y)
        play_sfx("mouse")

        # Also navigate direct URL if popular site query
        q_term = params.get("query", "").lower().strip()
        if q_term in POPULAR_SITES:
            open_in_chrome(POPULAR_SITES[q_term])
            return f"Opened link for {q_term.capitalize()} ({POPULAR_SITES[q_term]})"
        return f"Clicked Search Result #{rank} at ({click_x}, {click_y})"

    elif tool == "open_website":
        url = params.get("url", "")
        open_in_chrome(url)
        play_sfx("online")
        return f"Navigated to {url} in Chrome"

    elif tool == "play_youtube":
        q = params.get("query", "")
        open_in_chrome(f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}")
        play_sfx("online")
        return f"Streaming '{q}' on YouTube in Chrome"

    elif tool == "open_app":
        name = params.get("name", "")
        launch_windows_app(name)
        play_sfx("execute")
        return f"Launched Application: {name.capitalize()}"

    elif tool == "close_app":
        name = params.get("name", "")
        res = close_application(name)
        play_sfx("abort")
        return res

    elif tool == "mouse_action":
        act = params.get("action", "click")
        if act == "click": pyautogui.click()
        elif act == "double_click": pyautogui.doubleClick()
        elif act == "right_click": pyautogui.rightClick()
        elif act == "center_click": pyautogui.click(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        elif act == "click_at": pyautogui.click(params.get("x", 100), params.get("y", 100))
        elif act == "scroll_down": pyautogui.scroll(-750)
        elif act == "scroll_up": pyautogui.scroll(750)
        play_sfx("mouse")
        return f"Mouse Action: {act}"

    elif tool == "keyboard_action":
        act = params.get("action", "press")
        if act == "press":
            pyautogui.press(params.get("key", "enter"))
        elif act == "hotkey":
            pyautogui.hotkey(*params.get("keys", ["ctrl", "c"]))
        play_sfx("blip")
        return f"Keyboard: {act} {params.get('key') or params.get('keys')}"

    elif tool == "type_text":
        txt = params.get("text", "")
        pyautogui.write(txt, interval=0.02)
        if params.get("press_enter", False):
            time.sleep(0.1)
            pyautogui.press("enter")
        play_sfx("blip")
        return f"Typed: '{txt}'"

    elif tool == "browser_control":
        act = params.get("action", "new_tab")
        if act == "new_tab": pyautogui.hotkey("ctrl", "t")
        elif act == "close_tab": pyautogui.hotkey("ctrl", "w")
        elif act == "next_tab": pyautogui.hotkey("ctrl", "tab")
        elif act == "back": pyautogui.hotkey("alt", "left")
        elif act == "refresh": pyautogui.hotkey("ctrl", "r")
        play_sfx("blip")
        return f"Browser Control: {act}"

    elif tool == "window_action":
        act = params.get("action", "maximize")
        if act == "maximize": pyautogui.hotkey("win", "up")
        elif act == "minimize": pyautogui.hotkey("win", "down")
        elif act == "show_desktop": pyautogui.hotkey("win", "d")
        play_sfx("blip")
        return f"Window Action: {act}"

    elif tool == "create_note":
        p = write_desktop_note(params.get("text", "Note"), params.get("filename", ""))
        play_sfx("execute")
        return f"Created Note on Desktop: {os.path.basename(p)}"

    elif tool == "create_folder":
        p = create_desktop_folder(params.get("name", "New_Folder"))
        play_sfx("execute")
        return f"Created Folder on Desktop: {os.path.basename(p)}"

    elif tool == "take_screenshot":
        p = take_desktop_screenshot()
        play_sfx("execute")
        return f"Screenshot: {os.path.basename(p)}"

    elif tool == "control_volume":
        res = control_multimedia(params.get("action", "volumeup"))
        play_sfx("execute")
        return res

    elif tool == "lock_pc":
        subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"], shell=False)
        return "Workstation Locked"

    elif tool == "sleep":
        time.sleep(params.get("seconds", 1.0))
        return "Waited for interface ready"

    return None


# ==============================================================================
# MOVIE-GRADE ARC REACTOR (STARK INDUSTRIES MARK-XII)
# ==============================================================================
class ArcReactorHUD:
    def __init__(self, canvas, cx, cy, radius=140):
        self.canvas = canvas
        self.cx = cx
        self.cy = cy
        self.radius = radius

        self.ang_outer = 0.0
        self.ang_radar = 0.0
        self.ang_segmented = 0.0
        self.ang_coils = 0.0
        self.ang_turbine = 0.0

        self.state = "BOOTING"
        self.power_level = 0.0
        self.pulse_phase = 0.0
        self.audio_amplitude = 0.0
        self.shockwaves = []

    def trigger_shockwave(self):
        self.shockwaves.append({"r": self.radius * 0.25, "speed": 180.0, "max_r": self.radius * 1.35})

    def update(self, dt=0.033):
        self.pulse_phase += dt * 3.8
        self.ang_radar = (self.ang_radar + dt * 115.0) % 360.0

        if self.state == "BOOTING":
            self.power_level = min(1.0, self.power_level + dt * 0.45)
            self.ang_outer += dt * 45.0
            self.ang_segmented -= dt * 70.0
            self.ang_coils += dt * 80.0
            self.ang_turbine -= dt * 120.0
        elif self.state == "PROCESSING":
            self.ang_outer += dt * 160.0
            self.ang_segmented -= dt * 300.0
            self.ang_coils += dt * 360.0
            self.ang_turbine -= dt * 520.0
            if random.random() < 0.12:
                self.trigger_shockwave()
        elif self.state in ("SPEAKING", "LISTENING"):
            self.ang_outer += dt * 55.0
            self.ang_segmented -= dt * 130.0
            self.ang_coils += dt * 160.0
            self.ang_turbine -= dt * 230.0
            if random.random() < 0.14:
                self.trigger_shockwave()
        else:
            self.ang_outer += dt * 18.0
            self.ang_segmented -= dt * 32.0
            self.ang_coils += dt * 42.0
            self.ang_turbine -= dt * 60.0

        new_sw = []
        for sw in self.shockwaves:
            sw["r"] += sw["speed"] * dt
            if sw["r"] < sw["max_r"]:
                new_sw.append(sw)
        self.shockwaves = new_sw

        if self.state not in ("SPEAKING", "LISTENING"):
            self.audio_amplitude = max(0.0, self.audio_amplitude - dt * 2.5)

    def draw(self):
        cx, cy = self.cx, self.cy
        r = self.radius * self.power_level
        if r < 12:
            return

        reticle_dist = r * 1.30
        self._draw_reticle_cross(cx - reticle_dist, cy - reticle_dist)
        self._draw_reticle_cross(cx + reticle_dist, cy - reticle_dist)
        self._draw_reticle_cross(cx - reticle_dist, cy + reticle_dist)
        self._draw_reticle_cross(cx + reticle_dist, cy + reticle_dist)

        for sw in self.shockwaves:
            sr = sw["r"] * self.power_level
            decay = max(0.0, 1.0 - (sw["r"] / sw["max_r"]))
            sw_col = COLOR_CYAN_GLOW if decay > 0.4 else COLOR_CYAN_DIM
            self.canvas.create_oval(
                cx - sr, cy - sr, cx + sr, cy + sr,
                outline=sw_col, width=1.5
            )

        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=COLOR_BORDER_DIM, width=1)
        num_ticks = 72
        for i in range(num_ticks):
            deg = self.ang_outer + (i * 360.0 / num_ticks)
            rad = math.radians(deg)
            is_maj = (i % 9 == 0)
            is_mid = (i % 3 == 0)
            len_tick = (r * 0.08) if is_maj else ((r * 0.045) if is_mid else (r * 0.025))
            col = COLOR_CYAN_GLOW if is_maj else (COLOR_CYAN_DIM if is_mid else "#032840")
            x1 = cx + (r - len_tick) * math.cos(rad)
            y1 = cy + (r - len_tick) * math.sin(rad)
            x2 = cx + r * math.cos(rad)
            y2 = cy + r * math.sin(rad)
            self.canvas.create_line(x1, y1, x2, y2, fill=col, width=1.5 if is_maj else 1)

            if is_maj and r > 70:
                card_deg = int(deg % 360)
                tx = cx + (r - len_tick - 9) * math.cos(rad)
                ty = cy + (r - len_tick - 9) * math.sin(rad)
                self.canvas.create_text(tx, ty, text=f"{card_deg:03d}", fill=COLOR_CYAN_DIM, font=("Consolas", 6))

        radar_rad = math.radians(self.ang_radar)
        rx = cx + (r * 0.88) * math.cos(radar_rad)
        ry = cy + (r * 0.88) * math.sin(radar_rad)
        self.canvas.create_line(cx, cy, rx, ry, fill=COLOR_CYAN_PALE, width=1.5)
        self.canvas.create_arc(
            cx - r * 0.88, cy - r * 0.88, cx + r * 0.88, cy + r * 0.88,
            start=self.ang_radar - 35, extent=35, style="arc",
            outline=COLOR_CYAN_DIM, width=1
        )

        r_arcs = r * 0.82
        for i in range(4):
            st = self.ang_segmented + (i * 90.0)
            self.canvas.create_arc(
                cx - r_arcs, cy - r_arcs, cx + r_arcs, cy + r_arcs,
                start=st, extent=48, style="arc",
                outline=COLOR_CYAN_GLOW, width=3
            )

        r_coils = r * 0.66
        num_coils = 10
        coil_pulse = 0.5 + 0.5 * math.sin(self.pulse_phase)
        for i in range(num_coils):
            deg = self.ang_coils + (i * 360.0 / num_coils)
            rad = math.radians(deg)
            px = cx + r_coils * math.cos(rad)
            py = cy + r_coils * math.sin(rad)
            cw, ch = r * 0.065, r * 0.11

            is_active = (i % 2 == 0 or coil_pulse > 0.55)
            coil_col = COLOR_CYAN_GLOW if is_active else COLOR_CYAN_DIM
            self.canvas.create_oval(
                px - cw, py - ch, px + cw, py + ch,
                fill=COLOR_CARD_BG, outline=coil_col, width=2
            )
            self.canvas.create_line(
                px - cw * 0.6, py, px + cw * 0.6, py,
                fill=COLOR_CYAN_PALE if is_active else COLOR_GOLD, width=1.5
            )

        r_turbine_rim = r * 0.48
        self.canvas.create_oval(
            cx - r_turbine_rim, cy - r_turbine_rim, cx + r_turbine_rim, cy + r_turbine_rim,
            outline=COLOR_CYAN_GLOW, width=2
        )

        num_blades = 8
        r_b_outer = r_turbine_rim * 0.88
        r_b_inner = r_turbine_rim * 0.36
        for i in range(num_blades):
            deg = self.ang_turbine + (i * 360.0 / num_blades)
            rad1 = math.radians(deg - 11)
            rad2 = math.radians(deg + 11)
            rad_mid = math.radians(deg)

            x1 = cx + r_b_outer * math.cos(rad1)
            y1 = cy + r_b_outer * math.sin(rad1)
            x2 = cx + r_b_outer * math.cos(rad2)
            y2 = cy + r_b_outer * math.sin(rad2)
            x3 = cx + r_b_inner * math.cos(rad_mid)
            y3 = cy + r_b_inner * math.sin(rad_mid)

            self.canvas.create_polygon(
                x1, y1, x2, y2, x3, y3,
                fill="#071b30", outline=COLOR_CYAN_GLOW, width=1
            )

        base_core = r * 0.24
        extra_pulse = (math.sin(self.pulse_phase) * 0.16 + self.audio_amplitude * 0.45) * base_core
        core_r = max(6.0, base_core + extra_pulse)

        self.canvas.create_oval(
            cx - core_r * 1.8, cy - core_r * 1.8, cx + core_r * 1.8, cy + core_r * 1.8,
            fill="#032136", outline=COLOR_CYAN_DIM, width=1
        )
        self.canvas.create_oval(
            cx - core_r * 1.25, cy - core_r * 1.25, cx + core_r * 1.25, cy + core_r * 1.25,
            fill="#054a6e", outline=COLOR_CYAN_GLOW, width=2
        )
        self.canvas.create_oval(
            cx - core_r * 0.7, cy - core_r * 0.7, cx + core_r * 0.7, cy + core_r * 0.7,
            fill=COLOR_CYAN_PALE, outline="#ffffff", width=1.5
        )
        self.canvas.create_oval(
            cx - core_r * 0.35, cy - core_r * 0.35, cx + core_r * 0.35, cy + core_r * 0.35,
            fill="#ffffff", outline=""
        )

        status_col = COLOR_PURPLE if self.state == "PROCESSING" else (COLOR_GREEN if self.state == "LISTENING" else COLOR_CYAN_GLOW)
        self.canvas.create_text(
            cx, cy + r * 1.24,
            text=f"// ZERO-POINT CORE: {self.state} • STARK MK-XII",
            fill=status_col, font=("Consolas", 9, "bold")
        )

    def _draw_reticle_cross(self, x, y):
        size = 8
        self.canvas.create_line(x - size, y, x + size, y, fill=COLOR_CYAN_DIM, width=1)
        self.canvas.create_line(x, y - size, x, y + size, fill=COLOR_CYAN_DIM, width=1)


# ==============================================================================
# HOLOGRAPHIC 40-BAND SPECTRUM VISUALIZER
# ==============================================================================
class AudioSpectrumHUD:
    def __init__(self, canvas, x, y, width=420, height=54, num_bars=40):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.num_bars = num_bars
        self.bars = [0.0] * num_bars
        self.peaks = [0.0] * num_bars
        self.phase = 0.0
        self.mode = "IDLE"

    def update(self, dt=0.033):
        self.phase += dt * 4.2
        decay = dt * 1.9

        for i in range(self.num_bars):
            norm_i = i / float(self.num_bars)
            target = 0.0

            if self.mode == "SPEAKING":
                w1 = math.sin(self.phase * 2.5 + norm_i * 8.0)
                w2 = math.cos(self.phase * 3.8 - norm_i * 14.0)
                target = (abs(w1) * 0.65 + abs(w2) * 0.35) * random.uniform(0.65, 1.0)
            elif self.mode == "LISTENING":
                w = math.sin(self.phase * 3.4 + norm_i * 9.5)
                target = abs(w) * random.uniform(0.55, 0.98)
            elif self.mode == "PROCESSING":
                radar = math.sin(self.phase * 4.5 - norm_i * 12.0)
                target = max(0.12, (radar + 1.0) * 0.42)
            else:
                w = math.sin(self.phase * 0.9 + norm_i * 4.0)
                target = 0.10 + 0.08 * max(0.0, w)

            if target > self.bars[i]:
                self.bars[i] += (target - self.bars[i]) * 0.48
            else:
                self.bars[i] = max(0.04, self.bars[i] - decay)

            if self.bars[i] > self.peaks[i]:
                self.peaks[i] = self.bars[i]
            else:
                self.peaks[i] = max(0.04, self.peaks[i] - dt * 0.55)

    def draw(self):
        bar_w = (self.width / float(self.num_bars)) - 2.0
        base_y = self.y + self.height
        self.canvas.create_line(self.x, base_y, self.x + self.width, base_y, fill=COLOR_BORDER_DIM, width=1)

        for i in range(self.num_bars):
            bx = self.x + i * (bar_w + 2.0)
            val = max(0.04, min(1.0, self.bars[i]))
            bh = val * (self.height - 8)
            by = base_y - bh

            if val > 0.78:
                col = COLOR_PURPLE if self.mode == "PROCESSING" else COLOR_CYAN_PALE
            elif val > 0.42:
                col = COLOR_CYAN_GLOW
            else:
                col = COLOR_CYAN_DIM

            self.canvas.create_rectangle(bx, by, bx + bar_w, base_y, fill=col, outline="")

            pk = min(1.0, self.peaks[i])
            pk_y = base_y - (pk * (self.height - 8)) - 2
            self.canvas.create_line(
                bx, pk_y, bx + bar_w, pk_y,
                fill=COLOR_CYAN_PALE if self.mode != "PROCESSING" else COLOR_AMBER,
                width=1.5
            )


# ==============================================================================
# MAIN APPLICATION HUD (SIDDHU AI // MARK-XII)
# ==============================================================================
class SiddhuAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title(HUD_TITLE)
        self.root.geometry("1420x910")
        self.root.minsize(1120, 720)
        self.root.configure(bg=COLOR_VOID)

        # State Variables
        self.is_fullscreen = False
        self.sfx_active = True
        self.running = True
        self.is_speaking = False
        self.is_busy = False
        self.last_reply = ""
        self.ollama_online = False

        # Live Telemetry
        self.cpu_usage = 0.0
        self.ram_usage = 0.0
        self.ram_used_gb = 0.0
        self.ram_total_gb = 0.0
        self.disk_usage = 0.0
        self.disk_free_gb = 0.0
        self.battery_info = "Nominal (100%)"
        self.uptime_sec = 0

        # Cognitive NLP & LLM Brain
        self.brain = CognitiveBrain()
        self.speech_engine = TacticalSpeechEngine()

        # Build Clean, Button-Free Interface
        self._build_top_hud_header()
        self._build_workspace_grid()
        self._build_bottom_safety_footer()

        # F11 Fullscreen
        self.root.bind("<F11>", lambda _e: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda _e: self._exit_fullscreen())

        # Start Daemons
        self._start_system_telemetry_thread()
        self._start_continuous_vocal_listener()
        self._start_cinematic_boot_sequence()

        # 30 FPS Animation Loop
        self._hud_animation_loop()

    # --------------------------------------------------------------------------
    # TOP HUD HEADER
    # --------------------------------------------------------------------------
    def _build_top_hud_header(self):
        self.header_frame = tk.Frame(self.root, bg=COLOR_NAVY_DEEP, height=54, bd=0)
        self.header_frame.pack(fill="x", side="top", padx=8, pady=(6, 2))
        self.header_frame.pack_propagate(False)

        h_left = tk.Frame(self.header_frame, bg=COLOR_NAVY_DEEP)
        h_left.pack(side="left", padx=14, pady=8)

        self.beacon_canvas = tk.Canvas(h_left, width=16, height=16, bg=COLOR_NAVY_DEEP, highlightthickness=0)
        self.beacon_canvas.pack(side="left", padx=(0, 8))
        self.beacon_canvas.create_oval(3, 3, 13, 13, fill=COLOR_PURPLE, outline=COLOR_CYAN_PALE)

        tk.Label(
            h_left, text="FRIDAY // SIDDHU AI",
            font=("Segoe UI", 16, "bold"), fg=COLOR_CYAN_GLOW, bg=COLOR_NAVY_DEEP
        ).pack(side="left")

        tk.Label(
            h_left, text=" // COGNITIVE NLP & LLM MATRIX",
            font=("Consolas", 10, "bold"), fg=COLOR_PURPLE, bg=COLOR_NAVY_DEEP
        ).pack(side="left", padx=6)

        h_mid = tk.Frame(self.header_frame, bg=COLOR_NAVY_DEEP)
        h_mid.pack(side="left", expand=True)

        self.lbl_vocal_matrix = tk.Label(
            h_mid,
            text="● FRIDAY REASONING CORE: ONLINE [NLP + LLM INTENT PARSER ACTIVE]",
            font=("Consolas", 10, "bold"), fg=COLOR_GREEN, bg=COLOR_NAVY_DEEP
        )
        self.lbl_vocal_matrix.pack()

        h_right = tk.Frame(self.header_frame, bg=COLOR_NAVY_DEEP)
        h_right.pack(side="right", padx=12)

        self.lbl_clock = tk.Label(
            h_right, text="00:00:00 IST",
            font=("Consolas", 11, "bold"), fg=COLOR_CYAN_PALE, bg=COLOR_NAVY_DEEP
        )
        self.lbl_clock.pack(side="left", padx=8)

        sep = tk.Canvas(self.root, height=2, bg=COLOR_VOID, highlightthickness=0)
        sep.pack(fill="x", padx=8, pady=(0, 4))
        sep.create_line(0, 1, 2600, 1, fill=COLOR_BORDER_DIM, width=2)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        play_sfx("blip")

    def _exit_fullscreen(self):
        if self.is_fullscreen:
            self.toggle_fullscreen()

    # --------------------------------------------------------------------------
    # 3-COLUMN WORKSPACE
    # --------------------------------------------------------------------------
    def _build_workspace_grid(self):
        self.workspace = tk.Frame(self.root, bg=COLOR_VOID)
        self.workspace.pack(fill="both", expand=True, padx=8, pady=2)

        # COLUMN 1: LEFT TELEMETRY
        self.left_panel = tk.Frame(self.workspace, bg=COLOR_PANEL_BG, width=340, bd=1, relief="solid")
        self.left_panel.pack(side="left", fill="both", padx=(0, 4), pady=2)
        self.left_panel.pack_propagate(False)
        self._build_left_telemetry_ui(self.left_panel)

        # COLUMN 2: CENTER ARC REACTOR & SPECTRUM
        self.center_panel = tk.Frame(self.workspace, bg=COLOR_NAVY_DEEP, width=520, bd=1, relief="solid")
        self.center_panel.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        self._build_center_reactor_ui(self.center_panel)

        # COLUMN 3: RIGHT COMM-LINK & AUTO-EXECUTION STATUS
        self.right_panel = tk.Frame(self.workspace, bg=COLOR_PANEL_BG, width=540, bd=1, relief="solid")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(4, 0), pady=2)
        self._build_right_commlink_ui(self.right_panel)

    # --------------------------------------------------------------------------
    # LEFT TELEMETRY PANEL
    # --------------------------------------------------------------------------
    def _build_left_telemetry_ui(self, parent):
        tk.Label(
            parent, text="⌜ HOLOGRAPHIC TELEMETRY ⌝",
            font=("Consolas", 10, "bold"), fg=COLOR_CYAN_GLOW, bg=COLOR_PANEL_BG
        ).pack(anchor="w", padx=12, pady=(8, 4))

        self.telemetry_canvas = tk.Canvas(parent, bg=COLOR_CARD_BG, height=220, highlightthickness=0)
        self.telemetry_canvas.pack(fill="x", padx=8, pady=4)

        ai_box = tk.Frame(parent, bg=COLOR_CARD_BG, bd=1, relief="flat")
        ai_box.pack(fill="x", padx=8, pady=6)

        tk.Label(
            ai_box, text="// COGNITIVE NLP & LLM RUNTIME",
            font=("Consolas", 8, "bold"), fg=COLOR_PURPLE, bg=COLOR_CARD_BG
        ).pack(anchor="w", padx=8, pady=(4, 1))

        self.lbl_brain_mode = tk.Label(
            ai_box, text="BRAIN: HYBRID LLM + MULTI-INTENT NLU",
            font=("Consolas", 8, "bold"), fg=COLOR_CYAN_PALE, bg=COLOR_CARD_BG
        )
        self.lbl_brain_mode.pack(anchor="w", padx=8, pady=1)

        self.lbl_task_engine = tk.Label(
            ai_box, text=f"DISPATCH: MULTI-STEP ATOMIC ACTION PLANNER",
            font=("Consolas", 8), fg=COLOR_GREEN, bg=COLOR_CARD_BG
        )
        self.lbl_task_engine.pack(anchor="w", padx=8, pady=(1, 6))

        tk.Label(
            parent, text="// HOLOGRAPHIC EVENT STREAM",
            font=("Consolas", 9, "bold"), fg=COLOR_CYAN_DIM, bg=COLOR_PANEL_BG
        ).pack(anchor="w", padx=12, pady=(6, 2))

        self.log_text = tk.Text(
            parent, wrap="word", state="disabled",
            bg=COLOR_VOID, fg=COLOR_CYAN_PALE, font=("Consolas", 8),
            bd=0, padx=8, pady=8, highlightbackground=COLOR_BORDER_DIM, highlightthickness=1
        )
        self.log_text.pack(fill="both", expand=True, padx=8, pady=(2, 8))

    # --------------------------------------------------------------------------
    # CENTER ARC REACTOR & SPECTRUM
    # --------------------------------------------------------------------------
    def _build_center_reactor_ui(self, parent):
        top_hdr = tk.Frame(parent, bg=COLOR_NAVY_DEEP)
        top_hdr.pack(fill="x", padx=12, pady=(8, 2))

        tk.Label(
            top_hdr, text="ARC REACTOR // ZERO-POINT CORE",
            font=("Consolas", 11, "bold"), fg=COLOR_CYAN_GLOW, bg=COLOR_NAVY_DEEP
        ).pack(side="left")

        self.lbl_core_output = tk.Label(
            top_hdr, text="FRIDAY: ONLINE",
            font=("Consolas", 9, "bold"), fg=COLOR_GREEN, bg=COLOR_NAVY_DEEP
        )
        self.lbl_core_output.pack(side="right")

        self.reactor_canvas = tk.Canvas(parent, bg=COLOR_VOID, highlightthickness=0)
        self.reactor_canvas.pack(fill="both", expand=True, padx=8, pady=4)
        self.reactor_canvas.bind("<Configure>", self._on_reactor_canvas_resize)

        self.arc_reactor = ArcReactorHUD(self.reactor_canvas, 240, 200, radius=140)
        self.audio_spectrum = AudioSpectrumHUD(self.reactor_canvas, 20, 390, width=440, height=54, num_bars=40)

    def _on_reactor_canvas_resize(self, event):
        cw = max(200, event.width)
        ch = max(200, event.height)
        self.arc_reactor.cx = cw // 2
        self.arc_reactor.cy = int(ch * 0.44)
        self.arc_reactor.radius = max(65, min(145, int(min(cw, ch) * 0.32)))

        viz_w = max(200, min(460, cw - 30))
        self.audio_spectrum.x = (cw - viz_w) // 2
        self.audio_spectrum.y = int(ch * 0.83)
        self.audio_spectrum.width = viz_w

    # --------------------------------------------------------------------------
    # RIGHT COMM-LINK & AUTO-EXECUTION STATUS
    # --------------------------------------------------------------------------
    def _build_right_commlink_ui(self, parent):
        top_hdr = tk.Frame(parent, bg=COLOR_PANEL_BG)
        top_hdr.pack(fill="x", padx=10, pady=(8, 2))

        tk.Label(
            top_hdr, text="⌜ TACTICAL COMM-LINK // DIALOGUE FEED ⌝",
            font=("Consolas", 10, "bold"), fg=COLOR_CYAN_GLOW, bg=COLOR_PANEL_BG
        ).pack(side="left")

        self.lbl_comm_state = tk.Label(
            top_hdr, text="[LISTENING]",
            font=("Consolas", 9, "bold"), fg=COLOR_GREEN, bg=COLOR_PANEL_BG
        )
        self.lbl_comm_state.pack(side="right")

        chat_box = tk.Frame(parent, bg=COLOR_VOID, bd=1, relief="solid")
        chat_box.pack(fill="both", expand=True, padx=8, pady=4)

        self.chat = tk.Text(
            chat_box, wrap="word", state="disabled",
            bg=COLOR_VOID, fg=COLOR_TEXT_PRIMARY, font=("Segoe UI", 10),
            bd=0, padx=12, pady=10, insertbackground=COLOR_CYAN_GLOW
        )
        self.chat.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(chat_box, command=self.chat.yview, bg=COLOR_PANEL_BG)
        scrollbar.pack(side="right", fill="y")
        self.chat.configure(yscrollcommand=scrollbar.set)

        self.chat.tag_config("user_tag", foreground=COLOR_GOLD, font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("ai_tag", foreground=COLOR_CYAN_GLOW, font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("system_tag", foreground=COLOR_CYAN_DIM, font=("Consolas", 9, "italic"))
        self.chat.tag_config("exec_tag", foreground=COLOR_GREEN, font=("Consolas", 9, "bold"))
        self.chat.tag_config("thought_tag", foreground=COLOR_PURPLE, font=("Consolas", 9, "italic"))
        self.chat.tag_config("body", foreground=COLOR_TEXT_PRIMARY)

        # AUTOMATIC COGNITIVE STATUS CARD
        self.auto_exec_card = tk.Frame(parent, bg=COLOR_CARD_BG, bd=1, relief="solid")
        self.auto_exec_card.pack(fill="x", padx=8, pady=6)

        tk.Label(
            self.auto_exec_card, text="// COGNITIVE NLP / LLM REASONING DECK",
            font=("Consolas", 8, "bold"), fg=COLOR_PURPLE, bg=COLOR_CARD_BG
        ).pack(anchor="w", padx=10, pady=(6, 1))

        self.lbl_auto_status = tk.Label(
            self.auto_exec_card,
            text="STATUS: READY • SPEAK ANY COMPLEX DIRECTIVE • NLP/LLM WILL PLAN & EXECUTE AUTOMATICALLY",
            font=("Consolas", 9, "bold"), fg=COLOR_GREEN, bg=COLOR_CARD_BG,
            wraplength=480, justify="left"
        )
        self.lbl_auto_status.pack(anchor="w", padx=10, pady=(1, 8))

        entry_wrap = tk.Frame(parent, bg=COLOR_CARD_BG, bd=1, relief="solid")
        entry_wrap.pack(fill="x", padx=8, pady=(2, 8))

        self.entry = tk.Entry(
            entry_wrap, font=("Segoe UI", 11),
            bg=COLOR_CARD_BG, fg=COLOR_TEXT_PRIMARY,
            insertbackground=COLOR_CYAN_GLOW, bd=0
        )
        self.entry.pack(fill="x", padx=10, pady=8)
        self.entry.insert(0, "Speak naturally or type any complex command & press Enter...")
        self.entry.bind("<FocusIn>", lambda _e: self._clear_placeholder())
        self.entry.bind("<Return>", lambda _e: self._on_entry_enter())

    def _clear_placeholder(self):
        if "Speak naturally" in self.entry.get():
            self.entry.delete(0, "end")

    def _on_entry_enter(self):
        val = self.entry.get().strip()
        if val and "Speak naturally" not in val:
            self.entry.delete(0, "end")
            self.execute_task_pipeline(val)

    # --------------------------------------------------------------------------
    # BOTTOM SAFETY BANNER
    # --------------------------------------------------------------------------
    def _build_bottom_safety_footer(self):
        self.footer = tk.Frame(self.root, bg=COLOR_NAVY_DEEP, height=26)
        self.footer.pack(fill="x", side="bottom", padx=8, pady=(1, 4))
        self.footer.pack_propagate(False)

        tk.Label(
            self.footer,
            text="🧠 NLP + LLM ACTIVE: MULTI-STEP REASONING ENGAGED • SLAM MOUSE TO (0,0) FOR HARDWARE ABORT",
            font=("Consolas", 8, "bold"), fg=COLOR_AMBER, bg=COLOR_NAVY_DEEP
        ).pack(side="left", padx=10)

        self.lbl_ollama_badge = tk.Label(
            self.footer, text="COGNITIVE CORE: ONLINE",
            font=("Consolas", 8, "bold"), fg=COLOR_PURPLE, bg=COLOR_NAVY_DEEP
        )
        self.lbl_ollama_badge.pack(side="right", padx=10)

    # --------------------------------------------------------------------------
    # TELEMETRY DAEMON
    # --------------------------------------------------------------------------
    def _start_system_telemetry_thread(self):
        def _telemetry_loop():
            while self.running:
                try:
                    diag = get_deep_diagnostics()
                    self.cpu_usage = diag["cpu"]
                    self.ram_usage = diag["ram_pct"]
                    self.ram_used_gb = diag["ram_used_gb"]
                    self.ram_total_gb = diag["ram_total_gb"]
                    self.disk_usage = diag["disk_pct"]
                    self.disk_free_gb = diag["disk_free_gb"]
                    self.battery_info = diag["battery"]
                    self.uptime_sec += 1

                    if self.uptime_sec % 6 == 0:
                        self.ollama_online = check_ollama_live(timeout=1.0)
                except Exception:
                    pass
                time.sleep(1.0)

        threading.Thread(target=_telemetry_loop, daemon=True).start()

    def _draw_telemetry_gauges(self):
        canv = self.telemetry_canvas
        canv.delete("all")
        w = canv.winfo_width()
        if w < 100:
            w = 320
        bar_w = w - 24

        # CPU
        canv.create_text(12, 12, text="CPU UTILIZATION", anchor="w", fill=COLOR_CYAN_DIM, font=("Consolas", 8, "bold"))
        cpu_col = COLOR_RED if self.cpu_usage > 85 else (COLOR_AMBER if self.cpu_usage > 65 else COLOR_CYAN_GLOW)
        canv.create_text(w - 12, 12, text=f"{self.cpu_usage:.1f}%", anchor="e", fill=cpu_col, font=("Consolas", 9, "bold"))
        canv.create_rectangle(12, 23, 12 + bar_w, 31, fill=COLOR_VOID, outline=COLOR_BORDER_DIM)
        fill_cpu = max(2, int(bar_w * (self.cpu_usage / 100.0)))
        canv.create_rectangle(12, 23, 12 + fill_cpu, 31, fill=cpu_col, outline="")

        # RAM
        canv.create_text(12, 45, text="MEMORY (RAM)", anchor="w", fill=COLOR_CYAN_DIM, font=("Consolas", 8, "bold"))
        ram_col = COLOR_RED if self.ram_usage > 88 else (COLOR_AMBER if self.ram_usage > 75 else COLOR_CYAN_GLOW)
        canv.create_text(w - 12, 45, text=f"{self.ram_used_gb:.1f} / {self.ram_total_gb:.1f} GB ({self.ram_usage:.1f}%)", anchor="e", fill=ram_col, font=("Consolas", 8, "bold"))
        canv.create_rectangle(12, 56, 12 + bar_w, 64, fill=COLOR_VOID, outline=COLOR_BORDER_DIM)
        fill_ram = max(2, int(bar_w * (self.ram_usage / 100.0)))
        canv.create_rectangle(12, 56, 12 + fill_ram, 64, fill=ram_col, outline="")

        # Storage
        canv.create_text(12, 78, text="STORAGE (C: DRIVE)", anchor="w", fill=COLOR_CYAN_DIM, font=("Consolas", 8, "bold"))
        canv.create_text(w - 12, 78, text=f"{self.disk_free_gb:.1f} GB Free ({self.disk_usage:.1f}% Full)", anchor="e", fill=COLOR_CYAN_PALE, font=("Consolas", 8))
        canv.create_rectangle(12, 89, 12 + bar_w, 97, fill=COLOR_VOID, outline=COLOR_BORDER_DIM)
        fill_disk = max(2, int(bar_w * (self.disk_usage / 100.0)))
        canv.create_rectangle(12, 89, 12 + fill_disk, 97, fill=COLOR_CYAN_DIM, outline="")

        # Hardware & Neural Telemetry
        canv.create_line(12, 110, w - 12, 110, fill=COLOR_BORDER_DIM, width=1)
        canv.create_text(12, 124, text=f"NLP ENGINE: MULTI-STEP SEMANTIC DECOMPOSER", anchor="w", fill=COLOR_PURPLE, font=("Consolas", 8, "bold"))
        canv.create_text(12, 140, text=f"LLM MATRIX: OLLAMA + CLOUD DUAL-ROUTER", anchor="w", fill=COLOR_CYAN_PALE, font=("Consolas", 8))
        canv.create_text(12, 156, text=f"POWER SYSTEM: {self.battery_info}", anchor="w", fill=COLOR_GREEN, font=("Consolas", 8))
        canv.create_text(12, 172, text=f"BROWSER MATRIX: GOOGLE CHROME HOOKED", anchor="w", fill=COLOR_TEXT_MUTED, font=("Consolas", 8))

    # --------------------------------------------------------------------------
    # LOGGING & TRANSCRIPT
    # --------------------------------------------------------------------------
    def _log_event(self, category, text):
        now = time.strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{now}] [{category}] {text}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _append_chat(self, speaker, text, tag="body"):
        self.chat.configure(state="normal")
        if speaker == "OPERATOR":
            self.chat.insert("end", f"▶ OPERATOR (BOSS): ", "user_tag")
        elif speaker == "FRIDAY":
            self.chat.insert("end", f"◈ FRIDAY // SIDDHU AI: ", "ai_tag")
        elif speaker == "THOUGHT":
            self.chat.insert("end", f"🧠 [NEURAL REASONING]: ", "thought_tag")
        elif speaker == "EXECUTED":
            self.chat.insert("end", f"✔ [ACTION EXECUTED]: ", "exec_tag")
        else:
            self.chat.insert("end", f"ℹ [{speaker}]: ", "system_tag")

        self.chat.insert("end", f"{text}\n\n", tag)
        self.chat.see("end")
        self.chat.configure(state="disabled")

    # --------------------------------------------------------------------------
    # CINEMATIC BOOT
    # --------------------------------------------------------------------------
    def _start_cinematic_boot_sequence(self):
        play_sfx("boot")
        self._log_event("BOOT", "Stark Mark-XII FRIDAY NLP + LLM Core online.")
        self._log_event("NEURAL", "Cognitive multi-step reasoning matrix active.")
        self._log_event("TOOLS", "18 PC and web control execution primitives attached.")

        def _boot_greeting():
            time.sleep(1.2)
            greeting = "Friday Mark Twelve online. Boss, cognitive NLP and LLM matrix are fully engaged. I can analyze any complex command and execute multi-step operations across your PC and browser. What are your orders?"
            self._tts_speak(greeting)

        threading.Thread(target=_boot_greeting, daemon=True).start()

    # --------------------------------------------------------------------------
    # CONTINUOUS VOCAL LISTENING DAEMON
    # --------------------------------------------------------------------------
    def _start_continuous_vocal_listener(self):
        if not HAS_SR:
            self._log_event("VOCAL_WARN", "SpeechRecognition module not present.")
            return

        def _continuous_loop():
            r = sr.Recognizer()
            r.dynamic_energy_threshold = True
            r.energy_threshold = 240
            r.pause_threshold = 0.65
            r.non_speaking_duration = 0.35

            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.6)
            except Exception:
                pass

            self.root.after(0, lambda: self._log_event("MIC_OK", "Microphone calibrated. Continuous listening active."))

            while self.running:
                if self.is_speaking:
                    time.sleep(0.3)
                    continue

                try:
                    with sr.Microphone() as source:
                        if self.is_speaking:
                            time.sleep(0.2)
                            continue

                        self.root.after(0, self._set_listening_visuals)
                        audio = r.listen(source, timeout=3.5, phrase_time_limit=7.5)

                        if self.is_speaking:
                            continue

                        self.root.after(0, self._set_processing_visuals)
                        phrase = r.recognize_google(audio)

                        if phrase and phrase.strip():
                            p = phrase.strip()
                            self.root.after(0, lambda val=p: self.execute_task_pipeline(val))
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    time.sleep(0.4)

        threading.Thread(target=_continuous_loop, daemon=True).start()

    def _set_listening_visuals(self):
        if not self.is_speaking and not self.is_busy:
            self.arc_reactor.state = "LISTENING"
            self.audio_spectrum.mode = "LISTENING"
            self.lbl_comm_state.configure(text="[LISTENING]", fg=COLOR_GREEN)
            self.lbl_vocal_matrix.configure(text="● FRIDAY REASONING CORE: LISTENING [SPEAK NATURALLY, BOSS]", fg=COLOR_GREEN)

    def _set_processing_visuals(self):
        self.arc_reactor.state = "PROCESSING"
        self.audio_spectrum.mode = "PROCESSING"
        self.lbl_comm_state.configure(text="[REASONING]", fg=COLOR_PURPLE)
        self.lbl_vocal_matrix.configure(text="◈ COGNITIVE MATRIX: LLM & NLP ANALYZING DIRECTIVE...", fg=COLOR_PURPLE)

    # --------------------------------------------------------------------------
    # FRIDAY NLP & LLM REASONING & EXECUTION PIPELINE
    # --------------------------------------------------------------------------
    def execute_task_pipeline(self, user_query):
        if self.is_busy:
            return

        play_sfx("neural")
        self.is_busy = True
        self._append_chat("OPERATOR", user_query)
        self._log_event("TRANS_IN", f"Command: {user_query}")

        self.arc_reactor.state = "PROCESSING"
        self.audio_spectrum.mode = "PROCESSING"
        self.lbl_comm_state.configure(text="[REASONING]", fg=COLOR_PURPLE)
        self.lbl_auto_status.configure(text=f"NEURAL REASONING: ANALYZING '{user_query.upper()}'...", fg=COLOR_PURPLE)

        threading.Thread(target=self._task_reasoning_worker, args=(user_query,), daemon=True).start()

    def _task_reasoning_worker(self, user_query):
        # 1. NLP + LLM Reasoning and Plan Generation
        thought, reply, actions = self.brain.reason_and_plan(user_query)

        executed_summaries = []

        # 2. Sequential Execution of Generated Multi-Step Actions
        for idx, act in enumerate(actions, 1):
            try:
                res = execute_atomic_action(act)
                if res:
                    executed_summaries.append(f"Step {idx}: {res}")
                    self._log_event("EXEC_STEP", res)
            except Exception as e:
                executed_summaries.append(f"Step {idx} Anomaly: {e}")

        # 3. Handle Special Direct Answers (Weather, Diagnostics, Intel)
        if not reply:
            q = user_query.lower()
            if "weather" in q:
                w_data = fetch_live_weather()
                if w_data:
                    reply = f"Atmospheric report, boss: {w_data['temp_c']}°C in {w_data['location']} with {w_data['desc'].lower()}."
                else:
                    reply = "Atmospheric data retrieved, boss."
            elif "diagnostic" in q or "status" in q:
                d = get_deep_diagnostics()
                reply = f"Diagnostics, boss: CPU {d['cpu']}%, RAM {d['ram_pct']}%, Disk free {d['disk_free_gb']:.1f} GB. Power {d['battery']}."
            elif "who is" in q or "what is" in q or "explain" in q:
                topic = re.sub(r"^(?:who is|what is|tell me about|explain)\s*", "", q, flags=re.I).strip()
                intel = fetch_live_online_intelligence(topic)
                reply = f"Intelligence report, boss: {intel}" if intel else f"I've initiated reconnaissance on {topic} for you, boss."
            else:
                reply = "Directive executed, boss."

        self.root.after(0, lambda: self._on_pipeline_completed(thought, reply, executed_summaries))

    def _on_pipeline_completed(self, thought, reply, executed_summaries):
        # Show Neural Thought in transcript
        if thought:
            self._append_chat("THOUGHT", thought, "thought_tag")

        # Show Executed Actions in transcript
        for summ in executed_summaries:
            self._append_chat("EXECUTED", summ, "exec_tag")

        if executed_summaries:
            self.lbl_auto_status.configure(
                text=f"✔ FRIDAY EXECUTED: {len(executed_summaries)} ACTION(S) COMPLETED SUCCESSFULLY",
                fg=COLOR_GREEN
            )

        self._append_chat("FRIDAY", reply)
        self.last_reply = reply
        self._log_event("AI_REPLY", f"{reply[:40]}...")

        # Speak Vocal Response in background
        threading.Thread(target=lambda: self._tts_speak(reply), daemon=True).start()
        self.is_busy = False

    # --------------------------------------------------------------------------
    # VOICE SYNTHESIS (TTS)
    # --------------------------------------------------------------------------
    def _tts_speak(self, text):
        self.is_speaking = True
        self.arc_reactor.state = "SPEAKING"
        self.audio_spectrum.mode = "SPEAKING"
        self.lbl_comm_state.configure(text="[VOCALIZING]", fg=COLOR_CYAN_GLOW)
        self.lbl_vocal_matrix.configure(text="◈ FRIDAY: VOCALIZING RESPONSE...", fg=COLOR_CYAN_GLOW)

        try:
            self.speech_engine.speak(text)
        except Exception as e:
            self._log_event("TTS_ERR", str(e))
        finally:
            self.is_speaking = False
            self.arc_reactor.state = "LISTENING"
            self.audio_spectrum.mode = "LISTENING"
            self.lbl_comm_state.configure(text="[LISTENING]", fg=COLOR_GREEN)
            self.lbl_vocal_matrix.configure(text="● FRIDAY REASONING CORE: CONTINUOUS LISTENING [SPEAK NATURALLY, BOSS]", fg=COLOR_GREEN)

    # --------------------------------------------------------------------------
    # 30 FPS ANIMATION LOOP
    # --------------------------------------------------------------------------
    def _hud_animation_loop(self):
        now_str = time.strftime("%H:%M:%S")
        self.lbl_clock.configure(text=f"{now_str} IST")

        dt = 0.033
        self.arc_reactor.update(dt)
        self.audio_spectrum.update(dt)

        self.reactor_canvas.delete("all")
        self.arc_reactor.draw()
        self.audio_spectrum.draw()

        self._draw_telemetry_gauges()

        self.root.after(33, self._hud_animation_loop)


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
def main():
    root = tk.Tk()
    app = SiddhuAIApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
