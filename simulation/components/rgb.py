try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None
from mqtt_wrapper import send_measurement
from settings import load_settings


def set_rgb_color(settings, r, g, b):
    if settings['simulated']:
        print(f"SIMULATOR: RGB LED set to R:{r} G:{g} B:{b}")
        topic = settings['topic']
        send_measurement(topic, {'r': r, 'g': g, 'b': b}, "RGB", settings['device'], is_simulated=settings['simulated'])
    else:
        if GPIO is None:
            print("GPIO library not available. Cannot control RGB LED.")
            return
        
        red_pin, green_pin, blue_pin = settings['pins'].values()

        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)
        
        GPIO.output(red_pin, r)
        GPIO.output(green_pin, g)
        GPIO.output(blue_pin, b)
        
        send_measurement(settings['topic'], {'r': r, 'g': g, 'b': b}, "RGB", settings['device'], is_simulated=settings['simulated'])

def handle_rgb(payload):
    print(f"Handling RGB command with payload: {payload}")
    r, g, b = payload.get("action", (0, 0, 0))
    settings = load_settings()['PI3']['BRGB']
    set_rgb_color(settings, r, g, b)
