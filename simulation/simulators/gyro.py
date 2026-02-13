import time
import random

def generate_gyro_values():
    """
    Generates simulated 3-axis data for Accelerometer and Gyroscope.
    Accel units: g-force (m/s^2)
    Gyro units: degrees per second (dps)
    """
    accel = [0, 0, 16384] 
    gyro = [0, 0, 0]
    
    while True:
        accel = [a + random.randint(-500, 500) for a in accel]
        gyro = [g + random.randint(-100, 100) for g in gyro]
        
        yield accel, gyro

def run_gyro_simulator(delay, callback, stop_event, sensor_config=None):
    """
    Mimics the interface of the real run_gyro_sensor function.
    """
    data_generator = generate_gyro_values()
    
    while not stop_event.is_set():
        accel, gyro = next(data_generator)
        
        callback(accel, gyro, sensor_config)
        
        time.sleep(delay)