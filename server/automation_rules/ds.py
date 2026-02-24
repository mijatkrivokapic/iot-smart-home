from threading import Lock, Timer

from system_state import AlarmStatus, state

alarm_timer = None



def turn_on_alarm():
    global alarm_timer
    if state.get("alarm_status") is AlarmStatus.ARMED:
        state.set_alarm_status(AlarmStatus.ACTIVATED)
        print("🚨 Alarm Activated!")
    alarm_timer = None


def turn_off_alarm():
    if state.get("alarm_status") is AlarmStatus.ACTIVATED:
        state.set_alarm_status(AlarmStatus.DISARMED)
        print("🛑 Alarm Deactivated.")


def handle_ds(payload):
    global alarm_timer, open_door_timer, door_alarm
    sensor_value = payload.get("value")
    current_status = state.get("alarm_status")

    if sensor_value == 1:
        if current_status is AlarmStatus.ACTIVATED:
            return

        if state.get("alarm_config").get("door_alarm", False) and current_status is AlarmStatus.ARMED:
            if alarm_timer is None:
                alarm_timer = Timer(10.0, turn_on_alarm)
                alarm_timer.start()


        
