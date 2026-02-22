from system_state import state
from mqtt_helper import send_actuator_command

def handle_btn(payload):
    value = payload.get("value")
    if value == 1:
        send_actuator_command("PI2","4SD","add_time",state.get("timer_increment"))