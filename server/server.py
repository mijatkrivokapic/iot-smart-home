import json
import threading
import time
from queue import Queue

import paho.mqtt.client as mqtt
import socketio_helper
from automation_rules.automation_rules import process_automation_rules
from automation_rules.dms import PASSWORD
from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from mqtt_helper import init_mqtt, mqtt_client, send_actuator_command
from system_state import state

app = Flask(__name__)
CORS(app)

INFLUXDB_CONFIG = {
    "url": "http://localhost:8086",
    "token": "B8HDBR5Sh9cCibUUGyUAM2rDL4ajESUs_UyUHpRp52OT3mL1IriRtRCD2cnnix-09BGs1_OU9xv9HMNXnWDSGg==",
    "org": "FTN",
    "bucket": "sensor_data",
}

MQTT_CONFIG = {
    "broker": "localhost",
    "port": 1883,
    "topics": ["home/sensors/+"],  # Subscribe to all home/sensors/* topics
}

# Global state
influxdb_client = None
message_queue = Queue(maxsize=1000)
stop_event = threading.Event()


def init_influxdb():
    """Initialize InfluxDB client."""
    global influxdb_client
    try:
        influxdb_client = InfluxDBClient(
            url=INFLUXDB_CONFIG["url"],
            token=INFLUXDB_CONFIG["token"],
            org=INFLUXDB_CONFIG["org"],
        )
        print("✓ InfluxDB connected")
        return True
    except Exception as e:
        print(f"✗ InfluxDB connection error: {e}")
        return False


def on_mqtt_connect(client, userdata, flags, rc):
    """MQTT on_connect callback."""
    if rc == 0:
        print(
            f"✓ MQTT connected to broker: {MQTT_CONFIG['broker']}:{MQTT_CONFIG['port']}"
        )
        # Subscribe to all sensor topics
        for topic in MQTT_CONFIG["topics"]:
            client.subscribe(topic, qos=1)
            print(f"  → Subscribed to topic: {topic}")
    else:
        print(f"✗ MQTT connection failed with code {rc}")


def on_mqtt_disconnect(client, userdata, rc):
    """MQTT on_disconnect callback."""
    if rc != 0:
        print(f"✗ Unexpected MQTT disconnection (code {rc})")
    else:
        print("✓ MQTT disconnected gracefully")


def on_mqtt_message(client, userdata, msg):
    """MQTT on_message callback - queue messages for batch processing."""
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        message_data = {
            "topic": msg.topic,
            "payload": payload,
            "timestamp": time.time(),
        }

        socketio_helper.socketio.emit(
            f"sensor-data-{payload.get('device', 'Unknown')}", message_data
        )  # , broadcast=True)

        # Non-blocking queue put with timeout
        try:
            message_queue.put(message_data, block=False)
        except:
            print(f"⚠ Message queue full, dropping oldest message")
            try:
                message_queue.get_nowait()
                message_queue.put(message_data, block=False)
            except:
                pass

    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in MQTT message: {e}")
    except Exception as e:
        print(f"✗ Error processing MQTT message: {e}")


