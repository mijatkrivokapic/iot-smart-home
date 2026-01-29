import time
import random

DETECTION_PROBABILITY = 0.2 

def run_pir_simulator(delay, callback, stop_event):
    while True:
        motion_detected = random.random() < DETECTION_PROBABILITY
        if motion_detected:
            callback() 
        if stop_event.is_set():
            break
        time.sleep(delay)