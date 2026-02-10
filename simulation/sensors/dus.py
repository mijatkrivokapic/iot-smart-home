import time

import RPi.GPIO as GPIO


def get_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    max_iter = 100

    iter = 0
    while GPIO.input(ECHO_PIN) == 0:
        if iter > max_iter:
            return None
        pulse_start_time = time.time()
        iter += 1

    iter = 0
    while GPIO.input(ECHO_PIN) == 1:
        if iter > max_iter:
            return None
        pulse_end_time = time.time()
        iter += 1

    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300)/2
    return distance

def run_dus_sensor(delay, callback, stop_event, sensor_config=None):
    global TRIG_PIN, ECHO_PIN
    TRIG_PIN = sensor_config['trig']
    ECHO_PIN = sensor_config['echo']

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    try:
        while not stop_event.is_set():
            distance = get_distance()
            if distance is not None:
                callback(distance, sensor_config)
            time.sleep(delay)
    except Exception as e:
        print(f"Error: {e}")
