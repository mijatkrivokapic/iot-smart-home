import json
import queue
import threading
import time
from collections import defaultdict

import paho.mqtt.client as mqtt


class MQTTClientWrapper:
    """
    Generic MQTT client for batch publishing sensor data AND subscribing to actuator commands.
    """

    def __init__(self, broker, port, command_callback=None, command_topic="home/actuators/+", batch_size=5, batch_timeout=5):
        """
        Args:
            broker: MQTT broker address
            port: MQTT broker port
            command_callback: Function to call when a command is received (func(topic, payload))
            command_topic: MQTT topic to subscribe to for commands
            batch_size: Number of messages before sending batch
            batch_timeout: Maximum time (seconds) before sending partial batch
        """
        self.broker = broker
        self.port = port
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        
        # Command handling
        self.command_callback = command_callback
        self.command_topic = command_topic

        # Per-topic batching queues and locks
        self.batch_queues = defaultdict(queue.Queue)
        self.batch_locks = defaultdict(threading.Lock)
        self.last_send_time = defaultdict(time.time)

        # MQTT client initialization
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_disconnect = self._on_disconnect
        self.mqtt_client.on_message = self._on_message
        
        self.connected = False
        
        # Daemon thread control
        self.stop_event = threading.Event()
        self.daemon_thread = None

        self._connect_mqtt()
        self._start_daemon()

    def _connect_mqtt(self):
        """Connect to MQTT broker."""
        try:
            self.mqtt_client.connect(self.broker, self.port, keepalive=60)
            self.mqtt_client.loop_start()
        except Exception as e:
            print(f"MQTT connection error: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        """MQTT on_connect callback."""
        if rc == 0:
            print(f"MQTT Connected to broker: {self.broker}:{self.port}")
            self.connected = True
            
            # Subscribe to command topic if callback is provided
            if self.command_callback:
                client.subscribe(self.command_topic, qos=1)
                print(f"Subscribed to commands: {self.command_topic}")
        else:
            print(f"MQTT Connection failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """MQTT on_disconnect callback."""
        self.connected = False
        if rc != 0:
            print(f"Unexpected MQTT disconnection (code {rc})")

    def _on_message(self, client, userdata, msg):
        """MQTT on_message callback for incoming commands."""
        try:
            payload = json.loads(msg.payload.decode())
            
            if self.command_callback:
                # Run callback in a separate thread to avoid blocking the MQTT loop
                threading.Thread(
                    target=self.command_callback, 
                    args=(payload,),
                    daemon=True
                ).start()
                
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON on topic {msg.topic}")
        except Exception as e:
            print(f"Error processing incoming message: {e}")

    def _start_daemon(self):
        """Start daemon thread for batch message processing."""
        self.daemon_thread = threading.Thread(target=self._batch_sender_loop, daemon=True)
        self.daemon_thread.start()

    def send_measurement(self, topic, value, sensor_name, device_name, is_simulated=True):
        """
        Queue a measurement for batch sending (non-blocking).
        """
        message = {
            "topic": topic,
            "value": value,
            "sensor_name": sensor_name,
            "device_name": device_name,
            "simulated": is_simulated,
            "timestamp": time.time()
        }

        with self.batch_locks[topic]:
            self.batch_queues[topic].put(message)

    def _batch_sender_loop(self):
        """
        Daemon thread that continuously processes and sends batched messages.
        """
        while not self.stop_event.is_set():
            current_time = time.time()
            topics_to_process = list(self.batch_queues.keys())

            for topic in topics_to_process:
                with self.batch_locks[topic]:
                    queue_size = self.batch_queues[topic].qsize()
                    should_send = (
                        queue_size >= self.batch_size or
                        (queue_size > 0 and
                         current_time - self.last_send_time[topic] >= self.batch_timeout)
                    )

                    if should_send:
                        batch = []
                        try:
                            while len(batch) < self.batch_size and not self.batch_queues[topic].empty():
                                batch.append(self.batch_queues[topic].get_nowait())
                        except queue.Empty:
                            pass

                        if batch:
                            self._send_batch(topic, batch)
                            self.last_send_time[topic] = current_time

            time.sleep(0.1)

    def _send_batch(self, topic, batch):
        """Send batch of messages to MQTT topic."""
        if not self.connected:
            return

        try:
            for message in batch:
                payload = json.dumps({
                    "sensor": message["sensor_name"],
                    "device": message["device_name"],
                    "value": message["value"],
                    "simulated": message["simulated"],
                    "timestamp": message["timestamp"]
                })
                self.mqtt_client.publish(topic, payload, qos=1)
        except Exception as e:
            print(f"Error sending batch to topic {topic}: {e}")

    def stop(self):
        """Gracefully stop the client."""
        print("Stopping MQTT client...")
        self.stop_event.set()
        if self.daemon_thread:
            self.daemon_thread.join(timeout=5)
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        print("MQTT client stopped")


# --- GLOBAL STATE & HELPER FUNCTIONS ---

_mqtt_client_instance = None


def init_mqtt_client(broker, port, command_callback=None, command_topic="home/actuators/+", batch_size=5, batch_timeout=5):
    """Initialize global MQTT client instance."""
    global _mqtt_client_instance
    _mqtt_client_instance = MQTTClientWrapper(
        broker, port, command_callback, command_topic, batch_size, batch_timeout
    )
    return _mqtt_client_instance


def get_mqtt_client():
    """Get the global MQTT client instance."""
    return _mqtt_client_instance


def send_measurement(topic, value, sensor_name, device_name, is_simulated=True):
    """Send a measurement through the global MQTT client."""
    if _mqtt_client_instance:
        _mqtt_client_instance.send_measurement(topic, value, sensor_name, device_name, is_simulated)
    else:
        print("Warning: MQTT Client not initialized. Data dropped.")