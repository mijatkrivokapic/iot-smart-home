import threading
import time
from simulators.ds import run_ds_simulator

def ds_callback(state):
    t = time.localtime()
    status = "PRESSED (Open)" if state == 1 else "RELEASED (Closed)"
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: DS1 (Door Sensor)")
    print(f"State: {status}")

def run_ds(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DS1 simulator")
        ds_thread = threading.Thread(target=run_ds_simulator, args=(2, ds_callback, stop_event))
        ds_thread.start()
        threads.append(ds_thread)
    else:
        pass # TODO: implement real sensor logic