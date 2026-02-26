import time
import random

DETECTION_PROBABILITY = 0.2

def run_ds_simulator(delay, callback, stop_event, sensor_config=None):
    while True:
        state = int(random.random() < DETECTION_PROBABILITY)
        callback(state, sensor_config)
        if stop_event.is_set():
            break
        time.sleep(delay)