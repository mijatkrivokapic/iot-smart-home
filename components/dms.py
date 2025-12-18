import threading
import time
from simulators.dms import run_dms_simulator

def dms_callback(key):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: DMS (Membrane Switch)")
    print(f"Key pressed: {key}")

def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DMS simulator")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(2, dms_callback, stop_event))
        dms_thread.start()
        threads.append(dms_thread)
    else:
        pass #TODO: implement real sensor logic