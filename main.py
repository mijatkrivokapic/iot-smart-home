import threading
import sys
import time
from settings import load_settings
from components.pir import run_pir
from components.dus import run_dus
from components.ds import run_ds
from components.dms import run_dms
from components.dl import toggle_light
from components.db import toggle_buzzer

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ImportError:
    pass

def menu():
    print("\n" + "="*35)
    print("     PI1 ACTUATOR CONTROL")
    print("="*35)
    print("1 - Turn on Door Light (DL)")
    print("2 - Turn off Door Light (DL)")
    print("3 - Activate Buzzer (DB)")
    print("4 - Deactivate Buzzer (DB)")
    print("x - Exit")
    print("-" * 35)

def run_actuators_logic(pi1_settings):
    while True:
        menu()
        choice = input("Enter command: ").strip().lower()
        if choice == '1':
            toggle_light(pi1_settings['DL'], 1)
        elif choice == '2':
            toggle_light(pi1_settings['DL'], 0)
        elif choice == '3':
            toggle_buzzer(pi1_settings['DB'], 1)
        elif choice == '4':
            toggle_buzzer(pi1_settings['DB'], 0)
        elif choice == 'x':
            break
        else:
            print("Unknown option.")

if __name__ == "__main__":
    args = sys.argv[1:]
    print(args)

    settings = load_settings()
    pi1_settings = settings['PI1']
    threads = []
    stop_event = threading.Event()

    if not args or ( '--sensors' not in args and '--actuators' not in args):
        print("Please specify --sensors, --actuators, or both.")
    else:
        try:
            if '--sensors' in args:
                print("Starting sensor monitoring...")
                run_ds(pi1_settings['DS1'], threads, stop_event)
                run_dus(pi1_settings['DUS1'], threads, stop_event)
                run_pir(pi1_settings['DPIR1'], threads, stop_event)
                run_dms(pi1_settings['DMS'], threads, stop_event)

            if '--actuators' in args:
                run_actuators_logic(pi1_settings)
            else:
                while True:
                    time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping application...")
        finally:
            stop_event.set()
            for t in threads:
                t.join(timeout=1)
            try:
                GPIO.cleanup()
            except:
                pass
            print("Application shut down.")