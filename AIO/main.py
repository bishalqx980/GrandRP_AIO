from datetime import datetime
from threading import Thread
import customtkinter as ctk
from logic.antiafk import AFK_MODES

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
afk_modes = AFK_MODES()
__version__ = "0.3 - (beta)"


class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("GrandRP - AIO")
        self.geometry("700x500")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Top status bar
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.top_frame.grid_columnconfigure(1, weight=1)

        # App status
        self.app_status = ctk.CTkLabel(
            self.top_frame,
            text="App Status: Idle",
            text_color="orange"
        )
        self.app_status.grid(row=0, column=0, padx=10)

        # title
        self.title_label = ctk.CTkLabel(
            self.top_frame,
            text="GrandRP - AIO",
            font=("Segoe UI", 18, "bold")
        )
        self.title_label.grid(row=0, column=1, sticky="e", padx=10)

        # Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
        
        self.antiafk_btn = ctk.CTkButton(
            self.button_frame,
            width=100,
            text="AntiAFK",
            font=("Segoe UI", 14, "bold")
        )
        self.antiafk_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

        self.leo_btn = ctk.CTkButton(
            self.button_frame,
            width=100,
            text="Leo",
            font=("Segoe UI", 14, "bold")
        )
        self.leo_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=10)

        # self.autoclicker_btn = ctk.CTkButton(
        #     self.button_frame,
        #     text="Autoclicker",
        #     font=("Segoe UI", 14, "bold")
        # )
        # self.autoclicker_btn.grid(row=0, column=2, sticky="ew", padx=5, pady=10)

        # self.misc_btn = ctk.CTkButton(
        #     self.button_frame,
        #     text="Misc",
        #     font=("Segoe UI", 14, "bold")
        # )
        # self.misc_btn.grid(row=0, column=3, sticky="ew", padx=5, pady=10)

        self.antiafk_btn.configure(command=lambda: self.switch_section("antiafk"))
        self.leo_btn.configure(command=lambda: self.switch_section("leo"))
        # self.autoclicker_btn.configure(command=lambda: self.switch_section("autoclicker"))
        # self.misc_btn.configure(command=lambda: self.switch_section("misc"))

        # Tab navigation
        self.nav_buttons = {
            "antiafk": self.antiafk_btn,
            "leo": self.leo_btn,
            # "autoclicker": self.autoclicker_btn,
            # "misc": self.misc_btn,
        }

        self.active_section = None

        self.normal_color = self.antiafk_btn.cget("fg_color")
        self.active_color = ("#001755")

        # Activity Status
        # self.activity_status = ctk.CTkLabel(
        #     self,
        #     text="Status: Idle",
        #     font=("Segoe UI", 14)
        # )
        # self.activity_status.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 10))

        # Main area (Content & Log)
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        self.log_frame.grid_rowconfigure(0, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)

        # Content Area
        self.content_box = ctk.CTkFrame(self.log_frame)
        self.content_box.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Log TextArea
        self.log_box = ctk.CTkTextbox(self.log_frame)
        self.log_box.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.log_frame.grid_columnconfigure(0, weight=1) # Left side
        self.log_frame.grid_columnconfigure(1, weight=1) # Right side
        self.log_frame.grid_rowconfigure(0, weight=1)

        self.log_box.configure(state="disabled")
        self.log_box.tag_config(
            "time",
            foreground="#ffcc81"
        )
        self.log_box.tag_config(
            "msg",
            foreground="#b1b1b1"
        )
        self.log_box.tag_config(
            "error",
            foreground="#ff0000"
        )
        self.log_box.bind("<Key>", lambda e: "break")
        self.log_box.bind("<Button-1>", lambda e: "break")

        self.log("App initialized...")
        self.switch_section("antiafk") # Default Section

        # Credit
        self.footer = ctk.CTkLabel(
            self,
            text=f"Developed by @bishalqx980 | App Version: {__version__}",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.footer.grid(row=4, column=0, pady=(0, 10))
    

    # Functions
    def log(self, message: str, error = False):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")

        self.log_box.insert("end", f"[{timestamp}] ", "time")
        self.log_box.insert("end", f"- {message}\n", "msg" if not error else "error")

        self.log_box.see("end") # auto scroll
        self.log_box.configure(state="disabled")
    

    def switch_section(self, section: str):
        if self.active_section == section:
            return # already active, do nothing

        self.active_section = section

        # update top button visuals
        for name, btn in self.nav_buttons.items():
            if name == section:
                btn.configure(fg_color=self.active_color)
            else:
                btn.configure(fg_color=self.normal_color)

        # clear content area
        for widget in self.content_box.winfo_children():
            widget.destroy()

        # load section UI
        if section == "antiafk":
            self.load_antiafk_ui()
        elif section == "leo":
            self.load_leo_ui()
        elif section == "autoclicker":
            self.load_autoclicker_ui()
        elif section == "misc":
            self.load_misc_ui()
    

    def load_antiafk_ui(self):
        ctk.CTkLabel(
            self.content_box,
            text="AntiAFK Menu",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=10, pady=(0, 10))

        self.normal_antiafk_switch = ctk.CTkSwitch(
            self.content_box,
            text="Enable Normal Anti-AFK",
            command=self.toggle_normal_antiafk
        )
        self.normal_antiafk_switch.pack(fill="x", padx=10, pady=(0, 10))

        self.gym_antiafk_switch = ctk.CTkSwitch(
            self.content_box,
            text="Enable GYM Anti-AFK",
            command=self.toggle_gym_antiafk
        )
        self.gym_antiafk_switch.pack(fill="x", padx=10, pady=(0, 10))

        self.quarry_antiafk_switch = ctk.CTkSwitch(
            self.content_box,
            text="Enable Quarry Anti-AFK",
            command=self.toggle_quarry_antiafk
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

        self.badge_entry = ctk.CTkEntry(
            badge_row,
            placeholder_text="e.g. 109",
            width=160
        )
        self.badge_entry.pack(side="left", padx=(0, 10))

        btn_row = ctk.CTkFrame(self.content_box, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(0, 10))

        btn_row.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_row,
            text="On Duty",
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.log("On duty")
        ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

        ctk.CTkButton(
            btn_row,
            text="Off Duty",
            font=("Segoe UI", 14, "bold"),
            command=lambda: self.log("Off duty")
        ).grid(row=0, column=1, sticky="ew", padx=(5, 0))

    # def load_autoclicker_ui(self):
    #     self.log("Autoclicker Menu...")
    

    # def load_misc_ui(self):
    #     self.log("Misc Menu...")

    def afk_status(self):
        if afk_modes.NORMAL_AFK_RUNNING:
            self.app_status.configure(text="App Status: Normal AFK Running", text_color="green")
            self.log("Please turn off Normal AFK to run other AFK modes...", True)
            return True
        elif afk_modes.GYM_AFK_RUNNING:
            self.app_status.configure(text="App Status: Gym AFK Running", text_color="green")
            self.log("Please turn off Gym AFK to run other AFK modes...", True)
            return True
        elif afk_modes.QUARRY_AFK_RUNNING:
            self.app_status.configure(text="App Status: Quarry AFK Running", text_color="green")
            self.log("Please turn off Quarry AFK to run other AFK modes...", True)
            return True
        else:
            self.app_status.configure(text="App Status: Idle", text_color="orange")
            return False

        # if any([
        #     afk_modes.NORMAL_AFK_RUNNING,
        #     afk_modes.GYM_AFK_RUNNING,
        #     afk_modes.QUARRY_AFK_RUNNING
        # ]):
        #     self.log("Please turn of other anti-afk modes...", True)
        #     self.app_status.configure(text="")
        #     return True
        # else:
        #     return False
    

    # Functions
    def toggle_normal_antiafk(self):
        if self.normal_antiafk_switch.get():
            if self.afk_status():
                return
            
            self.log("Stopping all active AFK modes..!")

            afk_modes.stop_all()
            afk_modes.NORMAL_AFK_RUNNING = True

            self.log("Starting normal Anti-afk in 3sec..!")
            thread = Thread(target=afk_modes.start_normal_afk, daemon=True)
            thread.start()
            self.app_status.configure(text="App Status: Normal AFK Running", text_color="green")
        elif afk_modes.NORMAL_AFK_RUNNING:
            self.log("Stopping normal Anti-afk..!")
            afk_modes.stop_all()
            self.app_status.configure(text="App Status: Idle", text_color="orange")


    def toggle_gym_antiafk(self):
        if self.gym_antiafk_switch.get():
            if self.afk_status():
                return
            
            self.log("Stopping all active AFK modes..!")

            afk_modes.stop_all()
            afk_modes.GYM_AFK_RUNNING = True

            self.log("Starting GYM Anti-afk in 3sec..!")
            thread = Thread(target=afk_modes.start_gym_afk, daemon=True)
            thread.start()
            self.app_status.configure(text="App Status: Gym AFK Running", text_color="green")
        elif afk_modes.GYM_AFK_RUNNING:
            self.log("Stopping GYM Anti-afk..!")
            afk_modes.stop_all()
            self.app_status.configure(text="App Status: Idle", text_color="orange")
    

    def toggle_quarry_antiafk(self):
        if self.quarry_antiafk_switch.get():
            if self.afk_status():
                return
            
            self.log("Stopping all active AFK modes..!")

            afk_modes.stop_all()
            afk_modes.QUARRY_AFK_RUNNING = True

            self.log("Starting Quarry Anti-afk in 3sec..!")
            thread = Thread(target=afk_modes.start_quarry_afk, daemon=True)
            thread.start()
            self.app_status.configure(text="App Status: Quarry AFK Running", text_color="green")
        elif afk_modes.QUARRY_AFK_RUNNING:
            self.log("Stopping Quarry Anti-afk..!")
            afk_modes.stop_all()
            self.app_status.configure(text="App Status: Idle", text_color="orange")


if __name__ == "__main__":
    app = App()
    app.mainloop()
