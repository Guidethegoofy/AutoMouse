@echo off
echo Building AutoMouse Executable...
pyinstaller --noconfirm --onefile --windowed --name "AutoMouse" --add-data "AutoMouse.py;." AutoMouse.py
echo Build complete! Check the 'dist' folder.
pause
