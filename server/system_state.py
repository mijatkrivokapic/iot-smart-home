import threading
from enum import StrEnum
from threading import Timer

import socketio_helper
from mqtt_helper import send_actuator_command, send_message


class AlarmStatus(StrEnum):
    DISARMED = "DISARMED"
    ARMED = "ARMED"
    ACTIVATED = "ACTIVATED"
    ARMING = "ARMING"


class SystemState:
    def __init__(self):
        self._state = {
            "alarm_status": AlarmStatus.DISARMED,
            "people_count": 0,
            "timer_increment": 10,
        }
        self._lock = threading.Lock()
        self._arm_timer = None

    def _change_alarm_status(self, status):
        self._state["alarm_status"] = status
        print(f"📢 Alarm state changed to: {status}")
        if status is AlarmStatus.ACTIVATED:
            send_actuator_command("PI1", "DB", 1, None)
            print("🚀 Command Sent: BUZZER ON")
        elif status is AlarmStatus.DISARMED:
            send_actuator_command("PI1", "DB", 0, None)
            print("🛑 Command Sent: BUZZER OFF")
        socketio_helper.socketio.emit("state-update", self._state)

    def set_alarm_status(self, new_status):
        with self._lock:
            old_status = self._state["alarm_status"]
            if old_status is new_status:
                return

            if new_status is AlarmStatus.ACTIVATED:
                send_message(
                    "home/sensors/alarm_status", {"sensor": "alarm", "value": 1}
                )
            elif new_status is AlarmStatus.DISARMED:
                send_message(
                    "home/sensors/alarm_status", {"sensor": "alarm", "value": 0}
                )

            if self._arm_timer is not None and new_status is AlarmStatus.DISARMED:
                print("⏱️ Alarm disarm - cancelling pending timer")
                self._arm_timer.cancel()
                self._arm_timer = None

            if new_status is AlarmStatus.ARMED:
                if self._arm_timer is not None:
                    return
                self._change_alarm_status(AlarmStatus.ARMING)
                print("⏱️ Alarm arming initiated - will activate in 10 seconds...")
                self._arm_timer = Timer(
                    10.0, self._change_alarm_status, args=[new_status]
                )
                self._arm_timer.start()
            else:
                self._change_alarm_status(new_status)

    def set_timer_increment(self, increment):
        with self._lock:
            self._state["timer_increment"] = increment
            print(f"📢 Timer increment set to: {increment} seconds")
            socketio_helper.socketio.emit("state-update", self._state)

    def adjust_people_count(self, delta: int = 1):
        with self._lock:
            old = int(self._state.get("people_count", 0))
            new = old + int(delta)
            if new < 0:
                new = 0
            self._state["people_count"] = new
            print(f"👥 People count changed: {old} -> {new}")
            if (
                self._state["alarm_status"] is AlarmStatus.ARMED
                and old == 0
                and new > 0
            ):
                self.set_alarm_status(AlarmStatus.ACTIVATED)
            socketio_helper.socketio.emit("state-update", self._state)

    def get(self, key):
        with self._lock:
            return self._state.get(key)

    def get_all(self):
        with self._lock:
            return self._state.copy()


# Initialize globally
state = SystemState()
