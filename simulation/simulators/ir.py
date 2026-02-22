import random
import time

ButtonsNames = ["LEFT",   "RIGHT",      "UP",       "DOWN",       "2",          "3",          "1",        "OK",        "4",         "5",         "6",         "7",         "8",          "9",        "*",         "0",        "#"]  # String list in same order as HEX list

def run_ir_simulator(delay, callback, stop_event, sensor_config=None):
    """
    Simulates the behavior of an IR sensor by generating random button presses.
    """
    while not stop_event.is_set():
        button_index = random.randint(0, len(ButtonsNames) - 1)
        button_name = ButtonsNames[button_index]
        
        callback(button_name, sensor_config)
        
        time.sleep(delay)