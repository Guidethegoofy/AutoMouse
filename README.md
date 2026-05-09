<div align="center">
  <h1>🖱️ AutoMouse Pro</h1>
  <p><em>A modern, high-performance automation utility built with Python.</em></p>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![GUI](https://img.shields.io/badge/GUI-CustomTkinter-success.svg)](https://customtkinter.tomschimansky.com/)
  [![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com/Guidethegoofy/AutoMouse/releases/tag/v1.0.0)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Guidethegoofy/AutoMouse/blob/main/LICENSE)
</div>

<hr>

## 📌 Overview

**AutoMouse Pro** is a robust, cross-platform-ready GUI application engineered for precision mouse automation. Built with a focus on usability, minimal latency, and zero-interference execution, it provides advanced control over click intervals, button mappings, and operation modes. The application leverages multi-threading to ensure the UI remains fully responsive while executing intensive macro loops in the background.

## ✨ Key Features

- **Asynchronous Execution**: Utilizes Python's `threading` module to isolate the GUI mainloop from the heavy-duty clicking loops, preventing interface freezing.
- **Modern Dark UI**: A sleek, distraction-free interface built using `customtkinter` with intuitive visual feedback for active states.
- **Always on Top Window**: Easily toggleable mode to keep the application in focus over other windows.
- **Global Hotkeys**: Robust background toggling support (e.g., F6).
- **Customizable Operations**:
  - Configurable click intervals down to the millisecond.
  - Multi-button support (Left, Right, Middle).
  - Flexible activation key bindings (F6-F9, X, Z).
- **Dual Operating Modes**:
  - *Rapid Fire*: Interval-based repetitive clicking.
  - *Hold Mode*: Continuous button depression until released.

## 🏗️ Architecture & Tech Stack

- **Core Logic**: Python 3
- **User Interface**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Input Simulation & Hotkey Hooking**: `pynput` (Mouse) and `keyboard` (Hotkey suppression)
- **Concurrency**: Native Python `threading`
- **Build System**: PyInstaller (via `build.bat`)

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AutoMouse.git
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
2. **Configure** your parameters:
   - Enter the desired delay between clicks in the **Interval (ms)** field.
   - Select the target **Mouse Button** from the dropdown.
   - Choose your preferred **Activation Key** (e.g., F6).
3. **Toggle Mode** (Optional): 
   - Enable *Hold Mode* if you need the button to remain pressed continuously rather than clicked repeatedly.
   - Toggle *Always on Top* to keep the window floating above other applications.
4. **Start**: Press your selected Activation Key globally, or click the **Start** button in the UI. 
5. **Stop**: Press the Activation Key again, or click **Stop** to halt automation instantly.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](#) if you want to contribute.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Crafted with precision for developers, testers, and power users.*