import os
from PIL import Image

png_path = "AI_Lol.png"
ico_path = "AI_Lol.ico"

if os.path.exists(png_path):
    # Open image and convert to RGBA to ensure transparency support
    img = Image.open(png_path).convert("RGBA")
    
    # Auto-crop transparent borders so the icon looks bigger and clearer
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    
    # Generate multiple sizes for the ICO file to ensure clarity on all taskbar/UI scales
    # Windows uses different sizes for different views (16x16 for small taskbar, 256x256 for large icons)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    img.save(ico_path, format="ICO", sizes=icon_sizes)
    print(f"Successfully converted {png_path} to {ico_path} with multi-size support and auto-cropping.")
else:
    print(f"Error: {png_path} not found.")
