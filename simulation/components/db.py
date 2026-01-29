def toggle_buzzer(settings, state):
    if settings['simulated']:
        print(f"SIMULATOR: Door Buzzer is now {'ON' if state else 'OFF'}")
    else:
        pass #TODO : implement real actuator logic