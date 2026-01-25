import pyperclip
from datetime import datetime, timezone
from time import sleep
import pydirectinput as pdi


def take_screenshot(keycombo_list):
    holding_key = keycombo_list[0]
    press_key = keycombo_list[1]

    pdi.keyDown(holding_key)
    pdi.press(press_key)
    pdi.keyUp(holding_key)


def do_leo_automation(config, duty):
    """
    :param config: config.json loaded file
    :param duty: int 1 for onduty 0 for offduty
    """
    current_gmt_time = datetime.now(timezone.utc).strftime("%H:%M")
    badge_number = config["badge_number"]
    screenshot_combo = config["screenshot_combo"]
    commands = []

    if duty == 1:
        commands = config["onduty_commands"]
    elif duty == 0:
        commands = config["offduty_commands"]

    # Starting automation
    sleep(3)

    # conflict clear at first attempt
    pdi.press("enter")

    for cmd in commands:
        # Copy the command with formatting
        pyperclip.copy(cmd.format(
            badge = badge_number,
            time = current_gmt_time
        ))

        # main execution
        pdi.press("t")
        sleep(0.25)

        pdi.keyDown("ctrl")
        pdi.press("v")
        pdi.keyUp("ctrl")
        
        pdi.press("enter")

        # human delay
        sleep(0.5)
    
    # Take a screenshot if all done
    take_screenshot(screenshot_combo)
