from threading import Lock, Timer

from system_state import AlarmStatus, state

alarm_timer = None
open_door_timer = None

door_alarm = False


def turn_on_alarm():
    global alarm_timer
    if state.get("alarm_status") is AlarmStatus.ARMED:
        state.set_alarm_status(AlarmStatus.ACTIVATED)
        print("🚨 Alarm Activated!")
    alarm_timer = None


def open_door_alarm():
    global door_alarm
    door_alarm = True
    state.set_alarm_status(AlarmStatus.ACTIVATED)
    print("🚨 Door opened while alarm armed - Alarm Activated!")


def turn_off_alarm():
    if state.get("alarm_status") is AlarmStatus.ACTIVATED:
        state.set_alarm_status(AlarmStatus.DISARMED)
        print("🛑 Alarm Deactivated.")


def handle_ds(payload):
    global alarm_timer, open_door_timer, door_alarm
    sensor_value = payload.get("value")
    current_status = state.get("alarm_status")

    if sensor_value == 0:
        # Cancel door alarm timer if door is closed
        if open_door_timer is not None:
            open_door_timer.cancel()
            open_door_timer = None
        if door_alarm:
            door_alarm = False
            turn_off_alarm()
            
    elif sensor_value == 1:
        if current_status is AlarmStatus.ACTIVATED:
            return
        
        if state.get("alarm_config").get("open_door_alarm", False):
            if open_door_timer is None:
                open_door_timer = Timer(5.0, open_door_alarm)
                open_door_timer.start()

        if state.get("alarm_config").get("door_alarm", False) and current_status is AlarmStatus.ARMED:
            if alarm_timer is None:
                alarm_timer = Timer(10.0, turn_on_alarm)
                alarm_timer.start()


        
