import customtkinter as ctk
import pydirectinput
import threading
import time

pydirectinput.PAUSE = 0
pydirectinput.FAILSAFE = False

class PositionSelector:

    def __init__(self, parent):
        self.parent = parent
        self.position = None
        self.window = None
        self.running = True

    def start(self):
        self.window = ctk.CTkToplevel(self.parent)

        # Fullscreen + always on top
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-topmost", True)

        # 10% opacity overlay
        self.window.attributes("-alpha", 0.1)
        self.window.configure(fg_color="black")

        # Remove borders
        self.window.overrideredirect(True)

        # Info label
        self.label = ctk.CTkLabel(
            self.window,
            text="X: 0  Y: 0",
            font=("Arial", 18, "bold"),
            text_color="white",
            fg_color="#222222",
            corner_radius=6
        )

        self.label.place(x=10, y=10)

        self.window.bind("<Button-1>", self._on_click)

        threading.Thread(target=self._track_mouse, daemon=True).start()

        self.parent.wait_window(self.window)
        return self.position

    def _track_mouse(self):
        while self.running:
            x, y = pydirectinput.position()

            try:
                self.label.configure(text=f"X: {x}  Y: {y}")
            except:
                break

            time.sleep(0.03)

    def _on_click(self, event):
        self.position = pydirectinput.position()
        self.running = False
        self.window.destroy()
