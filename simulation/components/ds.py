import threading
import time

from mqtt_publisher import send_measurement
from simulators.ds import run_ds_simulator


def ds_callback(state, sensor_config):
    t = time.localtime()
    status = "PRESSED (Open)" if state == 1 else "RELEASED (Closed)"
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: DS1 (Door Sensor)")
    print(f"State: {status}")
    
    # Send measurement to MQTT
    topic = sensor_config.get('topic', 'home/door_sensor')
    send_measurement(topic, state, "DS1", sensor_config['device'], is_simulated=sensor_config['simulated'])

def run_ds(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DS1 simulator")
        ds_thread = threading.Thread(
            target=run_ds_simulator, 
            args=(2, ds_callback, stop_event, settings)
        )
        ds_thread.start()
        threads.append(ds_thread)
    else:
        pass # TODO: implement real sensor logic