try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
import time

def run_ds_sensor(delay, callback, stop_event, sensor_config=None):
    PORT_BUTTON = sensor_config['pin']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def hardware_callback(channel):
        state = 0 if GPIO.input(PORT_BUTTON) else 1
        callback(state, sensor_config)

    GPIO.add_event_detect(PORT_BUTTON, GPIO.BOTH, 
                          callback=hardware_callback, 
                          bouncetime=100)

    try:
        while not stop_event.is_set():
            time.sleep(delay)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.remove_event_detect(PORT_BUTTON)
        GPIO.cleanup()