import threading
import time

from mqtt_wrapper import send_measurement
from simulators.dht import run_dht_simulator


def dht_callback(humidity, temperature, code, sensor_config):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")

    topic = sensor_config.get('topic', 'home/dht')
    send_measurement(topic, {'humidity': humidity, 'temperature': temperature}, sensor_config['component'], sensor_config['device'], is_simulated=sensor_config['simulated'])



def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event, settings))
            dht1_thread.start()
            threads.append(dht1_thread)
        else:
            from sensors.dht import DHT, run_dht_loop
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, settings))
            dht1_thread.start()
            threads.append(dht1_thread)