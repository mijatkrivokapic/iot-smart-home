import time

import RPi.GPIO as GPIO


def readLine(line, characters, callback, sensor_config):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        callback(characters[0], sensor_config)
    if(GPIO.input(C2) == 1):
        callback(characters[1], sensor_config)
    if(GPIO.input(C3) == 1):
        callback(characters[2], sensor_config)
    if(GPIO.input(C4) == 1):
        callback(characters[3], sensor_config)
    GPIO.output(line, GPIO.LOW)

def run_dms_sensor(delay, callback, stop_event, sensor_config=None):
    global C1, C2, C3, C4
    R1, R2, R3, R4, C1, C2, C3, C4 = sensor_config['pins']

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(R3, GPIO.OUT)
    GPIO.setup(R4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while not stop_event.is_set():
        readLine(R1, ["1","2","3","A"], callback, sensor_config)
        readLine(R2, ["4","5","6","B"], callback, sensor_config)
        readLine(R3, ["7","8","9","C"], callback, sensor_config)
        readLine(R4, ["*","0","#","D"], callback, sensor_config)
        time.sleep(delay)
