import time
import random


def run_btn_simulator(delay, callback, stop_event, sensor_config=None):
    while True:
        callback(1, sensor_config)
        if stop_event.is_set():
            break
        time.sleep(delay)