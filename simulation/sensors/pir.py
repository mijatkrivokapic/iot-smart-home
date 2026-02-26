try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
import time


def run_pir_sensor(delay, callback, stop_event, sensor_config=None):
    PIR_PIN = sensor_config['pin']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    def sensor_callback(channel):
        state = GPIO.input(channel)
        callback(True if state else False, sensor_config)
    GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=sensor_callback)

    try:
        while not stop_event.is_set():
            time.sleep(delay)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.remove_event_detect(PIR_PIN)
        GPIO.cleanup(PIR_PIN)