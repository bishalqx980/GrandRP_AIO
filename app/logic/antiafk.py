from random import choice
from threading import Event
from time import sleep, time

import pydirectinput as pdi


class AFK_MODES:
    def __init__(self):
        self.NORMAL_AFK_RUNNING = False
        self.GYM_AFK_RUNNING = False
        self.QUARRY_AFK_RUNNING = False
        self._normal_stop = Event()
        self._gym_stop = Event()
        self._quarry_stop = Event()

    def stop_all(self):
        self.NORMAL_AFK_RUNNING = False
        self.GYM_AFK_RUNNING = False
        self.QUARRY_AFK_RUNNING = False
        self._normal_stop.set()
        self._gym_stop.set()
        self._quarry_stop.set()

    def start_normal_afk(self):
        self._normal_stop.clear()
        sleep(3)

        while self.NORMAL_AFK_RUNNING and not self._normal_stop.is_set():
            for _ in range(2):
                if not self.NORMAL_AFK_RUNNING or self._normal_stop.is_set():
                    return

                key = choice(("w", "a", "s", "d"))
                pdi.keyDown(key)
                sleep(0.5)
                pdi.keyUp(key)

            self._normal_stop.wait(9 * 60)

    def start_gym_afk(self):
        self._gym_stop.clear()
        press_delay = choice((2, 3))
        sleep(3)

        while self.GYM_AFK_RUNNING and not self._gym_stop.is_set():
            pdi.press("e")

            if self._gym_stop.wait(press_delay):
                return

    def start_quarry_afk(self):
        self._quarry_stop.clear()
        afk_time = time()
        keys = ("w", "a", "s", "d")
        sleep(3)

        while self.QUARRY_AFK_RUNNING and not self._quarry_stop.is_set():
            if time() - afk_time >= 5 * 60:
                key = choice(keys)
                pdi.keyDown(key)
                sleep(0.5)
                pdi.keyUp(key)
                afk_time = time()

            pdi.keyDown("e")

            if self._quarry_stop.wait(5):
                pdi.keyUp("e")
                return

            pdi.keyUp("e")

            if self._quarry_stop.wait(7):
                return
