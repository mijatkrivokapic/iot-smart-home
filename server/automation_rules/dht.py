from mqtt_helper import send_actuator_command


def handle_dht(payload):
    data = {**payload['value'], "sensor": payload['sensor']}
    send_actuator_command("PI3", "LCD", data)