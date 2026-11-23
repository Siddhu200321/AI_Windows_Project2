# SIDDHU AI // STARK INDUSTRIES MARK-XII [FRIDAY COGNITIVE NLP & LLM MATRIX]

A next-generation autonomous AI desktop interface modeled after Tony Stark's **FRIDAY** from *Avengers*. Operates **100% automatically via your voice without clicking any buttons** and is powered by a **Cognitive NLP + LLM Multi-Step Reasoning Engine**.

---

## 🧠 What Makes This a True NLP + LLM Brain?

1. **Autonomous Multi-Step Intent Planning**:
   - Understands complex, multi-part natural language sentences and automatically decomposes them into sequential actions.
   - **Example**: *"Search for LinkedIn in Chrome and open the first link"*
     - **Step 1**: FRIDAY opens Google Chrome and queries Google Search for *"LinkedIn"*.
     - **Step 2**: FRIDAY waits for the page to load and clicks on the primary search result link!
     - **Result**: You are immediately taken to the LinkedIn homepage hands-free!

2. **Tri-Tier Intelligence Architecture**:
   - **Local Neural Core (Ollama)**: Seamlessly links with local LLMs (`qwen2.5:3b`, `llama3`, `mistral`) when `ollama serve` is active for private on-device reasoning.
   - **Cloud Neural LLM Fallback**: Instantaneous cloud LLM reasoning with zero setup or API keys required.
   - **Semantic NLU Action Decomposer**: 0ms-latency local natural language parser that breaks down conjunctions (`and`, `then`, `after that`), extracts entities, coordinates, numbers, and file names.

3. **18 Execution Primitives (Tools Available to the Brain)**:
   - `search_google`: Searches Google in Chrome.
   - `click_search_link`: Clicks top search results by rank (Link 1, Link 2, Link 3).
   - `open_website`: Navigates to any URL or site name (LinkedIn, YouTube, GitHub, ChatGPT...).
   - `play_youtube`: Streams any song/artist/video on YouTube in Chrome.
   - `open_app`: Launches any PC software (Notepad, VS Code, Paint, Calculator, Spotify, Settings...).
   - `close_app`: Terminates applications or closes windows.
   - `mouse_action`: Clicks, double clicks, right clicks, scrolls up/down, jumps to top/bottom, coordinates.
   - `keyboard_action`: Enter, space, tab, esc, backspace, arrows, F1-F12, hotkeys (`Ctrl+A`, `Ctrl+C`, `Ctrl+V`, `Ctrl+S`...).
   - `type_text`: Writes arbitrary text smoothly and optionally presses Enter.
   - `browser_control`: New tab, close tab, next tab, previous tab, back, forward, reload.
   - `window_action`: Maximize, minimize, show desktop, snap left, snap right.
   - `create_note`: Generates timestamped `.txt` documents on the Desktop.
   - `create_folder`: Generates new folders on the Desktop.
   - `take_screenshot`: Full-resolution display capture archived to Pictures.
   - `control_volume`: Volume up, volume down, mute audio, media play/pause.
   - `lock_pc`: Locks the Windows workstation immediately.
   - `weather_report`: Real-time atmospheric sensors readout.
   - `online_intel`: Queries DuckDuckGo and Wikipedia live for instant answers.

---

## 🎙️ Zero-Touch Voice Interaction:

- **Continuous Vocal Ear**: Always listening in real time. **No buttons to operate**. Just speak naturally into your microphone!
- **Intelligent Echo Suppression**: Automatically pauses listening while FRIDAY is speaking to prevent self-echo loops.
- **Acoustic Audio Feedback**: High-tech sci-fi chimes, boot sweeps, command blips, and neural chords via Windows `winsound`.
- **Fullscreen Theater Mode**: Hit **`F11`** at any time to toggle fullscreen command center.

---

## 🚀 How to Run:

Double-click `run_siddhu_ai.bat` in [C:\Users\siddartha\Downloads\SIDDHU_AI_Windows_Project](file:///C:/Users/siddartha/Downloads/SIDDHU_AI_Windows_Project) or run:

```powershell
cd C:\Users\siddartha\Downloads\SIDDHU_AI_Windows_Project\siddhu_ai
python app.py
```

*Try speaking complex commands naturally:*
- *"Search for LinkedIn in Chrome and open the first link"*
- *"Play AC/DC on YouTube in Chrome"*
- *"Create a folder named Projects on desktop and open VS Code"*
- *"What's the weather today and set volume to maximum"*
- *"Scroll down"*, *"New tab"*, or *"Maximize window"*!
