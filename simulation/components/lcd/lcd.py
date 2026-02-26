import threading
import time

from mqtt_wrapper import send_measurement

from .Adafruit_LCD1602 import Adafruit_CharLCD
from .PCF8574 import PCF8574_GPIO

sensor_data = {}
sensor_data_lock = threading.Lock()


def lcd_display_loop(delay, stop_event, settings):
    while not stop_event.is_set():
        with sensor_data_lock:
            data_copy = dict(sensor_data)
        if settings['simulated']:
            if not data_copy:
                print("=" * 20)
                print(f"Timestamp: {time.strftime('%H:%M:%S', time.localtime())}")
                print(f"Actuator: {settings['component']}")
                print(f"No DHT data")
                send_measurement(
                    settings['topic'],
                    'No DHT data',
                    settings['component'],
                    settings['device'],
                    is_simulated=True,
                )
                time.sleep(delay)
            else:
                for sensor, data in data_copy.items():
                    print("=" * 20)
                    print(f"Timestamp: {time.strftime('%H:%M:%S', time.localtime())}")
                    print(f"Actuator: {settings['component']}")
                    print(f"{sensor} T:{data['temperature']}C H:{data['humidity']}%")
                    send_measurement(
                        settings['topic'],
                        f"{sensor} T:{data['temperature']}C H:{data['humidity']}%",
                        settings['component'],
                        settings['device'],
                        is_simulated=True,
                    )
                    time.sleep(delay)
        else:
            # LCD setup
            PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
            PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
            # Create PCF8574 GPIO adapter.
            try:
                mcp = PCF8574_GPIO(PCF8574_address)
            except:
                try:
                    mcp = PCF8574_GPIO(PCF8574A_address)
                except:
                    print('I2C Address Error !')
                    exit(1)
            # Create LCD, passing in MCP GPIO adapter.
            lcd = Adafruit_CharLCD(
                settings['pins']['rs'],
                settings['pins']['e'],
                settings['pins']['db'],
                mcp,
            )

            mcp.output(3, 1)  # Turn on LCD backlight
            lcd.begin(16, 2)

            if not data_copy:
                lcd.setCursor(0, 0)
                lcd.message('No DHT data')
                lcd.setCursor(0, 1)
                lcd.message('')
                send_measurement(
                    settings['topic'],
                    'No DHT data',
                    settings['component'],
                    settings['device'],
                    is_simulated=False,
                )
                time.sleep(delay)
            else:
                for sensor, data in data_copy.items():
                    # lcd.clear()
                    lcd.setCursor(0, 0)
                    lcd.message(f"{sensor}")
                    lcd.setCursor(0, 1)
                    lcd.message(f" T:{data['temperature']}C H:{data['humidity']}%")
                    send_measurement(
                        settings['topic'],
                        f"{sensor} T:{data['temperature']}C H:{data['humidity']}%",
                        settings['component'],
                        settings['device'],
                        is_simulated=False,
                    )
                    time.sleep(delay)
    else:
        if not settings['simulated']:
            lcd.clear()


def run_lcd(settings, threads, stop_event):
    print("Starting LCD component")
    lcd_thread = threading.Thread(
        target=lcd_display_loop, args=(2, stop_event, settings)
    )
    lcd_thread.start()
    threads.append(lcd_thread)


def handle_lcd(payload):
    action = payload.get('action')
    sensor = action.get('sensor', 'Unknown')
    temperature = action.get('temperature')
    humidity = action.get('humidity')

    if temperature is None or humidity is None:
        return

    with sensor_data_lock:
        sensor_data[sensor] = {'temperature': temperature, 'humidity': humidity}
