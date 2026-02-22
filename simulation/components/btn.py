import threading
import time

from mqtt_wrapper import send_measurement
from simulators.btn import run_btn_simulator
from sensors.ds import run_ds_sensor


def btn_callback(state, sensor_config):
    t = time.localtime()
    status = "PRESSED (Open)" if state == 1 else "RELEASED (Closed)"
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: {sensor_config['component']} ({sensor_config['device']} Door Sensor)")
    print(f"State: {status}")
    
    topic = sensor_config.get('topic', 'home/door_sensor')
    send_measurement(topic, state, sensor_config['component'], sensor_config['device'], is_simulated=sensor_config['simulated'])

def run_btn(settings, threads, stop_event):
    if settings['simulated']:
        ds_thread = threading.Thread(
            target=run_btn_simulator, 
            args=(10, btn_callback, stop_event, settings)
        )
        ds_thread.start()
        threads.append(ds_thread)
    else:
        ds_thread = threading.Thread(
            target=run_ds_sensor, 
            args=(1, btn_callback, stop_event, settings)
        )
        ds_thread.start()
        threads.append(ds_thread)