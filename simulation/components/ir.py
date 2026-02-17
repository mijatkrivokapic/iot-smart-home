import threading
import time

from mqtt_wrapper import send_measurement


def ir_callback(button_name, sensor_config):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Sensor: IR (Infrared)")
    print(f"Button: {button_name:.2f}")

    # Send measurement to MQTT
    topic = sensor_config.get('topic', 'home/ir')
    send_measurement(topic, button_name, "IR", sensor_config['device'], is_simulated=sensor_config['simulated'])

def run_ir(settings, threads, stop_event):
    if settings['simulated']:
        # print("Starting IR simulator")
        # from simulators.ir import run_ir_simulator
        # ir_thread = threading.Thread(
        #     target=run_ir_simulator,
        #     args=(2, stop_event, settings)
        # )
        # ir_thread.start()
        # threads.append(ir_thread)
        pass
    else:
        from sensors.ir import run_ir_sensor
        print("Starting IR sensor")
        ir_thread = threading.Thread(
            target=run_ir_sensor,
            args=(2, ir_callback, stop_event, settings)
        )
        ir_thread.start()
        threads.append(ir_thread)