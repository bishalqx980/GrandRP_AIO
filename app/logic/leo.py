from datetime import datetime, timedelta, timezone
from time import sleep

import pydirectinput as pdi
import pyperclip


def take_screenshot(keycombo):
    holding_key, press_key = keycombo
    pdi.keyDown(holding_key)
    try:
        pdi.press(press_key)
    finally:
        pdi.keyUp(holding_key)


def get_gmt_time(config):
    offset = float(config.get("gmt_offset", 0))
    current_time = datetime.now(timezone.utc) + timedelta(hours=offset)
    return current_time.strftime("%H:%M")


def do_leo_automation(config, duty):
    badge_number = config["badge_number"]
    department = config.get("department", "LSPD")
    screenshot_combo = config["screenshot_combo"]
    commands = (
        config["onduty_commands"]
        if duty == 1
        else config["offduty_commands"]
    )
    current_gmt_time = get_gmt_time(config)

    sleep(3)
    pdi.press("enter")

    for command in commands:
        pyperclip.copy(
            command.format(
                badge=badge_number,
                department=department,
                time=current_gmt_time
            )
        )

        pdi.press("t")
        sleep(0.25)

        pdi.keyDown("ctrl")
        try:
            pdi.press("v")
        finally:
            pdi.keyUp("ctrl")

        pdi.press("enter")
        sleep(0.5)

    take_screenshot(screenshot_combo)
