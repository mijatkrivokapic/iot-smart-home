from .dht import handle_dht
from .dms import handle_dms
from .ds1 import handle_ds1
from .ir import handle_ir
from .pir import handle_dpir1

SENSOR_RULES = {
    "DPIR1": handle_dpir1,
    "IR": handle_ir,
    "DHT1": handle_dht,
    "DHT2": handle_dht,
    "DS1": handle_ds1,
    "DMS": handle_dms
}

def process_automation_rules(payload):
    sensor_name = payload.get("sensor")
    
    if sensor_name in SENSOR_RULES:
        handler_function = SENSOR_RULES[sensor_name]
        handler_function(payload)