from app.nrf.nrf_connector import NrfConnector
from app.nrf import _nrf_api_call
import time

class NrfRtt:
    def __init__(self, _c=NrfConnector):
        self.api = _c.api
        self._lines = []

    @_nrf_api_call(on_fail_message="Failed to read rtt.")
    def _get_lines(self):
        data = self.api.rtt_read(0, 2048).rstrip()
        self._lines = []
        for line in data.splitlines():
            stripped = line.strip()
            if len(stripped) > 0:
                self._lines.append(stripped)
    
    def lines(self):
        while True:
            if not self._get_lines():
                break
            for line in self._lines:
                yield line
    
    @_nrf_api_call(on_fail_message="Failed to connect rtt client.")
    def connect(self):
        self.api.rtt_start()
        time.sleep(0.5)
        while not self.api.rtt_is_control_block_found():
            self.api.rtt_stop()
            time.sleep(0.1)
            self.api.rtt_start()
            time.sleep(0.5)

