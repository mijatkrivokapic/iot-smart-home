from .dl import handle_dl
from .rgb import handle_rgb

ACTUATOR_RULES = {
    "DL": handle_dl,
    "BRGB": handle_rgb
}

def actuator_callback(payload):
    actuator_name = payload.get("actuator")
    
    if actuator_name in ACTUATOR_RULES:
        handler_function = ACTUATOR_RULES[actuator_name]
        handler_function(payload)