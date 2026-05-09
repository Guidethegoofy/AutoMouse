@echo off
echo Building AutoMouse Executable...
pyinstaller --noconfirm --onedir --windowed --icon="AI_Lol.png" --name "AutoMouse" --add-data "AutoMouse.py;." --add-data "AI_Lol.png;." AutoMouse.py
echo Build complete! Check the 'dist' folder.
pause
