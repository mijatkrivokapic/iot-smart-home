from .dht import handle_dht
from .ds1 import handle_ds1
from .ir import handle_ir
from .pir import handle_dpir1
from .btn import handle_btn
from .gyro import handle_accel, handle_gyro

SENSOR_RULES = {
    "DPIR1": handle_dpir1,
    "IR": handle_ir,
    "DHT1": handle_dht,
    "DHT2": handle_dht,
    "DS1": handle_ds1,
    "BTN": handle_btn,
    "GSG_Accel": handle_accel,
    "GSG_Gyro": handle_gyro
}

def process_automation_rules(payload):
    sensor_name = payload.get("sensor")
    
    if sensor_name in SENSOR_RULES:
        handler_function = SENSOR_RULES[sensor_name]
        handler_function(payload)