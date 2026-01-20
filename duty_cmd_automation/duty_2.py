import os
import sys
import json
import threading
from time import sleep
from datetime import datetime, timezone

import pyperclip
import pydirectinput as pdi
import customtkinter as ctk

# ---------------------- CONFIG LOAD ----------------------

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(get_app_dir(), "config.json")

DEFAULT_CONFIG = {
    "badge_number": "",
    "start_delay": 3,
    "screenshot_keys": ["alt", "`"],
    "on_duty_commands": [],
    "off_duty_commands": []
}

if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

START_DELAY = CONFIG.get("start_delay", 3)
SCREENSHOT_KEYS = CONFIG.get("screenshot_keys", ["alt", "`"])


# ---------------------- CORE LOGIC ----------------------

def execute_commands(cmd_list: list, log_cb):
    try:
        for cmd in cmd_list:
            log_cb(f"Sending command: {cmd}")
            pyperclip.copy(cmd)
            pdi.press("t")
            sleep(0.25)
            pdi.keyDown("ctrl")
            pdi.press("v")
            pdi.keyUp("ctrl")
            pdi.press("enter")
            sleep(0.5)
        return True
    except Exception as e:
        log_cb(f"Error: {e}")
        return False


def take_screenshot():
    if len(SCREENSHOT_KEYS) == 2:
        pdi.keyDown(SCREENSHOT_KEYS[0])
        pdi.press(SCREENSHOT_KEYS[1])
        pdi.keyUp(SCREENSHOT_KEYS[0])


# ---------------------- UI APP ----------------------

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DutyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FIB/LSPD/SAHP Duty Command Helper by @bishalqx980")
        self.geometry("520x420")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Badge Number").pack(pady=(10, 0))
        self.badge_entry = ctk.CTkEntry(self, width=200)
        if "badge_number" in CONFIG:
            self.badge_entry.insert(0, str(CONFIG["badge_number"]))
        self.badge_entry.pack()

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)

        self.on_btn = ctk.CTkButton(btn_frame, text="On Duty", command=self.on_duty)
        self.on_btn.pack(side="left", padx=10)

        self.off_btn = ctk.CTkButton(btn_frame, text="Off Duty", command=self.off_duty)
        self.off_btn.pack(side="left", padx=10)

        ctk.CTkLabel(self, text="Log").pack()
        self.log_box = ctk.CTkTextbox(self, width=480, height=220)
        self.log_box.pack(pady=5)
        self.log_box.configure(state="disabled")
        
        self.footer = ctk.CTkLabel(
            self,
            text="Developed by @bishalqx980",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60")
        )
        self.footer.pack(pady=(0, 0))

    # ---------------------- HELPERS ----------------------

    def log(self, text: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{text}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def get_badge(self):
        badge = self.badge_entry.get().strip()
        if not badge.isdigit():
            self.log("Invalid badge number")
            return None

        # persist badge to json
        CONFIG["badge_number"] = badge
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(CONFIG, f, indent=4)
        except Exception as e:
            self.log(f"Failed to save badge: {e}")

        return badge

    def run_duty(self, mode: str):
        badge = self.get_badge()
        if not badge:
            return

        now = datetime.now(timezone.utc).strftime("%H:%M")
        commands = []

        for cmd in CONFIG[mode]:
            commands.append(cmd.format(badge=badge, time=now))

        self.log(f"Starting in {START_DELAY} sec")
        sleep(START_DELAY)

        if execute_commands(commands, self.log):
            take_screenshot()
            self.log(f"{mode.replace('_', ' ').title()} done")

    # ---------------------- BUTTON CALLBACKS ----------------------

    def on_duty(self):
        threading.Thread(target=self.run_duty, args=("on_duty_commands",), daemon=True).start()

    def off_duty(self):
        threading.Thread(target=self.run_duty, args=("off_duty_commands",), daemon=True).start()


if __name__ == "__main__":
    app = DutyApp()
    app.mainloop()
