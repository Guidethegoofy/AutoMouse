import threading
import time
import customtkinter as ctk
from tkinter import messagebox
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import keyboard


# ── Appearance Setup ──
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ── Constants ──
MIN_INTERVAL_MS = 1
MAX_INTERVAL_MS = 60000

# ── Global State ──
mouse_ctrl = MouseController()
kb_ctrl = KeyboardController()
running = False
click_thread = None
key_thread = None
stop_event = threading.Event()
current_hotkey = "f6"

# ── Default Keys ──
DEFAULT_KEYS = [
    {"label": "E", "key": "e"},
    {"label": "R", "key": "r"},
    {"label": "F", "key": "f"},
    {"label": "Q", "key": "q"},
    {"label": "Space", "key": Key.space},
    {"label": "Shift", "key": Key.shift},
]

# ── Special Key Map ──
SPECIAL_KEY_MAP = {
    "space": Key.space,
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "tab": Key.tab,
    "enter": Key.enter,
    "esc": Key.esc,
    "backspace": Key.backspace,
    "capslock": Key.caps_lock,
    "delete": Key.delete,
    "insert": Key.insert,
    "home": Key.home,
    "end": Key.end,
    "pageup": Key.page_up,
    "pagedown": Key.page_down,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
}


# ── Core Click Loop ──
def click_loop(interval_ms, mode_hold, button_type, stop_evt):
    """Execute mouse clicks in a background thread."""
    interval = interval_ms / 1000.0
    btn = Button.left
    if button_type == "Right":
        btn = Button.right
    elif button_type == "Middle":
        btn = Button.middle

    try:
        if mode_hold:
            mouse_ctrl.press(btn)
            stop_evt.wait()
            mouse_ctrl.release(btn)
        else:
            while not stop_evt.is_set():
                mouse_ctrl.click(btn)
                stop_evt.wait(interval)
    except Exception:
        pass  # Silently handle if controller fails on shutdown


# ── Core Key Press Loop ──
def key_press_loop(enabled_keys, interval_ms, stop_evt):
    """Repeatedly press all enabled keys at the given interval."""
    interval = interval_ms / 1000.0
    try:
        while not stop_evt.is_set():
            for key in enabled_keys:
                if stop_evt.is_set():
                    break
                kb_ctrl.press(key)
                kb_ctrl.release(key)
            stop_evt.wait(interval)
    except Exception:
        pass  # Silently handle if controller fails on shutdown


