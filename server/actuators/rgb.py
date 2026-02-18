from mqtt_helper import send_actuator_command

COLOR_MAP = {
    'red': (1, 0, 0),
    'green': (0, 1, 0),
    'blue': (0, 0, 1)
}

def handle_rgb(color):
    color = COLOR_MAP.get(color.lower())
    
    if color:
        send_actuator_command("PI3", "BRGB", color)
    else:
        print(f"Unknown color '{color}' received for RGB actuator.")
