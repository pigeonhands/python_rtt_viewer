import time


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.stop_time = None

    @property
    def elapsed_ms(self):
        if self.start_time is None:
            return 0
        
        if self.stop_time is None:
            return round((time.time() - self.start_time) * 1000, 1)
        
        return round((self.stop_time - self.start_time) * 1000, 1)

    @property
    def running(self):
        return self.start_time is not None and self.stop_time is None

    def start(self):
        self.start_time = time.time()
        self.stop_time = None
    
    def stop(self):
        self.stop_time = time.time()
