try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
import time
import threading
import json
from mqtt_wrapper import send_measurement
from components.timer_state import TimerState

_timer_instance = None
_display_instance = None

class FourSegmentDisplay:
    def __init__(self, settings):
        self.settings = settings
        self.current_display_string = "0000"
        self.is_blinking = False
        self.blink_state = True
        self.last_blink_time = time.time()
        self.last_printed_value = ""
        
        if not self.settings['simulated']:
            self._setup_gpio()
        
        self.display_thread = threading.Thread(target=self._update_display_loop, daemon=True)
        self.display_thread.start()

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        self.segments = self.settings['segment_pins']
        self.digits = self.settings['digit_pins']
        for seg in self.segments:
            GPIO.setup(seg, GPIO.OUT)
            GPIO.output(seg, 0)
        for dig in self.digits:
            GPIO.setup(dig, GPIO.OUT)
            GPIO.output(dig, 1)
        self.num_map = {
            ' ': (0,0,0,0,0,0,0), '0': (1,1,1,1,1,1,0), '1': (0,1,1,0,0,0,0),
            '2': (1,1,0,1,1,0,1), '3': (1,1,1,1,0,0,1), '4': (0,1,1,0,0,1,1),
            '5': (1,0,1,1,0,1,1), '6': (1,0,1,1,1,1,1), '7': (1,1,1,0,0,0,0),
            '8': (1,1,1,1,1,1,1), '9': (1,1,1,1,0,1,1)
        }

    def update_callback(self, state):
        mins, secs = divmod(state['current_time'], 60)
        self.current_display_string = f"{mins:02d}{secs:02d}"
        self.is_blinking = state['is_blinking']
       
        send_measurement(self.settings['topic'], json.dumps(state), self.settings['component'], 
                         self.settings['device'], is_simulated=self.settings['simulated'])

    def _update_display_loop(self):
        while True:
            if self.is_blinking:
                if time.time() - self.last_blink_time > 0.5:
                    self.blink_state = not self.blink_state
                    self.last_blink_time = time.time()
                display_val = "00:00" if self.blink_state else "     "
            else:
                display_val = f"{self.current_display_string[:2]}:{self.current_display_string[2:]}"

            if self.settings['simulated']:
                if display_val != self.last_printed_value:
                    print(f"[4SD SIMULATION]: {display_val}")
                    self.last_printed_value = display_val
                time.sleep(0.1)
            else:
                self._refresh_physical_display(display_val.replace(":", ""))

    def _refresh_physical_display(self, s):
        for i in range(4):
            char = s[i]
            segments_values = self.num_map.get(char, self.num_map[' '])
            for seg_idx in range(7):
                GPIO.output(self.segments[seg_idx], segments_values[seg_idx])
            
            GPIO.output(25, 1 if (i == 1 and int(time.time()) % 2 == 0) else 0)

            GPIO.output(self.digits[i], 0)
            time.sleep(0.002)
            GPIO.output(self.digits[i], 1)

def run_4sd(settings):
    global _timer_instance, _display_instance
    _display_instance = FourSegmentDisplay(settings)
    _timer_instance = TimerState(update_callback=_display_instance.update_callback)

def handle_4sd_message(payload):
    global _timer_instance
    if _timer_instance:
        try:
            if payload.get("action") == "add_time":
                _timer_instance.add_time(int(payload.get("value", 0)))
            
            if payload.get("action") == "start_timer":
                 _timer_instance.start_timer(int(payload.get("value", 0)))

        except Exception as e:
            print(f"Error in 4SD handle_4sd_message: {e}")