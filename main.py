import utime
import machine
from machine import Timer, Pin, RTC
import time
import ntptime
import micropython
import config
import control
import mqtt_reporting

def set_ntp_time(timer):
    ntptime.host = "tempus1.gum.gov.pl"
    for i in range(1,10):
        try:
            t = ntptime.time()
            tm = utime.localtime(t)
            tm = tm[0:3] + (0,) + tm[3:6] + (0,)
            RTC().datetime(tm)
            break
        except OSError:
            continue

# def init_modules():
# config.init()

micropython.alloc_emergency_exception_buf(500)

machine.freq(160000000)

timer = Timer(-1)
timer.init(period=300*1000, mode=Timer.PERIODIC, callback=set_ntp_time)
set_ntp_time(None)
control.start(timer)
mqtt_reporting.setup()

print("\nGROWBOX INIT COMPLETE!")

while True:
    mqtt_reporting.run()
    time.sleep_ms(60*1000)