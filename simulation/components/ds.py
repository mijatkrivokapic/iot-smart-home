import threading
import time

from mqtt_wrapper import send_measurement
from simulators.ds import run_ds_simulator
from sensors.ds import run_ds_sensor

is_paused = False


def ds_callback(state, sensor_config):
    global is_paused
    if is_paused:
        return
    _send_to_mqtt(state, sensor_config)

def _send_to_mqtt(state, sensor_config):
    t = time.localtime()
    status = "PRESSED (Open)" if state == 1 else "RELEASED (Closed)"
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: {sensor_config['component']} ({sensor_config['device']} Door Sensor)")
    print(f"State: {status}")
    
    # Send measurement to MQTT
    topic = sensor_config.get('topic', 'home/door_sensor')
    send_measurement(topic, state, sensor_config['component'], sensor_config['device'], is_simulated=sensor_config['simulated'])

def trigger_door_opened_event(settings):
    global is_paused
    if is_paused:
        return

    is_paused = True
    
    _send_to_mqtt(1, settings)
    
    timer = threading.Timer(6.0, resume_ds)
    timer.start()

def resume_ds():
    global is_paused
    is_paused = False

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