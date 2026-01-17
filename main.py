import customtkinter as ctk
from datetime import datetime
from time import sleep
from random import choice
import pydirectinput as pdi
import psutil
import threading

# ---------------------- CONFIG ----------------------
TARGET_PROCESS = "ragemp_game_ui"

def is_process_running(process_name: str) -> bool:
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

# ---------------------- UI APP ----------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AntiAFK - RageMP by @bishalqx980")
        self.geometry("500x400")
        self.minsize(400, 300)

        # Main frame
        self.frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Toggle buttons frame
        self.toggle_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        self.toggle_frame.pack(fill="x", pady=(0, 10))

        # Normal AFK toggle
        self.normal_var = ctk.BooleanVar()
        self.normal_toggle = ctk.CTkSwitch(
            self.toggle_frame, text="Normal AFK", variable=self.normal_var, command=self.toggle_changed
        )
        self.normal_toggle.pack(side="left", padx=10, pady=10)

        # GYM AFK toggle
        self.gym_var = ctk.BooleanVar()
        self.gym_toggle = ctk.CTkSwitch(
            self.toggle_frame, text="GYM AFK", variable=self.gym_var, command=self.toggle_changed
        )
        self.gym_toggle.pack(side="left", padx=10, pady=10)

        # Log area
        self.log_area = ctk.CTkTextbox(self.frame, height=200, corner_radius=10)
        self.log_area.pack(fill="both", expand=True, pady=(0, 10))
        self.log_area.configure(state="disabled")  # Read-only

        # Footer (Developer credit)
        self.footer = ctk.CTkLabel(
            self.frame,
            text="Developed by @bishalqx980",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60")
        )
        self.footer.pack(pady=(0, 0))

        self.log("App started!")

        # Thread control
        self.running = False

    # ---------------------- TOGGLE ----------------------
    def toggle_changed(self):
        # Only allow one toggle at a time
        if self.normal_var.get() and self.gym_var.get():
            self.gym_var.set(False)

        status_normal = "ON" if self.normal_var.get() else "OFF"
        status_gym = "ON" if self.gym_var.get() else "OFF"
        self.log(f"Normal AFK: {status_normal} | GYM AFK: {status_gym}")

        # Start/stop the AFK script
        if self.normal_var.get():
            self.start_script(script_type="normal")
        elif self.gym_var.get():
            self.start_script(script_type="gym")
        else:
            self.stop_script()

    # ---------------------- LOG FUNCTION ----------------------
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"[{timestamp}] {message}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    # ---------------------- SCRIPT CONTROL ----------------------
    def start_script(self, script_type):
        if self.running:
            self.log("Script already running...")
            return
        self.running = True
        thread = threading.Thread(target=self.afk_loop, args=(script_type,), daemon=True)
        thread.start()

    def stop_script(self):
        self.running = False
        self.log("Script stopped.")

    # ---------------------- AFK LOOP ----------------------
    def afk_loop(self, script_type):
        if script_type == "normal":
            WAIT_TIME = 9 * 60
            HOLD_TIME = 1
            STARTING_TIME = 3
            KEYS = ["w", "a", "s", "d"]

            self.log(f"Normal AFK starting in {STARTING_TIME} seconds...")
            sleep(STARTING_TIME)

            while self.running:
                if not is_process_running(TARGET_PROCESS):
                    sleep(1)
                    continue

                key = choice(KEYS)
                self.log(f"Holding {key.upper()} for {HOLD_TIME} seconds.")
                pdi.keyDown(key)
                sleep(HOLD_TIME)
                pdi.keyUp(key)
                sleep(0.25)
                self.log(f"Ping given. Waiting {(WAIT_TIME / 60):.2f} minutes...\n")
                sleep(WAIT_TIME)

        elif script_type == "gym":
            WAIT_TIME = choice([1, 2])
            STARTING_TIME = 3
            KEY = "e"

            self.log(f"GYM AFK starting in {STARTING_TIME} seconds...")
            sleep(STARTING_TIME)
            self.log("Running...")

            while self.running:
                if not is_process_running(TARGET_PROCESS):
                    sleep(1)
                    continue
                pdi.press(KEY)
                self.log(f"Pressed {KEY.upper()}. Waiting {WAIT_TIME} seconds...")
                sleep(WAIT_TIME)


# ---------------------- RUN APP ----------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
