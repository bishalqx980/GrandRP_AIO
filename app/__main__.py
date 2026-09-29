import json
import os
import sys
from datetime import datetime
from threading import Thread

import customtkinter as ctk

from app.logic.antiafk import AFK_MODES
from app.logic.leo import do_leo_automation
from app.logic.discord import do_discord


__version__ = "0.4 - (beta)"
afk_modes = AFK_MODES()

DEFAULT_CONFIG = {
    "badge_number": 109,
    "gmt_offset": 0,
    "department": "LSPD",
    "screenshot_combo": ["alt", "`"],
    "onduty_commands": [
        "/me takes out bodycam, turns it on, and checks for the red light",
        "/do The bodycam is recording, and is ballistic and waterproof",
        "{badge} to {department} Dispatch Show 10-41 at {time}"
    ],
    "offduty_commands": [
        "/do saves the bodycam content and uploads the bodycam to {department} servers and stops recording",
        "{badge} to {department} Dispatch Show 10-42 at {time}"
    ]
}


def resource_path(relative):
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.abspath(relative)


def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


SETTINGS_FILE = os.path.join(get_app_dir(), "config.json")


def load_config():
    if not os.path.exists(SETTINGS_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            config = json.load(file)
    except (OSError, json.JSONDecodeError):
        config = {}

    changed = False

    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
            changed = True

    if config.get("department") not in {"SAHP", "LSPD", "FIB"}:
        config["department"] = "LSPD"
        changed = True

    if changed:
        save_config(config)

    return config


def save_config(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


CONFIG = load_config()


class App(ctk.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.title("GrandRP - AIO")
        self.geometry("700x500")
        self.resizable(False, False)

        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.create_header()
        self.create_navigation()
        self.create_content()
        self.create_footer()

        self.log("App initialized...")
        self.switch_section("antiafk")

        if not CONFIG.get("discord"):
            Thread(target=self.send_discord_info, daemon=True).start()

    def create_header(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        frame.grid_columnconfigure(1, weight=1)

        self.app_status = ctk.CTkLabel(
            frame,
            text="App Status: Idle",
            text_color="orange"
        )
        self.app_status.grid(row=0, column=0, padx=10)

        ctk.CTkLabel(
            frame,
            text="GrandRP - AIO",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=1, sticky="e", padx=10)

    def create_navigation(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        buttons = {
            "antiafk": ("AntiAFK", self.load_antiafk_ui),
            "leo": ("LEO", self.load_leo_ui)
        }

        self.nav_buttons = {}

        for column, (section, (text, _)) in enumerate(buttons.items()):
            frame.grid_columnconfigure(column, weight=1)
            button = ctk.CTkButton(
                frame,
                text=text,
                font=("Segoe UI", 14, "bold"),
                command=lambda value=section: self.switch_section(value)
            )
            button.grid(row=0, column=column, sticky="ew", padx=5, pady=10)
            self.nav_buttons[section] = button

        self.normal_color = self.nav_buttons["antiafk"].cget("fg_color")
        self.active_color = "#001755"
        self.active_section = None

    def create_content(self):
        frame = ctk.CTkFrame(self)
        frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.content_box = ctk.CTkFrame(frame)
        self.content_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.log_box = ctk.CTkTextbox(frame)
        self.log_box.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.log_box.configure(state="disabled")
        self.log_box.tag_config("time", foreground="#ffcc81")
        self.log_box.tag_config("msg", foreground="#b1b1b1")
        self.log_box.tag_config("error", foreground="#ff0000")
        self.log_box.bind("<Key>", lambda _: "break")
        self.log_box.bind("<Button-1>", lambda _: "break")

    def create_footer(self):
        ctk.CTkLabel(
            self,
            text=f"Developed by @bishalqx980 | App Version: {__version__}",
            font=("Segoe UI", 12),
            text_color="gray"
        ).grid(row=4, column=0, pady=(0, 10))

    def send_discord_info(self):
        try:
            do_discord()
            CONFIG["discord"] = True
            save_config(CONFIG)
        except Exception as exc:
            self.after(0, lambda: self.log(f"Discord setup failed: {exc}", True))

    def log(self, message, error=False):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{timestamp}] ", "time")
        self.log_box.insert("end", f"- {message}\n", "error" if error else "msg")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def switch_section(self, section):
        if self.active_section == section:
            return

        self.active_section = section

        for name, button in self.nav_buttons.items():
            button.configure(
                fg_color=self.active_color if name == section else self.normal_color
            )

        for widget in self.content_box.winfo_children():
            widget.destroy()

        if section == "antiafk":
            self.load_antiafk_ui()
        elif section == "leo":
            self.load_leo_ui()

    def load_antiafk_ui(self):
        ctk.CTkLabel(
            self.content_box,
            text="AntiAFK Menu",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=10, pady=(0, 10))

        self.normal_antiafk_switch = ctk.CTkSwitch(
            self.content_box,
            text="Enable Normal Anti-AFK",
            command=lambda: self.toggle_antiafk("normal")
        )
        self.normal_antiafk_switch.pack(fill="x", padx=10, pady=(0, 10))

        self.gym_antiafk_switch = ctk.CTkSwitch(
            self.content_box,
            text="Enable GYM Anti-AFK",
            command=lambda: self.toggle_antiafk("gym")
        )
        self.gym_antiafk_switch.pack(fill="x", padx=10, pady=(0, 10))

        self.quarry_antiafk_switch = ctk.CTkSwitch(
            self.content_box,
            text="Enable Quarry Anti-AFK (disabled)",
            command=lambda: self.toggle_antiafk("quarry"),
            state=ctk.DISABLED
        )
        self.quarry_antiafk_switch.pack(fill="x", padx=10, pady=(0, 10))

    def load_leo_ui(self):
        ctk.CTkLabel(
            self.content_box,
            text="LEO Menu (LSPD / SAHP / FIB)",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=10, pady=(0, 10))

        badge_row = ctk.CTkFrame(self.content_box, fg_color="transparent")
        badge_row.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(
            badge_row,
            text="Badge Number",
            width=120,
            anchor="w"
        ).pack(side="left")

        self.badge_var = ctk.StringVar(value=str(CONFIG.get("badge_number", "")))
        self.badge_entry = ctk.CTkEntry(
            badge_row,
            placeholder_text="e.g. 109",
            width=160,
            textvariable=self.badge_var
        )
        self.badge_entry.pack(side="left")
        self.badge_entry.bind("<Return>", self.save_leo_settings)
        self.badge_entry.bind("<FocusOut>", self.save_leo_settings)

        offset_row = ctk.CTkFrame(self.content_box, fg_color="transparent")
        offset_row.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(
            offset_row,
            text="GMT Time Adjustment",
            width=120,
            anchor="w"
        ).pack(side="left")

        self.gmt_var = ctk.StringVar(value=str(CONFIG.get("gmt_offset", 0)))
        self.gmt_entry = ctk.CTkEntry(
            offset_row,
            placeholder_text="e.g. -1 or 5.5",
            width=160,
            textvariable=self.gmt_var
        )
        self.gmt_entry.pack(side="left")
        self.gmt_entry.bind("<Return>", self.save_leo_settings)
        self.gmt_entry.bind("<FocusOut>", self.save_leo_settings)

        department_row = ctk.CTkFrame(self.content_box, fg_color="transparent")
        department_row.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(
            department_row,
            text="Department",
            width=120,
            anchor="w"
        ).pack(side="left")

        self.department_box = ctk.CTkComboBox(
            department_row,
            values=["SAHP", "LSPD", "FIB"],
            width=160,
            command=self.save_department
        )
        self.department_box.set(CONFIG.get("department", "LSPD"))
        self.department_box.pack(side="left")

        button_row = ctk.CTkFrame(self.content_box, fg_color="transparent")
        button_row.pack(fill="x", padx=10, pady=(5, 0))
        button_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            button_row,
            text="On Duty",
            font=("Segoe UI", 14, "bold"),
            command=self.leo_onduty
        ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

        ctk.CTkButton(
            button_row,
            text="Off Duty",
            font=("Segoe UI", 14, "bold"),
            command=self.leo_offduty
        ).grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def save_leo_settings(self, _=None):
        badge = self.badge_var.get().strip()
        offset_text = self.gmt_var.get().strip()

        if not badge:
            self.log("Badge number cannot be empty.", True)
            self.badge_var.set(str(CONFIG.get("badge_number", "")))
            return

        try:
            offset = float(offset_text)
        except ValueError:
            self.log("GMT adjustment must be a number.", True)
            self.gmt_var.set(str(CONFIG.get("gmt_offset", 0)))
            return

        CONFIG["badge_number"] = badge
        CONFIG["gmt_offset"] = int(offset) if offset.is_integer() else offset
        save_config(CONFIG)

    def save_department(self, value):
        CONFIG["department"] = value
        save_config(CONFIG)

    def toggle_antiafk(self, mode):
        switches = {
            "normal": self.normal_antiafk_switch,
            "gym": self.gym_antiafk_switch,
            "quarry": self.quarry_antiafk_switch
        }

        if not switches[mode].get():
            if mode == "normal" and afk_modes.NORMAL_AFK_RUNNING:
                self.log("Stopping normal Anti-afk..!")
            elif mode == "gym" and afk_modes.GYM_AFK_RUNNING:
                self.log("Stopping GYM Anti-afk..!")
            elif mode == "quarry" and afk_modes.QUARRY_AFK_RUNNING:
                self.log("Stopping Quarry Anti-afk..!")
            afk_modes.stop_all()
            self.set_afk_switches()
            self.set_idle_status()
            return

        if self.afk_status():
            switches[mode].deselect()
            return

        afk_modes.stop_all()
        self.set_afk_switches(False)

        if mode == "normal":
            afk_modes.NORMAL_AFK_RUNNING = True
            target = afk_modes.start_normal_afk
            label = "Normal AFK"
        elif mode == "gym":
            afk_modes.GYM_AFK_RUNNING = True
            target = afk_modes.start_gym_afk
            label = "Gym AFK"
        else:
            afk_modes.QUARRY_AFK_RUNNING = True
            target = afk_modes.start_quarry_afk
            label = "Quarry AFK"

        switches[mode].select()
        self.log("Stopping all active AFK modes..!")
        self.log(f"Starting {label} in 3sec..!")
        Thread(target=target, daemon=True).start()
        self.set_afk_status(label)

    def afk_status(self):
        running = [
            ("Normal AFK", afk_modes.NORMAL_AFK_RUNNING),
            ("Gym AFK", afk_modes.GYM_AFK_RUNNING),
            ("Quarry AFK", afk_modes.QUARRY_AFK_RUNNING)
        ]

        for label, active in running:
            if active:
                self.set_afk_status(label)
                self.log(f"Please turn off {label} to run other AFK modes...", True)
                return True

        self.set_idle_status()
        return False

    def set_afk_switches(self, enabled=True):
        switches = (
            self.normal_antiafk_switch,
            self.gym_antiafk_switch,
            self.quarry_antiafk_switch
        )

        for switch in switches:
            if enabled:
                switch.deselect()
            else:
                switch.deselect()

    def set_afk_status(self, label):
        self.app_status.configure(
            text=f"App Status: {label} Running",
            text_color="green"
        )

    def set_idle_status(self):
        self.app_status.configure(
            text="App Status: Idle",
            text_color="orange"
        )

    def leo_onduty(self):
        self.run_leo(1)

    def leo_offduty(self):
        self.run_leo(0)

    def run_leo(self, duty):
        self.save_leo_settings()

        if not CONFIG.get("badge_number"):
            self.log("Badge Number wasn't provided!", True)
            return

        duty_name = "on-duty" if duty else "off-duty"
        self.log(f"Starting LEO {duty_name} command automation in 3sec..!")
        Thread(
            target=do_leo_automation,
            args=(CONFIG, duty),
            daemon=True
        ).start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
