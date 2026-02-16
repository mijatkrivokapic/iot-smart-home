from components.dl import handle_dl

ACTUATOR_RULES = {
    "DL": handle_dl
}

def actuator_callback(payload):
    actuator_name = payload.get("actuator")
    
    if actuator_name in ACTUATOR_RULES:
        handler_function = ACTUATOR_RULES[actuator_name]
        handler_function(payload)