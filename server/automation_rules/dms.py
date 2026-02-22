from system_state import AlarmStatus, state

buffer = ""

PASSWORD = "1234"
PW_LEN = len(PASSWORD)

def handle_dms(payload):
    global buffer

    symbol = str(payload.get("value", ""))

    buf = buffer + symbol

    if len(buf) > PW_LEN:
       buf = buf[-PW_LEN:]

    buffer = buf
    print(f"[DMS] buffer='{buf}' (symbol='{symbol}')")

    if buf == PASSWORD:
       current_status = state.get("alarm_status")
       if current_status is AlarmStatus.DISARMED:
           state.set_alarm_status(AlarmStatus.ARMED)
           print("🔓 Door password accepted - alarm arming.")
       else:
           state.set_alarm_status(AlarmStatus.DISARMED)
           print("🔓 Door password accepted - alarm disarmed.")

       buffer = ""
    else:
        print("❌ Incorrect password attempt.")
