import threading
import time

class TimerState:
    def __init__(self, update_callback=None):
        self.current_time = 0
        self.is_blinking = False
        self.is_running = False
        
        self.lock = threading.Lock()
        self.update_callback = update_callback
        
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        while True:
            time.sleep(1)
            trigger_update = False
            
            with self.lock:
                if self.is_running and self.current_time > 0:
                    self.current_time -= 1
                    trigger_update = True
                    
                    if self.current_time == 0:
                        self.is_running = False
                        self.is_blinking = True
                
                if self.is_blinking:
                    trigger_update = True

            if trigger_update and self.update_callback:
                self.update_callback(self.get_state())

    def start_timer(self, seconds):
        with self.lock:
            self.current_time = max(0, seconds)
            self.is_running = self.current_time > 0
            self.is_blinking = False
        self._notify()

    def add_time(self, seconds):
        with self.lock:
            if self.is_blinking:
                self.is_blinking = False
                self.is_running = False
                self.current_time = 0
            
            elif self.is_running:
                self.current_time += seconds
                self.is_running = True
                self.is_blinking = False
        self._notify()

    def get_state(self):
        with self.lock:
            return {
                "current_time": self.current_time,
                "is_blinking": self.is_blinking,
                "is_running": self.is_running,
            }

    def _notify(self):
        if self.update_callback:
            self.update_callback(self.get_state())