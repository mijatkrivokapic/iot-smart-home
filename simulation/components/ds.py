import threading
import time

from mqtt_wrapper import send_measurement
from simulators.ds import run_ds_simulator
from sensors.ds import run_ds_sensor


def ds_callback(state, sensor_config):
    t = time.localtime()
    status = "PRESSED (Open)" if state == 1 else "RELEASED (Closed)"
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: {sensor_config['component']} ({sensor_config['device']} Door Sensor)")
    print(f"State: {status}")
    
    # Send measurement to MQTT
    topic = sensor_config.get('topic', 'home/door_sensor')
    send_measurement(topic, state, sensor_config['component'], sensor_config['device'], is_simulated=sensor_config['simulated'])

def run_ds(settings, threads, stop_event):
    if settings['simulated']:
        ds_thread = threading.Thread(
            target=run_ds_simulator, 
            args=(2, ds_callback, stop_event, settings)
        )
        ds_thread.start()
        threads.append(ds_thread)
    else:
        ds_thread = threading.Thread(
            target=run_ds_sensor, 
            args=(2, ds_callback, stop_event, settings)
        )
        ds_thread.start()
        threads.append(ds_thread)