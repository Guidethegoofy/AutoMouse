@echo off
echo Building AutoMouse Executable...
pyinstaller --noconfirm --onefile --windowed --name "AutoMouse" --collect-all customtkinter AutoMouse.py
echo Build complete! Check the 'dist' folder.
pause
