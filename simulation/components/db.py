from mqtt_wrapper import send_measurement
from settings import load_settings
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


def toggle_buzzer(settings, state):
    if settings['simulated']:
        print(f"SIMULATOR: Door Buzzer is now {'ON' if state else 'OFF'}")
    else:
        print("state: ", state)
        GPIO.setmode(GPIO.BCM)
        buzzer_pin = settings['pin']
        GPIO.setup(buzzer_pin, GPIO.OUT)
        if state == 1:
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
            print("Turning off buzzer")
            GPIO.output(buzzer_pin, GPIO.LOW)
    topic = settings['topic']
    send_measurement(topic, 1 if state else 0, settings['component'], settings['device'], is_simulated=settings['simulated'])

def handle_db(payload):
    print(f"Handling DB command with payload: {payload}")
    action = payload.get("action")
    settings = load_settings()['PI1']['DB']
    toggle_buzzer(settings, action)