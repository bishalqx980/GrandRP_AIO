import pydirectinput
import threading
import time

pydirectinput.PAUSE = 0
pydirectinput.FAILSAFE = False

class AutoClicker:

    def __init__(self):
        self.running = False
        self.position = None
        self.interval = 0.5
        self.follow_mouse = False
        self.thread = threading.Thread(target=self._click_loop, daemon=True)
        self.thread.start()

    def set_position(self, pos):
        self.position = pos
        self.follow_mouse = False

    def set_follow_mouse(self, value: bool):
        self.follow_mouse = value

    def set_delay(self, seconds):
        self.interval = seconds

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def _click_loop(self):
        while True:
            if self.running:

                if self.follow_mouse:
                    x, y = pydirectinput.position()

                elif self.position:
                    x, y = self.position

                else:
                    time.sleep(0.1)
                    continue

                pydirectinput.moveTo(x, y)
                pydirectinput.click()
                time.sleep(self.interval)

            else:
                time.sleep(0.05)