def write_to_influxdb(topic, payload):
    """Write sensor data to InfluxDB."""
    if not influxdb_client:
        return

    try:
        sensor_name = payload.get("sensor", "Unknown")
        device_name = payload.get("device", "Unknown")
        value = payload.get("value", 0)
        is_simulated = payload.get("simulated", False)
        timestamp = payload.get("timestamp", time.time())

        if "DHT" in sensor_name:
            point = []
            for k, v in value.items():
                point.append(
                    Point(sensor_name)
                    .tag("sensor", sensor_name)
                    .tag("device", device_name)
                    .tag("topic", topic)
                    .tag("simulated", str(is_simulated))
                    .tag("type", k)  # temperature or humidity
                    .field("value", v)
                    .time(int(timestamp * 1e9))
                )
        elif "alarm" in sensor_name:
            point = (
                Point(sensor_name)
                .tag("sensor", sensor_name)
                .tag("device", device_name)
                .tag("topic", topic)
                .tag("simulated", str(is_simulated))
                .field("value", 1 if value else 0)
                .time(int(timestamp * 1e9))
            )
        else:
            # Create InfluxDB Point
            point = (
                Point(sensor_name)  # measurement name
                .tag("sensor", sensor_name)
                .tag("device", device_name)
                .tag("topic", topic)
                .tag("simulated", str(is_simulated))
                .field("value", value)
                .time(int(timestamp * 1e9))  # nanoseconds
            )

        # Write to InfluxDB
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        write_api.write(
            bucket=INFLUXDB_CONFIG["bucket"], org=INFLUXDB_CONFIG["org"], record=point
        )

        print(
            f"✓ [{sensor_name}] Wrote to InfluxDB: value={value}, simulated={is_simulated}"
        )

    except Exception as e:
        print(f"✗ Error writing to InfluxDB: {e}")


def database_writer_loop():
    """Daemon thread that continuously processes queued messages."""
    print("→ Database writer thread started")

    while not stop_event.is_set():
        try:
            if not message_queue.empty():
                message_data = message_queue.get(timeout=0.1)

                write_to_influxdb(message_data["topic"], message_data["payload"])

                process_automation_rules(message_data["payload"])

            else:
                time.sleep(0.1)

        except Exception as e:
            print(f"✗ Error in database writer loop: {e}")

    print("→ Database writer thread stopped")


def start_database_writer():
    """Start the database writer daemon thread."""
    writer_thread = threading.Thread(target=database_writer_loop, daemon=True)
    writer_thread.start()
    return writer_thread


@app.route('/api/state', methods=['GET'])
def get_system_state():
    try:
        current_state = state.get_all()
        return jsonify(current_state), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/timer/start', methods=['POST'])
def start_timer():
    data = request.get_json()

    timer_seconds = data.get("time")

    send_actuator_command("PI2", "4SD", "start_timer", timer_seconds)

    return jsonify({"status": "success"}), 200


@app.route('/api/timer/config', methods=['PUT'])
def set_timer_increment():
    data = request.get_json()

    timer_seconds = data.get("time")

    state.set_timer_increment(timer_seconds)

    return jsonify({"status": "success"}), 200


@app.route('/api/timer/increment', methods=['POST'])
def increment_timer():

    send_actuator_command("PI2", "4SD", "add_time", state.get("timer_increment"))

    return jsonify({"status": "success"}), 200


@app.route('/api/password', methods=['POST'])
def submit_password():
    try:
        data = request.get_json(force=True, silent=True) or {}
        pw = str(data.get('password', ''))

        if pw != PASSWORD:
            return jsonify({"status": "error", "message": "Invalid password"}), 403

        process_automation_rules({"sensor": "DMS", "value": pw, "simulated": False})

        return jsonify({"status": "ok", "message": "Password accepted"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Initialize connections
    if not init_influxdb():
        print("⚠ Warning: InfluxDB initialization failed, but continuing...")

    # Setup MQTT Callbacks BEFORE connecting
    mqtt_client.on_connect = on_mqtt_connect
    mqtt_client.on_message = on_mqtt_message
    mqtt_client.on_disconnect = on_mqtt_disconnect

    # Initialize MQTT Connection (using helper function)
    if not init_mqtt(MQTT_CONFIG["broker"], MQTT_CONFIG["port"]):
        print("⚠ Warning: MQTT initialization failed, but continuing...")

    # Start database writer daemon thread
    writer_thread = start_database_writer()

    try:
        # Run Flask app
        print("\n" + "=" * 50)
        print("Starting Flask server on http://localhost:5000")
        print("=" * 50)
        socketio_helper.init_socketio(app)
        socketio_helper.socketio.run(app, host='0.0.0.0', port=5000)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        stop_event.set()
        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        if influxdb_client:
            influxdb_client.close()
        print("Server shut down.")
