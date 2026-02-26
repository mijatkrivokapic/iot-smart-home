from .db import handle_db
from .dl import handle_dl
from .lcd.lcd import handle_lcd
from .rgb import handle_rgb
from .four_segment_display import handle_4sd_message

ACTUATOR_RULES = {
    "DL": handle_dl,
    "BRGB": handle_rgb,
    "LCD": handle_lcd,
    "DB": handle_db,
    "4SD": handle_4sd_message
}

def actuator_callback(payload):
    actuator_name = payload.get("actuator")
    
    if actuator_name in ACTUATOR_RULES:
        handler_function = ACTUATOR_RULES[actuator_name]
        handler_function(payload)