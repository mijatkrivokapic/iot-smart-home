from threading import Timer
from system_state import state

alarm_timer = None

def turn_on_alarm():
    global alarm_timer
    if state.get("alarm_status") == "ARMED":
        state.set_alarm_status("ACTIVATED")
        print("🚨 Alarm Activated!")
    alarm_timer = None

def turn_off_alarm():
    if state.get("alarm_status") == "ACTIVATED":
        state.set_alarm_status("ARMED")
        print("🛑 Alarm Deactivated.")

def handle_ds1(payload):
    global alarm_timer
    sensor_value = payload.get("value")
    current_status = state.get("alarm_status")

    if sensor_value == 0:
        if alarm_timer is not None:
            alarm_timer.cancel()
            alarm_timer = None
        turn_off_alarm() 

    elif sensor_value == 1:
        if current_status == "ACTIVATED" or current_status == "DISARMED":
            return

        if alarm_timer is None:
            alarm_timer = Timer(5.0, turn_on_alarm)
            alarm_timer.start()