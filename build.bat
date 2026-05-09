@echo off
echo Generating ICO file...
python convert_icon.py
echo Building AutoMouse Executable...
pyinstaller --noconfirm --onedir --windowed --icon="AI_Lol.ico" --name "AutoMouse" --add-data "AutoMouse.py;." --add-data "AI_Lol.ico;." AutoMouse.py
echo Build complete! Check the 'dist' folder.
pause
