from pynrfjprog.API import DeviceFamily
from app.nrf.nrf_connector import NrfConnector
from app.nrf.nrf_rtt import NrfRtt
from app.utils import list_selection
from app.utils.stopwatch import Stopwatch

import threading
import os
import msvcrt as m
from datetime import datetime

sw = Stopwatch()
timestamp_enaled = False

KNOWN_DEVICES = {}

class Device:
    def __init__(self, _serial):
        self.serial = _serial

    def __repr__(self):
        return "{} {}".format(self.serial, KNOWN_DEVICES.get(str(self.serial), ''))

def load_known_devices():
    try:
        global KNOWN_DEVICES
        import json
        with open("devices.json") as f:
            KNOWN_DEVICES = json.load(f)
    except:
        pass

def get_device(devices):
    if devices is None or len(devices) == 0:
        return None
    if len(devices) == 1:
        return devices[0]
    print("Please select a device")

    return list_selection(devices)

def to_console(*args):
    prefix = ""
    if timestamp_enaled:
        prefix = datetime.now().strftime("%H:%M:%S")
        print("{:<10}{}".format(prefix, ' '.join(args)))
    else:
        print(*args)
    

def process_commands():
    while True:
        c = str(m.getch(), encoding='utf-8')
        if c == 'c':
            os.system('cls')

        if c == 's': #stopwatch
            if sw.running:
                sw.stop()
                to_console(">Stopwatch stopped. {}ms elapsed".format(sw.elapsed_ms))
            else:
                sw.start()
                to_console(">Stopwatch started")
        
        if c == 't':
            global timestamp_enaled
            timestamp_enaled = not timestamp_enaled

def app_main(c):
    connected_devices = [Device(ser) for ser in c.get_connected_devices()]
    selected_device =  get_device(connected_devices)

    if selected_device is None:
        print("No devices connected.")
        return
    
    if  not c.connect_to_device(selected_device.serial):
        return
    if not c.read_device_info():
        return
    
    print("Connected to device -", selected_device)
    print(c.device_info)
    print()
    rtt = NrfRtt(c)

    print("Waiting for rtt...")
    if not rtt.connect():
        return
    print("Connected to rtt!")
    
    t = threading.Thread(target=process_commands)
    t.start()

    for line in rtt.lines():
        to_console(line)
    

def run(device_family=DeviceFamily.NRF52):
    load_known_devices()
    with NrfConnector(device_family) as c:
        app_main(c)
    print("Press enter to exit.")
    input()

