from pynrfjprog.API import DeviceFamily
from pynrfjprog.API import API
from app.nrf import _nrf_api_call

class NrfDeviceInfo:
    def __init__(self, _nrf_version, _version, _name, _memory, _revision):
        self.version = _version
        self.name = _name
        self.memory = _memory
        self.revision = _revision
        self.nrf_version = _nrf_version

    def __repr__(self):
        return f"{self.nrf_version} #{self.name} v{self.version}"

class NrfConnector:
    def __init__(self, _device_family):
        self.device_family = _device_family
        self.api = API(self.device_family)
        self._device_info = None
    
    @property
    def device_info(self):
        return self._device_info


    def open(self):
        self.api.open()
    
    def close(self):
        self.api.close()

    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    def get_connected_devices(self):
        return self.api.enum_emu_snr()

    @_nrf_api_call(on_fail_message="Failed to connect to device")
    def connect_to_device(self, device):
        if device is None:
            self.api.connect_to_emu_without_snr()
        else:
            self.api.connect_to_emu_with_snr(device)

    @_nrf_api_call(on_fail_message="Failed to read device info.")
    def read_device_info(self):
        version, _name, _memory, _revision = self.api.read_device_info()
        device_version = self.api.read_device_version()
        self._device_info = NrfDeviceInfo(device_version, version, _name, _memory, _revision)
       
    