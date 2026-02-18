import threading
import time
import socketio
from mqtt_helper import send_actuator_command
import socketio_helper

class SystemState:
    def __init__(self):
        self._state = {
            "alarm_status": "ARMED",  # DISARMED, ARMED, ACTIVATED
            "people_count": 0,
        }
        self._lock = threading.Lock()

    def set_alarm_status(self, new_status):
        with self._lock:
            old_status = self._state["alarm_status"]
            if old_status == new_status:
                return

            self._state["alarm_status"] = new_status
            print(f"📢 Alarm state changed: {old_status} -> {new_status}")

            if new_status == "ACTIVATED":
                send_actuator_command("PI1","DB",1,None)
                print("🚀 Command Sent: BUZZER ON")
            
            elif new_status == "ARMED":
                send_actuator_command("PI1","DB",0,None)
                print("🛑 Command Sent: BUZZER OFF")

            socketio_helper.socketio.emit("state-update", self._state)

    def get(self, key):
        with self._lock:
            return self._state.get(key)

    def get_all(self):
        with self._lock:
            return self._state.copy()

# Initialize globally
state = SystemState()