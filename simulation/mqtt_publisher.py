import threading
import queue
import json
import time
import paho.mqtt.client as mqtt
from collections import defaultdict


class MQTTBatchPublisher:
    """
    Generic MQTT publisher with batch-based message sending via daemon thread.
    Minimizes mutex locking by using queues.
    """
    
    def __init__(self, broker, port, batch_size=5, batch_timeout=5):
        """
        Initialize MQTT publisher with batch configuration.
        
        Args:
            broker: MQTT broker address
            port: MQTT broker port
            batch_size: Number of messages before sending batch
            batch_timeout: Maximum time (seconds) before sending partial batch
        """
        self.broker = broker
        self.port = port
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        
        # Per-topic batching queues and locks (only for queue access)
        self.batch_queues = defaultdict(queue.Queue)
        self.batch_locks = defaultdict(threading.Lock)
        self.last_send_time = defaultdict(time.time)
        
        # MQTT client initialization
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_disconnect = self._on_disconnect
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
        else:
            print(f"MQTT Connection failed with code {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """MQTT on_disconnect callback."""
        self.connected = False
        if rc != 0:
            print(f"Unexpected MQTT disconnection (code {rc})")
    
    def _start_daemon(self):
        """Start daemon thread for batch message processing."""
        self.daemon_thread = threading.Thread(target=self._batch_sender_loop, daemon=True)
        self.daemon_thread.start()
    
    def send_measurement(self, topic, value, sensor_name, is_simulated=True):
        """
        Queue a measurement for batch sending (non-blocking).
        
        Args:
            topic: MQTT topic
            value: Sensor measurement value
            sensor_name: Name of the sensor
            is_simulated: Whether value is simulated or real
        """
        message = {
            "topic": topic,
            "value": value,
            "sensor_name": sensor_name,
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
            
            time.sleep(0.1)  # Short sleep to avoid busy waiting
    
    def _send_batch(self, topic, batch):
        """Send batch of messages to MQTT topic."""
        if not self.connected:
            print(f"MQTT not connected. Dropping batch for topic {topic}")
            return
        
        try:
            for message in batch:
                payload = json.dumps({
                    "sensor": message["sensor_name"],
                    "value": message["value"],
                    "simulated": message["simulated"],
                    "timestamp": message["timestamp"]
                })
                self.mqtt_client.publish(topic, payload, qos=1)
            
            print(f"[MQTT] Sent batch of {len(batch)} messages to topic '{topic}'")
        except Exception as e:
            print(f"Error sending batch to topic {topic}: {e}")
    
    def stop(self):
        """Gracefully stop the publisher daemon."""
        print("Stopping MQTT publisher...")
        self.stop_event.set()
        if self.daemon_thread:
            self.daemon_thread.join(timeout=5)
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        print("MQTT publisher stopped")


# Global publisher instance
_mqtt_publisher = None


def init_mqtt_publisher(broker, port, batch_size=5, batch_timeout=5):
    """Initialize global MQTT publisher instance."""
    global _mqtt_publisher
    _mqtt_publisher = MQTTBatchPublisher(broker, port, batch_size, batch_timeout)
    return _mqtt_publisher


def get_mqtt_publisher():
    """Get the global MQTT publisher instance."""
    return _mqtt_publisher


def send_measurement(topic, value, sensor_name, is_simulated=True):
    """Send a measurement through the global MQTT publisher."""
    if _mqtt_publisher:
        _mqtt_publisher.send_measurement(topic, value, sensor_name, is_simulated)
