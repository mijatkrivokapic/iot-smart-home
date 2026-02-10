import threading
import time

from mqtt_publisher import send_measurement
from simulators.dus import run_dus_simulator


def dus_callback(distance, sensor_config):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: DUS1 (Ultrasonic)")
    print(f"Distance: {distance:.2f} cm")
    
    # Send measurement to MQTT
    topic = sensor_config.get('topic', 'home/ultrasonic')
    send_measurement(topic, distance, "DUS1", sensor_config['device'], is_simulated=sensor_config['simulated'])

def run_dus(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DUS1 simulator")
        dus_thread = threading.Thread(
            target=run_dus_simulator, 
            args=(2, dus_callback, stop_event, settings)
        )
        dus_thread.start()
        threads.append(dus_thread)
    else:
        from sensors.dus import run_dus_sensor
        print("Starting DUS1 sensor")
        dus_thread = threading.Thread(
            target=run_dus_sensor, 
            args=(2, dus_callback, stop_event, settings)
        )
        dus_thread.start()
        threads.append(dus_thread)