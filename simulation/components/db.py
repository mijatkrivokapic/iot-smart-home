from mqtt_publisher import send_measurement


def toggle_buzzer(settings, state):
    if settings['simulated']:
        print(f"SIMULATOR: Door Buzzer is now {'ON' if state else 'OFF'}")
        topic = settings['topic']
        send_measurement(topic, 1 if state else 0, "DB", settings['device'], is_simulated=settings['simulated'])
    else:
        pass #TODO : implement real actuator logic