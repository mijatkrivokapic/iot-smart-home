from components.dl import handle_dl
from components.db import handle_db

ACTUATOR_RULES = {
    "DL": handle_dl,
    "DB": handle_db
}

def actuator_callback(payload):
    actuator_name = payload.get("actuator")
    
    if actuator_name in ACTUATOR_RULES:
        handler_function = ACTUATOR_RULES[actuator_name]
        handler_function(payload)