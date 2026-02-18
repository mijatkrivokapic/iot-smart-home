import threading
import time

from mqtt_wrapper import send_measurement
from simulators.dms import run_dms_simulator


def dms_callback(key, sensor_config):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: {sensor_config['component']} (Membrane Switch)")
    print(f"Key pressed: {key}")
    
    # Send measurement to MQTT
    topic = sensor_config.get('topic', 'home/keypad')
    send_measurement(topic, key, f"{sensor_config['component']}", sensor_config['device'], is_simulated=sensor_config['simulated'])

def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['component']} simulator")
        dms_thread = threading.Thread(
            target=run_dms_simulator, 
            args=(2, dms_callback, stop_event, settings)
        )
        dms_thread.start()
        threads.append(dms_thread)
    else:
        from sensors.dms import run_dms_sensor
        print(f"Starting {settings['component']} sensor")
        dms_thread = threading.Thread(
            target=run_dms_sensor, 
            args=(2, dms_callback, stop_event, settings)
        )
        dms_thread.start()
        threads.append(dms_thread)