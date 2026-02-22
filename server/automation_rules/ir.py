from mqtt_helper import send_actuator_command

BUTTON_COLOR_MAP = {
    '1': (1, 0, 0), # red
    '2': (0, 1, 0), # green
    '3': (0, 0, 1) # blue
}

def handle_ir(payload):
    color = BUTTON_COLOR_MAP.get(str(payload.get("value")))
    if color:
        send_actuator_command("PI3", "BRGB", color)