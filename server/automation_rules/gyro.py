from system_state import AlarmStatus, state

GRAVITY_BASE = 16384
THRESHOLD_ACCEL_MOVE = 3000
FREE_FALL_THRESHOLD = 2000


def handle_accel(payload):
    mag_accel = payload.get("value", 0)

    if mag_accel < FREE_FALL_THRESHOLD:
        print(f"FREE FALL DETECTED! Mag: {mag_accel}")
        turn_on_alarm()
        return

    accel_diff = abs(mag_accel - GRAVITY_BASE)
    if accel_diff > THRESHOLD_ACCEL_MOVE:
        print(f"SUDDEN MOVEMENT! Diff: {accel_diff}")
        turn_on_alarm()
        return


def handle_gyro(payload):
    mag_gyro = payload.get("value", 0)

    if mag_gyro > 2000:
        print(f"ROTATION DETECTED! Mag: {mag_gyro}")
        turn_on_alarm()
        return


def turn_on_alarm():
    if state.get("alarm_status") is AlarmStatus.ARMED and state.get("alarm_config").get("gyro_alarm", False):
        state.set_alarm_status(AlarmStatus.ACTIVATED)
        print("🚨 Alarm Activated!")
