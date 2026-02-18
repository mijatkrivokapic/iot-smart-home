from automation_rules.pir import handle_dpir1

from .ir import handle_ir

SENSOR_RULES = {
    "DPIR1": handle_dpir1,
    "IR": handle_ir
}

def process_automation_rules(payload):
    sensor_name = payload.get("sensor")
    
    if sensor_name in SENSOR_RULES:
        handler_function = SENSOR_RULES[sensor_name]
        print("calling handlesr function for", sensor_name)
        handler_function(payload)