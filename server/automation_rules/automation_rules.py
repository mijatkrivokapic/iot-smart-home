from .btn import handle_btn
from .dht import handle_dht
from .dms import handle_dms
from .ds import handle_ds
from .dus import handle_dus
from .gyro import handle_accel, handle_gyro
from .ir import handle_ir
from .pir import handle_pir
from .ds1 import handle_ds1
from .ds2 import handle_ds2

SENSOR_RULES = {
    "DPIR1": [handle_pir],
    "DPIR2": [handle_pir],
    "IR": [handle_ir],
    "DHT1": [handle_dht],
    "DHT2": [handle_dht],
    "DS1": [handle_ds, handle_ds1],
    "DS2": [handle_ds, handle_ds2],
    "DMS": [handle_dms],
    "DUS1": [handle_dus],
    "DUS2": [handle_dus],
    "BTN": [handle_btn],
    "GSG_Accel": [handle_accel],
    "GSG_Gyro": [handle_gyro],
}


def process_automation_rules(payload):
    sensor_name = payload.get("sensor")

    if sensor_name in SENSOR_RULES:
        handler_functions = SENSOR_RULES[sensor_name]
        for handler in handler_functions:
            handler(payload)
