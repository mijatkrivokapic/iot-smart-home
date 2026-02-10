import RPi.GPIO as GPIO
import time


def run_pir_sensor(delay, callback, stop_event, sensor_config=None):
    PIR_PIN = sensor_config['pin']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    def motion_detected(channel):
        callback(True, sensor_config)

    def no_motion(channel):
        callback(False, sensor_config)


    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)
    GPIO.add_event_detect(PIR_PIN, GPIO.FALLING, callback=no_motion)

    try:
        while not stop_event.is_set():
            time.sleep(delay)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.remove_event_detect(PIR_PIN)
        GPIO.cleanup()