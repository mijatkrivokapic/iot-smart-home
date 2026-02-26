from threading import Timer

from mqtt_helper import send_actuator_command
from system_state import AlarmStatus, state

from .dus import MotionDirection, infer_direction

light_timer = None


def turn_off_light():
    global light_timer
    print("Turning off the light (DL) after 10 seconds of no motion.")
    send_actuator_command("PI1", "DL", 0)
    light_timer = None


def turn_on_alarm():
    if (
        state.get("alarm_status") is AlarmStatus.ARMED
        and state.get("people_count") == 0
        and not state.get("alarm_door_timer")
    ):
        state.set_alarm_status(AlarmStatus.ACTIVATED)
        print("🚨 Alarm Activated due to motion detected while armed!")


def handle_pir(payload):
    global light_timer

    if payload.get("value") == 1:
        if state.get("alarm_config").get("sensor_alarm", False):
            turn_on_alarm()

        if payload.get("device") == "PI1":
            send_actuator_command("PI1", "DL", 1)

            if light_timer is not None:
                light_timer.cancel()

            light_timer = Timer(10.0, turn_off_light)
            light_timer.start()

        try:
            direction = infer_direction()
            if direction is MotionDirection.ENTER:
                state.adjust_people_count(1)
            elif direction is MotionDirection.LEAVE:
                state.adjust_people_count(-1)
        except Exception as e:
            print(f"✗ Error inferring entry/exit: {e}")
