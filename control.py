from machine import RTC, Pin, Timer, WDT
import config
import sensors

class Device:
    def __init__(self, data, controller):
        self.pin = Pin(int(data["pin"]), Pin.OUT, value=1)
        self.controller = controller
        self.data = data
        self.name = data["name"]
    def run(self):
        self.controller(self)

__devices__ = []
__timer__ = None
__wdt__ = None

def is_it_daytime():
    daytime_start = config.get('daytimeStart')
    daytime_end = config.get('daytimeEnd')
    return cmp_time_with_now(daytime_start) < 0 < cmp_time_with_now(daytime_end)

def run(t):
    global __devices__
    for device in __devices__:
        device.run()
    __wdt__.feed()

# def control_airpump():
#     global __airpump_pin__
#     limit = float(config.get("airPumpWorktimePercentage"))*10
#     now = RTC().datetime()
#     minutes = now[-3]%10 + float(now[-2])/60
#     if(minutes <= limit):
#         __airpump_pin__.low()
#     else:
#         __airpump_pin__.high()


def cmp_time_with_now(time):
    now = RTC().datetime()
    pairs = zip(now[-len(time):], time)
    for n, t in pairs:
        if t > n:
            return 1
        elif t < n:
            return -1
    return 0

def init_devices():
    global __devices__
    for device_data in config.get("devices"):
        controller = get_device_controller(device_data["controller"])
        __devices__.append(Device(device_data, controller))

def on_controller(device):
    device.pin.low()

def off_controller(device):
    device.pin.high()

def daytime_controller(device):
    if is_it_daytime():
        device.pin.low()
    else:
        device.pin.high()

def door_controller(device):
    if sensors.is_door_open():
        device.pin.low()
    else:
        device.pin.high()

def get_device_controller(name):
    if(name == "on"):
        return on_controller
    elif(name == "off"):
        return off_controller
    elif(name == "day"):
        return daytime_controller
    elif (name == "door"):
        return door_controller
    else:
        return off_controller



def start(timer):
    global __timer__, __wdt__
    __timer__ = timer
    init_devices()
    __wdt__ = WDT()
    __timer__.init(period=300, mode=Timer.PERIODIC, callback=run)

