import threading
import time

from mqtt_wrapper import send_measurement
try:
    from sensors.gyro.gyro import run_gyro_sensor
except ImportError:
    pass
from simulators.gyro import run_gyro_simulator


def gyro_callback(accel, gyro, sensor_config):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: {sensor_config['component']}")
 
    topic = sensor_config.get('topic', 'home/gyro')
    send_measurement(topic, accel, f"{sensor_config['component']}_Accel", sensor_config['device'], is_simulated=sensor_config['simulated'])
    send_measurement(topic, gyro, f"{sensor_config['component']}_Gyro", sensor_config['device'], is_simulated=sensor_config['simulated'])

def run_gyro(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting Gyro simulator")
        gyro_thread = threading.Thread(
            target=run_gyro_simulator, 
            args=(2, gyro_callback, stop_event, settings)
        )
    else:
        print("Starting Gyro sensor")
        gyro_thread = threading.Thread(
            target=run_gyro_sensor, 
            args=(2, gyro_callback, stop_event, settings)
        )
        gyro_thread.start()
        threads.append(gyro_thread)