# SIDDHU AI // STARK INDUSTRIES MARK-XII [FRIDAY COGNITIVE NLP & LLM MATRIX]

An autonomous Iron Man / Avengers AI desktop operating assistant inspired by Tony Stark's **FRIDAY**. Operates **100% hands-free via continuous voice recognition—no buttons to operate, no manual confirmation dialogs**. Powered by a **Cognitive NLP + LLM Multi-Step Reasoning Engine** that gives you complete control over your Windows PC, Google Chrome, web search results, mouse, and keyboard.

---

## ⚡ What Makes SIDDHU AI Unique?

1. **Autonomous Multi-Step Intent Planning**:
   - Decomposes complex human instructions into sequential actions automatically.
   - **Example**: *"Search for LinkedIn in Chrome and open the first link"*
     - **Step 1**: Launches Google Chrome & queries Google Search for *"LinkedIn"*.
     - **Step 2**: Identifies the primary search link and navigates into the LinkedIn interface hands-free!

2. **Tri-Tier Intelligence Brain**:
   - **Local Neural Core (Ollama)**: Direct integration with local models (`qwen2.5:3b`, `llama3`, `mistral`) for on-device reasoning.
   - **Cloud Neural LLM Fallback**: Instant cloud LLM reasoning with zero setup or API keys required.
   - **Local Semantic NLU Action Decomposer**: 0ms-latency local natural language parser that breaks down conjunctions (`and`, `then`, `after that`), extracts targets, coordinates, numbers, and file names.

3. **Complete Mouse & Keyboard Emulation**:
   - **Mouse**: Clicks, double clicks, right clicks, middle clicks, center click, click coordinates `(X, Y)`, smooth scrolling up/down, and jumps to top/bottom (`Home`/`End`).
   - **Keyboard**: Enter, space, tab, esc, backspace, arrows, F1-F12, hotkeys (`Ctrl+A`, `Ctrl+C`, `Ctrl+V`, `Ctrl+S`, `Ctrl+Z`...), and arbitrary text typing.

4. **Web & Operating System Dispatch**:
   - **Chrome & Web**: Stream YouTube music/videos, search Google in Chrome, and open any web platform on command.
   - **Local OS**: Launches and terminates applications (Notepad, VS Code, Paint, Spotify, Calculator, Settings), takes full-res screenshots, creates notes/folders on the desktop, and controls master volume.

5. **Holographic Stark Industries HUD**:
   - Animated vector Arc Reactor with degree orbits, rotating radar sweep beam, and audio-reactive shockwaves.
   - 40-band holographic spectrum visualizer that dances in real time to voice audio.
   - Live hardware telemetry (CPU, RAM, storage, power matrix).
   - Resilient speech synthesis with articulate FRIDAY cadence.

---

## 🚀 Quick Start & Installation

### 1. Requirements
- Windows 10 or 11 (64-bit)
- Python 3.10, 3.11, or 3.12
- Google Chrome (optional, for web browser dispatch)
- [Ollama for Windows](https://ollama.com/download/windows) (optional, for local neural reasoning)

### 2. Clone the Repository
```powershell
git clone https://github.com/<your-username>/SIDDHU_AI_Windows_Project.git
cd SIDDHU_AI_Windows_Project
```

### 3. Install Dependencies
```powershell
pip install -r siddhu_ai/requirements.txt
```

### 4. Run SIDDHU AI
Double-click `run_siddhu_ai.bat` or run:
```powershell
cd siddhu_ai
python app.py
```

*As soon as the HUD launches, simply speak naturally into your microphone!*

---

## 🎙️ Example Voice Directives to Try

| Category | Example Directives |
| :--- | :--- |
| **Search & Links** | *"Search for LinkedIn in Chrome and open the first link"*<br>*"Search for chocolate cake recipes in Chrome"* → *"Open first link"* |
| **Mouse Control** | *"Click"*, *"Double click"*, *"Right click"*, *"Click center"*, *"Scroll down"*, *"Scroll to top"* |
| **Keyboard & Typing**| *"Press Enter"*, *"Press Tab"*, *"Type user@example.com and press enter"*, *"Select all"*, *"Copy"*, *"Paste"* |
| **Browser Tabs** | *"New tab"*, *"Close tab"*, *"Next tab"*, *"Previous tab"*, *"Go back"*, *"Refresh page"* |
| **App Control** | *"Open Notepad"*, *"Open VS Code"*, *"Open Spotify"*, *"Close Chrome"* |
| **Desktop Files** | *"Create folder Projects on desktop"*, *"Write a note: check code at 5pm"* |
| **Hardware & Audio**| *"Volume up"*, *"Volume down"*, *"Mute audio"*, *"Take a screenshot"*, *"Lock PC"* |
| **Online Intel** | *"Play AC/DC on YouTube in Chrome"*, *"What's the weather today?"*, *"Who is Tony Stark?"* |

---

## 🛡️ Safety & Hardware Failsafe
- Moving the mouse cursor into the very top-left corner of the screen **`(0, 0)`** immediately triggers PyAutoGUI's hardware failsafe abort.
- Press **`F11`** at any time to toggle fullscreen cinematic theater mode.

---

## 📜 License
MIT License. Built for enthusiasts of Iron Man, JARVIS, FRIDAY, and hands-free desktop AI automation.
