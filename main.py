from time import sleep
from random import choice
import pydirectinput as pdi
import pygetwindow as gw


TARGET_WINDOW = "RAGЕ Multiрlаyer"

def is_target_focused(target_title: str) -> bool:
    window = gw.getActiveWindow()
    if not window:
        return False
    return target_title.lower().strip() in window.title.lower().strip()

print("AntiAFK by @bishalqx980")

print("""

1. AntiAFK (normal)
2. AntiAFK GYM

"""
)

user_input = input("Type here: ")
available_option = [1, 2]

try:
    user_input = int(user_input)
except:
    pass

if type(user_input) != int:
    print("Wrong input!")
elif user_input not in available_option:
    print("Option not available!")

elif user_input == 1:
    WAIT_TIME = 9 * 60
    HOLD_TIME = 0.75
    STARTING_TIME = 3
    KEYS = ["w", "a", "s", "d"]

    print(f"Anti AFK starting in {STARTING_TIME}!")
    sleep(STARTING_TIME)

    while True:
        if not is_target_focused(TARGET_WINDOW):
            sleep(1)
            continue

        for _ in KEYS:
            key = choice(KEYS)
            print(f"Holding {key.upper()} for {HOLD_TIME} seconds.")

            pdi.keyDown(key)
            sleep(HOLD_TIME)
            pdi.keyUp(key)
            sleep(0.25) # Human delay :)
        
        print(f"Ping given. Waiting {(WAIT_TIME / 60):.2f} minutes...\n")
        sleep(WAIT_TIME)

elif user_input == 2:
    WAIT_TIME = choice([2, 1])
    SCRIPT_STARTING_TIME = 3
    KEY = "e"

    print(f"GYM script starting in {SCRIPT_STARTING_TIME}!")
    sleep(SCRIPT_STARTING_TIME)
    print("Running...")

    while True:
        if not is_target_focused(TARGET_WINDOW):
            sleep(1)
            continue

        pdi.press(KEY)
        sleep(WAIT_TIME)
