import time
import random

import random

def generate_gyro_values(incident_chance=0.2):
    base_accel = [0, 0, 16384] 
    
    while True:
        r = random.random()
        
        if r < (incident_chance / 2):
            # INCIDENT 1: free fall
            accel = [random.randint(-500, 500) for _ in range(3)]
            gyro = [random.randint(-1000, 1000) for _ in range(3)]
            print("\n[SIMULATOR] OBJECT IN FREE FALL!")
            
        elif r < incident_chance:
            # INCIDENT 2: sudden move
            accel = [a + random.randint(5000, 10000) for a in base_accel]
            gyro = [random.randint(2000, 5000) for _ in range(3)]
            print("\n[SIMULATOR] DETECTED SUDDEN MOVE!")
            
        else:
            accel = [a + random.randint(-200, 200) for a in base_accel]
            gyro = [0 + random.randint(-50, 50) for _ in range(3)]
            
        yield accel, gyro

def run_gyro_simulator(delay, callback, stop_event, sensor_config=None):
    """
    Mimics the interface of the real run_gyro_sensor function.
    """
    print("fdfsdfsdf")
    data_generator = generate_gyro_values()
    
    while not stop_event.is_set():
        accel, gyro = next(data_generator)
        
        callback(accel, gyro, sensor_config)
        
        time.sleep(delay)