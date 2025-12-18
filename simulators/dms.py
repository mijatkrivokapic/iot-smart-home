import time
import random

def run_dms_simulator(delay, callback, stop_event):
    keys = ["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "*", "0", "#"]
    while True:
        key = random.choice(keys)
        callback(key)
        if stop_event.is_set():
            break
        time.sleep(delay)