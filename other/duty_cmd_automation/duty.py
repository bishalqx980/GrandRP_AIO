import pyperclip
from datetime import datetime, timezone
from time import sleep
import pydirectinput as pdi

BADGE_NUMMBER = 956
CURRENT_GMT_TIME = datetime.now(timezone.utc).strftime("%H:%M")

print(f"""
Badge No: {BADGE_NUMMBER}

1. On Duty
2. Off Duty

> Note: After giving the command, it will start in 3sec !!
""")

def execute_command(cmd_list: list) -> bool:
    try:
        for cmd in cmd_list:
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
        print(f"Error: {e}")


def take_screenshot():
    pdi.keyDown("alt")
    pdi.press("`")
    pdi.keyUp("alt")


while True:
    try:
        user_input = int(input("> "))
    except Exception as e:
        print(f"Error: {e}")

    if user_input not in [1, 2]:
        print("wrong input!")
        continue

    elif user_input == 1:
        print("Starting in 3sec")
        sleep(3)
        
        ONDUTY_COMMANDS = [
            "/me takes out bodycam, turns it on, and checks for the red light",
            "/do The bodycam is recording, and is ballistic and waterproof",
            f"{BADGE_NUMMBER} to Dispatch Show 10-41 at {CURRENT_GMT_TIME}"
        ]

        res = execute_command(ONDUTY_COMMANDS)
        if res:
            take_screenshot()
            print("Done...")
    
    elif user_input == 2:
        print("Starting in 3sec")
        sleep(3)

        OFFDUTY_COMMANDS = [
            "/do saves the bodycam content and uploads the bodycam to SAHP servers and stops recording",
            f"{BADGE_NUMMBER} to Dispatch Show 10-42 at {CURRENT_GMT_TIME}"
        ]

        res = execute_command(OFFDUTY_COMMANDS)
        if res:
            take_screenshot()
            print("Done...")
    
    sleep(3)
