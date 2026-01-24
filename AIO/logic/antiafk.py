from time import sleep, time
from random import choice
import pydirectinput as pdi


class AFK_MODES:
    def __init__(self):
        self.NORMAL_AFK_RUNNING = False
        self.GYM_AFK_RUNNING = False
        self.QUARRY_AFK_RUNNING = False
    

    def stop_all(self):
        self.NORMAL_AFK_RUNNING = False
        self.GYM_AFK_RUNNING = False
        self.QUARRY_AFK_RUNNING = False


    def start_normal_afk(self):
        # Variables
        sleep_time = 9 * 60 # 9 Min
        keys = ["w", "a", "s", "d"]

        # Starting delay 3sec
        sleep(3)

        while self.NORMAL_AFK_RUNNING:
            for _ in range(2):
                key = choice(keys)

                pdi.keyDown(key)
                sleep(0.5)
                pdi.keyUp(key)
            # Sleep until next ping time
            sleep(sleep_time)


    def start_gym_afk(self):
        # Variables
        press_delay = choice([2, 3])

        # Starting delay 3sec
        sleep(3)

        while self.GYM_AFK_RUNNING:
            pdi.press("e")
            # press delay
            sleep(press_delay)


    def start_quarry_afk(self):
        # Variables
        afktime = time()
        max_afktime = 5 * 60 # 5 Min
        keys = ["w", "a", "s", "d"]

        # Starting delay 3sec
        sleep(3)

        while self.QUARRY_AFK_RUNNING:
            if (time() - afktime) >= max_afktime:
                key = choice(keys)

                pdi.keyDown(key)
                sleep(0.5)
                pdi.keyUp(key)

                afktime = time()
            
            pdi.keyDown("e")
            sleep(5)
            pdi.keyUp("e")
            sleep(7)
