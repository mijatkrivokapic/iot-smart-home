import json
import time
import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client()

def init_mqtt(broker, port):
    """
    Connects the global MQTT client to the broker.
    """
    try:
        mqtt_client.connect(broker, port, keepalive=60)
        mqtt_client.loop_start()
        print("✓ MQTT client initialized")
        return True
    except Exception as e:
        print(f"✗ MQTT connection error: {e}")
        return False

def send_actuator_command(pi_id, actuator_id, action, value=None):
    """
    Sends a command to an actuator.
    Import this function in your automation rules (e.g., pir.py).
    """
    print("⚡ Sending command to actuator...")
    topic = f"home/actuators/{actuator_id}"
    payload = {
        "actuator": actuator_id,
        "action": action,
        "value": value,
        "timestamp": time.time()
    }
    
    try:
        if mqtt_client.is_connected():
            mqtt_client.publish(topic, json.dumps(payload), qos=1)
            print(f"⚡ Action: sent {action} on {actuator_id} (PI: {pi_id})")
        else:
            print("⚠ Cannot send command: MQTT not connected")
            
    except Exception as e:
        print(f"✗ Error sending command: {e}")