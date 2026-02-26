import time
import random

DETECTION_PROBABILITY = 0.2 

def run_pir_simulator(delay, callback, stop_event, sensor_config=None):
    while True:
        motion_detected = random.random() < DETECTION_PROBABILITY
        callback(motion_detected, sensor_config)
        if stop_event.is_set():
            break
        time.sleep(delay)