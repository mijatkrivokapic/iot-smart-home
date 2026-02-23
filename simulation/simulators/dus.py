import random
import time

INITIAL_DISTANCE = 50


def generate_distance():
    dist = INITIAL_DISTANCE
    while True:
        dist = dist + random.randint(-10, 10)
        dist = max(5, min(400, dist))
        yield dist


def run_dus_simulator(delay, callback, stop_event, sensor_config=None):
    for d in generate_distance():
        time.sleep(delay)
        callback(d, sensor_config)
        if stop_event.is_set():
            break
