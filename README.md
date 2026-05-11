<div align="center">
  <h1>🖱️ AutoMouse Pro</h1>
  <p><em>A modern, high-performance mouse & keyboard automation utility built with Python.</em></p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![GUI](https://img.shields.io/badge/GUI-CustomTkinter-success.svg)](https://customtkinter.tomschimansky.com/)
  [![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com/Guidethegoofy/AutoMouse/releases/latest)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Guidethegoofy/AutoMouse/blob/main/LICENSE)
</div>

<hr>

## 📌 Overview

**AutoMouse Pro** is a robust GUI application engineered for precision mouse and keyboard automation. Built with a focus on usability, minimal latency, and clean execution, it provides advanced control over click intervals, button mappings, keyboard key presses, and operation modes — all from a compact horizontal two-panel layout.

The application leverages multi-threading to ensure the UI remains fully responsive while executing intensive automation loops in the background.

## ✨ Key Features

- **Horizontal Two-Panel Layout**: Mouse settings on the left, keyboard key toggles on the right — everything visible at a glance without scrolling.
- **Asynchronous Execution**: Isolated background threads for mouse clicks and key presses prevent interface freezing.
- **Modern Dark UI**: A sleek, distraction-free interface built with `customtkinter`.
- **Always on Top Window**: Toggleable floating mode to keep the app above other windows.
- **Global Hotkeys**: Background toggling support with configurable activation keys (F6–F9, X, Z).
- **Customizable Mouse Operations**:
  - Configurable click intervals (10 ms – 60,000 ms) with bounds validation.
  - Multi-button support (Left, Right, Middle).
- **Auto Key Press**:
  - 6 default keys (E, R, F, Q, Space, Shift) with individual on/off toggles.
  - Add custom keys manually — single characters or special key names (Ctrl, Alt, Tab, Enter, Esc, etc.).
  - Remove custom keys with a single click.
  - Built-in conflict guard prevents enabling a key that matches the activation hotkey.
- **Dual Operating Modes**:
  - *Rapid Fire*: Interval-based repetitive clicking.
  - *Hold Mode*: Continuous button depression until released.
- **Safe Shutdown**: Graceful cleanup on window close — stops all threads and unhooks global hotkeys.

## 🏗️ Architecture & Tech Stack

| Component | Technology |
|---|---|
| Core Logic | Python 3.8+ |
| User Interface | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Mouse Simulation | `pynput.mouse` |
| Keyboard Simulation | `pynput.keyboard` |
| Global Hotkey Hooking | `keyboard` |
| Concurrency | Native Python `threading` |
| Build System | PyInstaller (via `build.bat`) |

## 🔐 Safety & Stability

The application includes several safety measures:

- **Interval bounds validation**: Prevents values below 10 ms (CPU protection) or above 60,000 ms.
- **Exception-safe background loops**: `try/except` guards around all input simulation to prevent crashes on shutdown.
- **Responsive stop mechanism**: Uses `stop_event.wait(interval)` instead of `time.sleep()` so threads halt immediately when stopped.
- **Clean shutdown handler**: The `WM_DELETE_WINDOW` protocol handler ensures all threads are stopped and all keyboard hooks are removed before the process exits.
- **Hotkey conflict guard**: Prevents enabling an auto-press key that matches the current activation hotkey, avoiding infinite loops.
- **Duplicate key prevention**: Cannot add the same key twice to the auto-press list.

## 📥 Download & Install (For Regular Users)

If you just want to use the application without dealing with Python code, you can download the ready-to-run `.exe` file.

1. Go to the [Latest Release Page](https://github.com/Guidethegoofy/AutoMouse/releases/latest).
2. Download **`AutoMouse.exe`** under the "Assets" section.
3. Double-click the file to run it. No installation or Python required!

---

## 🚀 For Developers (Running from Source)

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Guidethegoofy/AutoMouse.git
   cd AutoMouse
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running from Source

Execute the main script directly:
```bash
python AutoMouse.py
```

## 📦 Building the Executable

For deployment or distribution without requiring a Python environment, you can compile AutoMouse Pro into a standalone Windows executable.

1. Ensure all dependencies are installed.
2. Run the provided build script:
   ```cmd
   .\build.bat
   ```
3. Locate the compiled executable in the newly generated `dist/` directory.

## 🕹️ Usage Guide

1. **Launch** the application (via script or executable).
2. **Left Panel — Mouse Settings**:
   - Set the click **Interval (ms)** (range: 10–60,000).
   - Select the target **Mouse Button** (Left, Right, or Middle).
   - Choose your **Activation Key** (F6–F9, X, or Z).
   - Toggle **Hold Mode** for continuous button press instead of repeated clicks.
   - Toggle **Always on Top** to keep the window floating.
3. **Right Panel — Auto Key Press**:
   - Toggle any default key (E, R, F, Q, Space, Shift) on/off with the switch.
   - Type a key name in the input field and click **+ Add** to add a custom key.
   - Remove custom keys with the **✕** button.
   - Conflicting keys (matching the Activation Key) are automatically blocked.
4. **Start**: Press the Activation Key globally, or click **▶ Start**. Mouse clicks and enabled key presses run simultaneously.
5. **Stop**: Press the Activation Key again, or click **⏹ Stop** to halt all automation instantly.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Guidethegoofy/AutoMouse/issues) if you want to contribute.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Crafted with precision for developers, testers, and power users.*