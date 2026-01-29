import threading
import time
from simulators.pir import run_pir_simulator
from mqtt_publisher import send_measurement

def pir_callback(motion_detected, sensor_config):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if motion_detected:
        print(f"Sensor: DPIR1 (Motion Detected!)")
    
    # Send measurement to MQTT (1 for motion, 0 for no motion)
    topic = sensor_config.get('topic', 'home/motion')
    send_measurement(topic, 1 if motion_detected else 0, "DPIR1", is_simulated=sensor_config['simulated'])

def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DPIR1 simulator")
        pir_thread = threading.Thread(
            target=run_pir_simulator, 
            args=(2, pir_callback, stop_event, settings)
        )
        pir_thread.start()
        threads.append(pir_thread)
    else:
        pass #TODO: implement real sensor logic