import threading
import time

from mqtt_wrapper import send_measurement


def ir_callback(button_name, sensor_config):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: {sensor_config['component']}")
    print(f"Button: {button_name}")

    topic = sensor_config.get('topic', 'home/ir')
    send_measurement(topic, button_name, sensor_config['component'], sensor_config['device'], is_simulated=sensor_config['simulated'])

def run_ir(settings, threads, stop_event):
    if settings['simulated']:
        from simulators.ir import run_ir_simulator
        print("Starting IR simulator")
        ir_thread = threading.Thread(
            target=run_ir_simulator,
            args=(2, ir_callback, stop_event, settings)
        )
        ir_thread.start()
        threads.append(ir_thread)
    else:
        from sensors.ir import run_ir_sensor
        print("Starting IR sensor")
        ir_thread = threading.Thread(
            target=run_ir_sensor,
            args=(0.2, ir_callback, stop_event, settings)
        )
        ir_thread.start()
        threads.append(ir_thread)