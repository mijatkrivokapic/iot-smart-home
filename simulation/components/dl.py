try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
from mqtt_wrapper import send_measurement
from settings import load_settings


def toggle_light(settings, state):
    if settings['simulated']:
        print(f"SIMULATOR: Door Light is now {'ON' if state else 'OFF'}")
        topic = settings['topic']
        send_measurement(topic, 1 if state else 0, "DL", settings['device'], is_simulated=settings['simulated'])
    else:
        # TODO: Actuator setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(settings['pin'], GPIO.OUT)
        GPIO.output(settings['pin'], state)
        send_measurement(settings['topic'], 1 if state else 0, "DL", settings['device'], is_simulated=settings['simulated'])

def handle_dl(payload):
    print(f"Handling DL command with payload: {payload}")
    value = payload.get("action")
    settings = load_settings()['PI1']['DL']
    toggle_light(settings, value)