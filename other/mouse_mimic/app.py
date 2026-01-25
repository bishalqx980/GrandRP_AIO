import os
import sys
import json
import threading
import customtkinter as ctk
import pydirectinput as pdi
from pynput import mouse

def get_app_dir():
    # Running as PyInstaller EXE
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # Running as normal Python script
    return os.path.dirname(os.path.abspath(__file__))


# ---------------- CONFIG LOAD ----------------
APP_DIR = get_app_dir()
CONFIG_PATH = os.path.join(APP_DIR, "config.json")

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError("config.json not found next to the executable")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

MOUSE_BUTTON = CONFIG["mouse_button"].lower()
KEY_TO_PRESS = CONFIG["key_to_press"].lower()

BUTTON_MAP = {
    "left": mouse.Button.left,
    "right": mouse.Button.right,
    "middle": mouse.Button.middle
}

TARGET_BUTTON = BUTTON_MAP.get(MOUSE_BUTTON)

# ---------------- APP STATE ----------------
listener = None
enabled = False

# ---------------- MOUSE HANDLER ----------------
def on_click(x, y, button, pressed):
    if not enabled:
        return

    if button == TARGET_BUTTON and pressed:
        pdi.PAUSE = 0
        pdi.press(KEY_TO_PRESS)

# ---------------- TOGGLE LOGIC ----------------
def start_listener():
    global listener
    listener = mouse.Listener(on_click=on_click)
    listener.start()

def stop_listener():
    global listener
    if listener:
        listener.stop()
        listener = None

def toggle():
    global enabled
    enabled = toggle_var.get()

    if enabled:
        status_label.configure(text="Status: ON", text_color="green")
        start_listener()
    else:
        status_label.configure(text="Status: OFF", text_color="red")
        stop_listener()

# ---------------- UI ----------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Mouse → Key Toggle by @bishalqx980")
app.geometry("300x180")
app.resizable(False, False)

title = ctk.CTkLabel(
    app,
    text=f"{MOUSE_BUTTON.upper()} → {KEY_TO_PRESS.upper()}",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

toggle_var = ctk.BooleanVar(value=False)

toggle_btn = ctk.CTkSwitch(
    app,
    text="Enable",
    variable=toggle_var,
    command=toggle
)
toggle_btn.pack(pady=10)

status_label = ctk.CTkLabel(
    app,
    text="Status: OFF",
    text_color="red"
)
status_label.pack(pady=10)

footer = ctk.CTkLabel(
    app,
    text="Developed by @bishalqx980",
    font=ctk.CTkFont(size=12),
    text_color=("gray40", "gray60")
)
footer.pack(pady=(0, 0))

app.mainloop()
