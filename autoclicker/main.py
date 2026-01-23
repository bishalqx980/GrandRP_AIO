import customtkinter as ctk
from clicker import AutoClicker
from selector import PositionSelector
import keyboard
import threading
import json
import os
import sys

def resource_path(filename):
    if getattr(sys, 'frozen', False):
        # Running as EXE
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as .py
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

SETTINGS_FILE = resource_path("settings.json")

# Load settings safely
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {}  # empty default

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Auto Clicker by @bishalqx980")
app.geometry("420x470")
app.resizable(False, False)

clicker = AutoClicker()

# ---------------- Settings ----------------
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_settings():
    data = {
        "x": clicker.position[0] if clicker.position else None,
        "y": clicker.position[1] if clicker.position else None,
        "delay": delay_slider.get(),
        "follow": follow_var.get()
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)


settings = load_settings()

# ---------------- Functions ----------------
def select_position():
    selector = PositionSelector(app)
    pos = selector.start()

    if pos:
        clicker.set_position(pos)
        x_label.configure(text=f"X: {pos[0]}")
        y_label.configure(text=f"Y: {pos[1]}")
        follow_var.set(0)
        save_settings()


def start_click():
    clicker.start()
    status_label.configure(text="Status: Running")


def stop_click():
    clicker.stop()
    status_label.configure(text="Status: Stopped")


def toggle_click():
    if clicker.running:
        stop_click()
    else:
        start_click()


def delay_changed(value):
    clicker.set_delay(value / 1000)
    delay_label.configure(text=f"Delay: {int(value)} ms")
    save_settings()


def follow_changed():
    clicker.set_follow_mouse(bool(follow_var.get()))
    save_settings()


# ---------------- UI ----------------
title = ctk.CTkLabel(app, text="Auto Clicker", font=("Arial", 24, "bold"))
title.pack(pady=15)

select_btn = ctk.CTkButton(app, text="Select Fixed Position", command=select_position)
select_btn.pack(pady=8)

pos_frame = ctk.CTkFrame(app)
pos_frame.pack(pady=5)

x_label = ctk.CTkLabel(pos_frame, text="X: --", width=150)
x_label.pack(side="left", padx=10)

y_label = ctk.CTkLabel(pos_frame, text="Y: --", width=150)
y_label.pack(side="right", padx=10)

# Follow mouse option
follow_var = ctk.IntVar()
follow_check = ctk.CTkCheckBox(
    app,
    text="Follow Mouse (No Fixed Position)",
    variable=follow_var,
    command=follow_changed
)
follow_check.pack(pady=8)

# Delay
delay_label = ctk.CTkLabel(app, text="Delay: 500 ms")
delay_label.pack(pady=5)

delay_slider = ctk.CTkSlider(app, from_=10, to=2000, command=delay_changed)
delay_slider.pack(pady=5)

delay_slider.set(500)

start_btn = ctk.CTkButton(app, text="Start", command=start_click)
start_btn.pack(pady=8)

stop_btn = ctk.CTkButton(app, text="Stop", command=stop_click)
stop_btn.pack(pady=8)

status_label = ctk.CTkLabel(app, text="Status: Stopped")
status_label.pack(pady=10)

info = ctk.CTkLabel(app, text="F8 = Toggle Auto Click", font=("Arial", 12))
info.pack(pady=5)

footer = ctk.CTkLabel(
    app,
    text="Developed by @bishalqx980",
    font=ctk.CTkFont(size=12),
    text_color=("gray40", "gray60")
)
footer.pack(pady=(0, 0))

# ---------------- Load Saved Settings ----------------
if settings:
    if settings.get("x") is not None:
        pos = (settings["x"], settings["y"])
        clicker.set_position(pos)
        x_label.configure(text=f"X: {pos[0]}")
        y_label.configure(text=f"Y: {pos[1]}")

    if settings.get("delay"):
        delay_slider.set(settings["delay"])
        delay_changed(settings["delay"])

    if settings.get("follow"):
        follow_var.set(1)
        clicker.set_follow_mouse(True)


# ---------------- Hotkey ----------------
def hotkey_thread():
    keyboard.add_hotkey("f8", toggle_click)
    keyboard.wait()

threading.Thread(target=hotkey_thread, daemon=True).start()

app.mainloop()
