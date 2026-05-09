import threading
import time
import os
import sys
import tkinter as tk
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
from pynput import mouse
from pynput.mouse import Button, Controller as MouseController
import keyboard

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ── Appearance Setup ──
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ── Global State ──
mouse_ctrl = MouseController()
running = False
click_thread = None
stop_event = threading.Event()
current_hotkey = "f6"

# ── Core Click Loop ──
def click_loop(interval_ms, mode_hold, button_type, stop_evt):
    interval = interval_ms / 1000.0
    btn = Button.left
    if button_type == "Right": btn = Button.right
    elif button_type == "Middle": btn = Button.middle

    if mode_hold:
        mouse_ctrl.press(btn)
        stop_evt.wait()
        mouse_ctrl.release(btn)
    else:
        while not stop_evt.is_set():
            mouse_ctrl.click(btn)
            time.sleep(interval)

# ── App GUI ──
class AutoMouseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AutoMouse Pro")
        self.geometry("380x640")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        # Load Logo Image
        try:
            icon_path = resource_path("AI_Lol.png")
            # Set Window Icon
            img_icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(False, img_icon)
            
            # Show Logo in UI
            my_image = ctk.CTkImage(light_image=Image.open(icon_path), dark_image=Image.open(icon_path), size=(60, 60))
            self.logo_label = ctk.CTkLabel(self, text="", image=my_image)
            self.logo_label.pack(pady=(20, 0))
        except Exception as e:
            pass

        # Title
        self.title_label = ctk.CTkLabel(self, text="AutoMouse Pro", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(5, 0))

        self.subtitle_label = ctk.CTkLabel(self, text="Strategic Automation Utility", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray")
        self.subtitle_label.pack(pady=(0, 15))

        # Main Card / Panel
        self.card = ctk.CTkFrame(self, corner_radius=15)
        self.card.pack(padx=20, pady=10, fill="both", expand=True)

        # Status
        self.status_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(self.status_frame, text="Status:", font=ctk.CTkFont(size=14)).pack(side="left")
        self.status_label = ctk.CTkLabel(self.status_frame, text="○ Stopped", font=ctk.CTkFont(size=14, weight="bold"), text_color="#ef5350")
        self.status_label.pack(side="right")

        # Click Interval
        self.interval_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.interval_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(self.interval_frame, text="Interval (ms):", font=ctk.CTkFont(size=14)).pack(side="left")
        self.interval_var = ctk.StringVar(value="100")
        self.interval_entry = ctk.CTkEntry(self.interval_frame, textvariable=self.interval_var, width=80, justify="center")
        self.interval_entry.pack(side="right")

        # Mouse Button
        self.btn_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(self.btn_frame, text="Mouse Button:", font=ctk.CTkFont(size=14)).pack(side="left")
        self.button_var = ctk.StringVar(value="Left")
        self.btn_dropdown = ctk.CTkOptionMenu(self.btn_frame, values=["Left", "Right", "Middle"], variable=self.button_var, width=100)
        self.btn_dropdown.pack(side="right")

        # Activation Hotkey
        self.hotkey_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.hotkey_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(self.hotkey_frame, text="Activation Key:", font=ctk.CTkFont(size=14)).pack(side="left")
        self.hotkey_var = ctk.StringVar(value="F6")
        self.hotkey_dropdown = ctk.CTkOptionMenu(self.hotkey_frame, values=["F6", "F7", "F8", "F9", "X", "Z"], variable=self.hotkey_var, width=100, command=self.update_hotkey)
        self.hotkey_dropdown.pack(side="right")

        # Hold Mode Switch
        self.hold_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.hold_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(self.hold_frame, text="Hold Mode:", font=ctk.CTkFont(size=14)).pack(side="left")
        self.hold_var = ctk.BooleanVar(value=False)
        self.hold_switch = ctk.CTkSwitch(self.hold_frame, text="", variable=self.hold_var)
        self.hold_switch.pack(side="right")

        # Always on Top Switch
        self.topmost_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.topmost_frame.pack(fill="x", padx=20, pady=(10, 20))
        ctk.CTkLabel(self.topmost_frame, text="Always on Top:", font=ctk.CTkFont(size=14)).pack(side="left")
        self.topmost_var = ctk.BooleanVar(value=True)
        self.topmost_switch = ctk.CTkSwitch(self.topmost_frame, text="", variable=self.topmost_var, command=self.toggle_topmost)
        self.topmost_switch.pack(side="right")

        # Primary Toggle Button
        self.toggle_btn = ctk.CTkButton(self, text="▶  Start  (F6)", font=ctk.CTkFont(size=16, weight="bold"), height=50, corner_radius=10, command=self.toggle)
        self.toggle_btn.pack(padx=20, pady=(10, 20), fill="x")

        # Global Hotkey Listener
        keyboard.add_hotkey(current_hotkey, self._on_hotkey, suppress=True)

    def _on_hotkey(self):
        self.after(0, self.toggle)

    def toggle_topmost(self):
        self.attributes("-topmost", self.topmost_var.get())

    def update_hotkey(self, selection):
        global current_hotkey
        try:
            keyboard.remove_hotkey(current_hotkey)
        except Exception:
            pass
        current_hotkey = selection.lower()
        keyboard.add_hotkey(current_hotkey, self._on_hotkey, suppress=True)
        self.toggle_btn.configure(text=f"{'⏹  Stop' if running else '▶  Start'}  ({selection})")

    def toggle(self):
        global running, click_thread, stop_event

        if not running:
            try:
                interval_ms = float(self.interval_var.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid interval value")
                return

            running = True
            stop_event = threading.Event()

            mode_hold = self.hold_var.get()
            button_type = self.button_var.get()

            click_thread = threading.Thread(
                target=click_loop,
                args=(interval_ms, mode_hold, button_type, stop_event),
                daemon=True
            )
            click_thread.start()

            self.status_label.configure(text="● RUNNING", text_color="#00e676")
            self.toggle_btn.configure(text=f"⏹  Stop  ({self.hotkey_var.get()})", fg_color="#ef5350", hover_color="#c62828")
        else:
            running = False
            stop_event.set()

            self.status_label.configure(text="○ Stopped", text_color="#ef5350")
            # Default CTA colors
            self.toggle_btn.configure(text=f"▶  Start  ({self.hotkey_var.get()})", fg_color=["#3a7ebf", "#1f538d"], hover_color=["#325882", "#14375e"])

if __name__ == "__main__":
    app = AutoMouseApp()
    app.mainloop()
