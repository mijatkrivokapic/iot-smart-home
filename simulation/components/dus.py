import threading
import time
from simulators.dus import run_dus_simulator

def dus_callback(distance):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: DUS1 (Ultrasonic)")
    print(f"Distance: {distance:.2f} cm")

def run_dus(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DUS1 simulator")
        dus_thread = threading.Thread(target=run_dus_simulator, args=(2, dus_callback, stop_event))
        dus_thread.start()
        threads.append(dus_thread)
    else:
        pass # TODO: implement real sensor logic