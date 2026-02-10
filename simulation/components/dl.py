from mqtt_publisher import send_measurement


def toggle_light(settings, state):
    if settings['simulated']:
        print(f"SIMULATOR: Door Light is now {'ON' if state else 'OFF'}")
        topic = settings['topic']
        send_measurement(topic, 1 if state else 0, "DL", settings['device'], is_simulated=settings['simulated'])
    else:
        pass #TODO : implement real actuator logic