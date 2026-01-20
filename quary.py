from time import sleep, time
from random import choice
import pydirectinput as pdi

count = 0
afktime = time()

print("Starting in 3s...")
sleep(3)

keys = ["a", "s", "d", "w"]

while True:
    if (time() - afktime) >= 300:
        antiafk = choice(keys)
        pdi.keyDown(antiafk)
        sleep(0.5)
        pdi.keyUp(antiafk)

        afktime = time()

    pdi.keyDown("e")
    sleep(5)
    pdi.keyUp("e")
    sleep(7)

    count += 1

    print(f"Done: {count}", end="", flush=True)
