def toggle_light(settings, state):
    if settings['simulated']:
        print(f"SIMULATOR: Door Light is now {'ON' if state else 'OFF'}")
    else:
        pass #TODO : implement real actuator logic