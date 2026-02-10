from mqtt_publisher import send_measurement
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


def toggle_buzzer(settings, state):
    if settings['simulated']:
        print(f"SIMULATOR: Door Buzzer is now {'ON' if state else 'OFF'}")
        topic = settings['topic']
        send_measurement(topic, 1 if state else 0, "DB", settings['device'], is_simulated=settings['simulated'])
    else:
        GPIO.setmode(GPIO.BCM)
        buzzer_pin = settings['pin']
        GPIO.setup(buzzer_pin, GPIO.OUT)
        GPIO.output(buzzer_pin, True)