# ── App GUI ──
class AutoMouseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AutoMouse Pro")
        self.geometry("680x560")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        # Track key entries
        self.key_entries = []

        # ── Header ──
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(18, 0))

        self.title_label = ctk.CTkLabel(
            header, text="🖱 AutoMouse Pro",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(side="left")

        self.status_label = ctk.CTkLabel(
            header, text="○ Stopped",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ef5350"
        )
        self.status_label.pack(side="right")

        ctk.CTkLabel(
            header, text="Status:",
            font=ctk.CTkFont(size=14), text_color="gray"
        ).pack(side="right", padx=(0, 8))

        # ── Body — Two-Column Layout ──
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=(12, 0))
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        # ── Left Panel — Mouse & Settings ──
        left_card = ctk.CTkFrame(body, corner_radius=12)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        ctk.CTkLabel(
            left_card, text="🖱  Mouse Settings",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=16, pady=(14, 4), anchor="w")

        sep_l = ctk.CTkFrame(left_card, height=2, fg_color="gray30")
        sep_l.pack(fill="x", padx=16, pady=(0, 10))

        # Interval
        row_interval = ctk.CTkFrame(left_card, fg_color="transparent")
        row_interval.pack(fill="x", padx=16, pady=5)
        ctk.CTkLabel(row_interval, text="Interval (ms):", font=ctk.CTkFont(size=13)).pack(side="left")
        self.interval_var = ctk.StringVar(value="100")
        self.interval_entry = ctk.CTkEntry(row_interval, textvariable=self.interval_var, width=72, justify="center")
        self.interval_entry.pack(side="right")

        # Mouse Button
        row_btn = ctk.CTkFrame(left_card, fg_color="transparent")
        row_btn.pack(fill="x", padx=16, pady=5)
        ctk.CTkLabel(row_btn, text="Button:", font=ctk.CTkFont(size=13)).pack(side="left")
        self.button_var = ctk.StringVar(value="Left")
        self.btn_dropdown = ctk.CTkOptionMenu(row_btn, values=["Left", "Right", "Middle"], variable=self.button_var, width=90)
        self.btn_dropdown.pack(side="right")

        # Activation Key
        row_hotkey = ctk.CTkFrame(left_card, fg_color="transparent")
        row_hotkey.pack(fill="x", padx=16, pady=5)
        ctk.CTkLabel(row_hotkey, text="Activation Key:", font=ctk.CTkFont(size=13)).pack(side="left")
        self.hotkey_var = ctk.StringVar(value="F6")
        self.hotkey_dropdown = ctk.CTkOptionMenu(
            row_hotkey, values=["F6", "F7", "F8", "F9", "X", "Z"],
            variable=self.hotkey_var, width=90, command=self.update_hotkey
        )
        self.hotkey_dropdown.pack(side="right")

        # Hold Mode
        row_hold = ctk.CTkFrame(left_card, fg_color="transparent")
        row_hold.pack(fill="x", padx=16, pady=5)
        ctk.CTkLabel(row_hold, text="Hold Mode:", font=ctk.CTkFont(size=13)).pack(side="left")
        self.hold_var = ctk.BooleanVar(value=False)
        self.hold_switch = ctk.CTkSwitch(row_hold, text="", variable=self.hold_var)
        self.hold_switch.pack(side="right")

        # Always on Top
        row_top = ctk.CTkFrame(left_card, fg_color="transparent")
        row_top.pack(fill="x", padx=16, pady=(5, 14))
        ctk.CTkLabel(row_top, text="Always on Top:", font=ctk.CTkFont(size=13)).pack(side="left")
        self.topmost_var = ctk.BooleanVar(value=True)
        self.topmost_switch = ctk.CTkSwitch(row_top, text="", variable=self.topmost_var, command=self.toggle_topmost)
        self.topmost_switch.pack(side="right")

        # ── Right Panel — Auto Key Press ──
        right_card = ctk.CTkFrame(body, corner_radius=12)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=0)

        ctk.CTkLabel(
            right_card, text="⌨  Auto Key Press",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=16, pady=(14, 4), anchor="w")

        sep_r = ctk.CTkFrame(right_card, height=2, fg_color="gray30")
        sep_r.pack(fill="x", padx=16, pady=(0, 8))

        # Scrollable key list
        self.key_scroll = ctk.CTkScrollableFrame(right_card, corner_radius=8)
        self.key_scroll.pack(fill="both", expand=True, padx=16, pady=(0, 6))

        # Populate default keys
        for kdef in DEFAULT_KEYS:
            self._add_key_row(kdef["label"], kdef["key"], is_custom=False)

        # Custom key input row
        custom_row = ctk.CTkFrame(right_card, fg_color="transparent")
        custom_row.pack(fill="x", padx=16, pady=(0, 14))

        self.custom_key_var = ctk.StringVar(value="")
        self.custom_key_entry = ctk.CTkEntry(
            custom_row, textvariable=self.custom_key_var,
            width=120, placeholder_text="Key..."
        )
        self.custom_key_entry.pack(side="left")

        self.add_key_btn = ctk.CTkButton(
            custom_row, text="+ Add", width=60, height=28,
            command=self.add_custom_key
        )
        self.add_key_btn.pack(side="left", padx=(8, 0))

        # ── Info Panel ──
        info_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=8)
        info_frame.pack(fill="x", padx=24, pady=(5, 5))

        info_text = (
            "💡 How to Use AutoMouse Pro:\n"
            "1. Set Interval (Min: 1 ms | Max: 60,000 ms), Mouse Button, and Activation Key.\n"
            "2. Enable any Auto Keys on the right, or add your own custom keys.\n"
            "3. Press your Activation Key (e.g., F6) or click Start below to begin automation."
        )
        info_label = ctk.CTkLabel(
            info_frame, text=info_text,
            font=ctk.CTkFont(size=12), text_color="#d1d1d1", justify="left"
        )
        info_label.pack(padx=16, pady=10, anchor="w")

        # ── Bottom — Start/Stop Button ──
        self.toggle_btn = ctk.CTkButton(
            self, text="▶  Start  (F6)",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=46, corner_radius=10, command=self.toggle
        )
        self.toggle_btn.pack(padx=24, pady=(10, 18), fill="x")

        # ── Global Hotkey Listener ──
        keyboard.add_hotkey(current_hotkey, self._on_hotkey, suppress=True)

        # ── Clean shutdown ──
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Key Row Management ──
    def _add_key_row(self, label, key_value, is_custom=False):
        """Add a single key entry row to the scrollable list."""
        row = ctk.CTkFrame(self.key_scroll, fg_color="transparent")
        row.pack(fill="x", pady=2)

        enabled_var = ctk.BooleanVar(value=False)

        key_label = ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=13), width=60, anchor="w")
        key_label.pack(side="left", padx=(4, 0))

        switch = ctk.CTkSwitch(
            row, text="", variable=enabled_var, width=40,
            command=lambda lbl=label, var=enabled_var: self._on_key_toggle(lbl, var)
        )
        switch.pack(side="right", padx=(0, 4))

        entry_data = {
            "label": label,
            "key": key_value,
            "enabled": enabled_var,
            "is_custom": is_custom,
            "row_frame": row,
        }

        if is_custom:
            remove_btn = ctk.CTkButton(
                row, text="✕", width=26, height=26,
                fg_color="#ef5350", hover_color="#c62828",
                command=lambda e=entry_data: self._remove_key_row(e)
            )
            remove_btn.pack(side="right", padx=(0, 4))

        self.key_entries.append(entry_data)

    def _remove_key_row(self, entry_data):
        """Remove a custom key row from the list."""
        if running:
            messagebox.showwarning("Warning", "Stop automation before removing keys.")
            return
        entry_data["row_frame"].destroy()
        if entry_data in self.key_entries:
            self.key_entries.remove(entry_data)

    def _on_key_toggle(self, label, enabled_var):
        """Guard: prevent enabling a key that conflicts with the activation hotkey."""
        if enabled_var.get() and label.lower() == current_hotkey.lower():
            messagebox.showwarning(
                "Conflict",
                f'"{label}" is currently set as the Activation Key.\n'
                f"Change the Activation Key first, or choose a different key."
            )
            enabled_var.set(False)

    @staticmethod
    def _resolve_key(key_str):
        """Resolve a string key label to a pynput key value."""
        lower = key_str.strip().lower()
        if lower in SPECIAL_KEY_MAP:
            return SPECIAL_KEY_MAP[lower]
        # Single character key
        if len(key_str.strip()) == 1:
            return key_str.strip().lower()
        return None

    def add_custom_key(self):
        """Add a user-defined custom key to the list."""
        raw = self.custom_key_var.get().strip()
        if not raw:
            return

        key_value = self._resolve_key(raw)
        if key_value is None:
            messagebox.showerror(
                "Invalid Key",
                f'"{raw}" is not a recognized key.\n\n'
                f'Use a single character (e.g. "W") or a special name:\n'
                f"Space, Shift, Ctrl, Alt, Tab, Enter, Esc, etc."
            )
            return

        display_label = raw.capitalize()
        for entry in self.key_entries:
            if entry["label"].lower() == display_label.lower():
                messagebox.showwarning("Duplicate", f'"{display_label}" is already in the list.')
                return

        self._add_key_row(display_label, key_value, is_custom=True)
        self.custom_key_var.set("")

    # ── Hotkey & Toggle ──
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

        # Auto-disable any key toggles that now conflict
        for entry in self.key_entries:
            if entry["label"].lower() == current_hotkey.lower() and entry["enabled"].get():
                entry["enabled"].set(False)
                messagebox.showinfo(
                    "Auto-disabled",
                    f'Key "{entry["label"]}" was disabled because it conflicts with the new Activation Key.'
                )

    def toggle(self):
        global running, click_thread, key_thread, stop_event

        if not running:
            # Validate interval
            try:
                interval_ms = float(self.interval_var.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid interval value. Enter a number.")
                return

            if interval_ms < MIN_INTERVAL_MS:
                messagebox.showerror("Error", f"Interval must be at least {MIN_INTERVAL_MS} ms.")
                return
            if interval_ms > MAX_INTERVAL_MS:
                messagebox.showerror("Error", f"Interval must not exceed {MAX_INTERVAL_MS} ms.")
                return

            running = True
            stop_event = threading.Event()

            mode_hold = self.hold_var.get()
            button_type = self.button_var.get()

            # Start mouse click thread
            click_thread = threading.Thread(
                target=click_loop,
                args=(interval_ms, mode_hold, button_type, stop_event),
                daemon=True
            )
            click_thread.start()

            # Collect enabled keys and start key press thread
            enabled_keys = [e["key"] for e in self.key_entries if e["enabled"].get()]
            if enabled_keys:
                key_thread = threading.Thread(
                    target=key_press_loop,
                    args=(enabled_keys, interval_ms, stop_event),
                    daemon=True
                )
                key_thread.start()

            self.status_label.configure(text="● RUNNING", text_color="#00e676")
            self.toggle_btn.configure(
                text=f"⏹  Stop  ({self.hotkey_var.get()})",
                fg_color="#ef5350", hover_color="#c62828"
            )
        else:
            running = False
            stop_event.set()

            self.status_label.configure(text="○ Stopped", text_color="#ef5350")
            self.toggle_btn.configure(
                text=f"▶  Start  ({self.hotkey_var.get()})",
                fg_color=["#3a7ebf", "#1f538d"],
                hover_color=["#325882", "#14375e"]
            )

    def _on_close(self):
        """Clean shutdown: stop threads and unhook hotkeys before exit."""
        global running, stop_event
        if running:
            running = False
            stop_event.set()
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        self.destroy()


if __name__ == "__main__":
    app = AutoMouseApp()
    app.mainloop()
