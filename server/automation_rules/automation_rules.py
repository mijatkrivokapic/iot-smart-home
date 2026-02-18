from automation_rules.pir import handle_dpir1
from automation_rules.ds1 import handle_ds1

SENSOR_RULES = {
    "DPIR1": handle_dpir1,
    "DS1": handle_ds1
}

def process_automation_rules(payload):
    sensor_name = payload.get("sensor")
    
    if sensor_name in SENSOR_RULES:
        handler_function = SENSOR_RULES[sensor_name]
        handler_function(payload)