from threading import Timer
from mqtt_helper import send_actuator_command

light_timer = None

def turn_off_light():
    global light_timer
    print("Turning off the light (DL) after 10 seconds of no motion.")
    
    send_actuator_command("PI1", "DL", 0)
    
    light_timer = None

def handle_dpir1(payload):
    global light_timer
    
    if payload.get("value") == 1:
        send_actuator_command("PI1", "DL", 1)

        if light_timer is not None:
            light_timer.cancel()
        
        light_timer = Timer(10.0, turn_off_light)
        light_timer.start()