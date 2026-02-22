import sys
import threading
import time

from components.actuator_callback import actuator_callback
from components.db import toggle_buzzer
from components.dht import run_dht
from components.dl import toggle_light
from components.dms import run_dms
from components.ds import run_ds
from components.dus import run_dus
from components.gyro import run_gyro
from components.ir import run_ir
from components.lcd.lcd import run_lcd
from components.pir import run_pir
from mqtt_wrapper import get_mqtt_client, init_mqtt_client
from settings import load_settings
from components.four_segment_display import run_4sd
from components.btn import run_btn

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
    pi_ids = {'--1': 'PI1', '--2': 'PI2', '--3': 'PI3'}
    pi_id = pi_ids.get(args[0], 'PI1') if args else 'PI1'

    settings = load_settings()
    pi1_settings = settings['PI1']
    pi2_settings = settings['PI2']
    pi3_settings = settings['PI3']
    mqtt_settings = settings.get('MQTT', {})
    
    threads = []
    stop_event = threading.Event()
    
    # Initialize MQTT Client
    mqtt_client = init_mqtt_client(
        broker=mqtt_settings.get('broker', 'localhost'),
        port=mqtt_settings.get('port', 1883),
        command_topic=f'home/actuators/{pi_id}/+',
        command_callback=actuator_callback,
        batch_size=mqtt_settings.get('batch_size', 5),
        batch_timeout=mqtt_settings.get('batch_timeout', 5)
    )
    print("MQTT Client initialized")

    if not args or ( '--sensors' not in args and '--actuators' not in args):
        print("Please specify --sensors, --actuators, or both.")
    else:
        try:
            if args[0] == '--1':
                print("Running in PI1 mode")
                if '--sensors' in args:
                    print("Starting pi1 sensor monitoring...")
                    # run_ds(pi1_settings['DS1'], threads, stop_event)
                    run_dus(pi1_settings['DUS1'], threads, stop_event)
                    run_pir(pi1_settings['DPIR1'], threads, stop_event)
                    # run_dms(pi1_settings['DMS'], threads, stop_event)

                if '--actuators' in args:
                    run_actuators_logic(pi1_settings)
                else:
                    while True:
                        time.sleep(1)
            elif args[0] == '--2':
                print("Running in PI2 mode")
                if '--sensors' in args:
                    print("Starting pi2 sensor monitoring...")
                    #run_ds(pi2_settings['DS2'], threads, stop_event)
                    #run_dus(pi2_settings['DUS2'], threads, stop_event)
                    #run_pir(pi2_settings['DPIR2'], threads, stop_event)
                    run_btn(pi2_settings['BTN'], threads, stop_event)
                    #run_dht(pi2_settings['DHT3'], threads, stop_event)
                    #run_gyro(pi2_settings['GSG'], threads, stop_event)
                    run_4sd(pi2_settings['4SD'])
                    
                if '--actuators' in args:
                    run_actuators_logic(pi1_settings)
                else:
                    while True:
                        time.sleep(1)

            
            elif args[0] == '--3':
                print("Running in PI3 mode")
                if '--sensors' in args:
                    print("Starting pi3 sensor monitoring...")
                    run_dht(pi3_settings['DHT1'], threads, stop_event)
                    run_dht(pi3_settings['DHT2'], threads, stop_event)
                    run_ir(pi3_settings['IR'], threads, stop_event)
                    run_pir(pi3_settings['DPIR3'], threads, stop_event)
                    run_lcd(pi3_settings['LCD'], threads, stop_event)
                    
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
            
            mqtt_client = get_mqtt_client()
            if mqtt_client:
                mqtt_client.stop()
            
            try:
                GPIO.cleanup()
            except:
                pass
            print("Application shut down.")