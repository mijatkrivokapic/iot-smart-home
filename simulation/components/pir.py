import threading
import time
from simulators.pir import run_pir_simulator

def pir_callback():
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: DPIR1 (Motion Detected!)")

def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DPIR1 simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, pir_callback, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
    else:
        pass #TODO: implement real sensor logic