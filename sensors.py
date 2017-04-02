from machine import Pin
import time
import dht
import onewire
import ds18x20

import config

__dht22_last_measurement_time__ = 0
__dht22__ = None
__ds18x20__ = None
__ds18x20_last_measurement_time__ = 0
__ds18x20_last_temperature__ = None
__measurement_interval__ = 5000 #in ms

def is_door_open():
    if not door_sensor_set():
        print("No door sensor pin set")
    else:
        pin = Pin(int(config.get('sensors.door')), Pin.IN)
        return (pin.value() == 0)

def door_sensor_set():
    return config.exists('sensors.door')

def dht22_measure_if_needed():
    global __dht22_last_measurement_time__, __measurement_interval__, __dht22__
    if time.ticks_ms() > __dht22_last_measurement_time__+__measurement_interval__:
        __dht22__.measure()
        __dht22_last_measurement_time__ = time.ticks_ms()

def dht22_present():
    return (__dht22__ is not None)

def dht22_temperature():
    global __dht22__
    dht22_measure_if_needed()
    return __dht22__.temperature()

def ds18x20_measure_if_needed():
    global __ds18x20_last_measurement_time__, __measurement_interval__, __ds18x20__, __ds18x20_last_temperature__
    if time.ticks_ms() > __ds18x20_last_measurement_time__+__measurement_interval__:
        roms = __ds18x20__.scan()
        __ds18x20__.convert_temp()
        time.sleep_ms(750)
        __ds18x20_last_temperature__ = __ds18x20__.read_temp(roms[0])
        __ds18x20_last_measurement_time__ = time.ticks_ms()

def ds18x20_temperature():
    global __ds18x20_last_temperature__
    ds18x20_measure_if_needed()
    return __ds18x20_last_temperature__

def ds18x20_present():
    return (__ds18x20__ is not None)

def temperature():
    global __dht22__
    if dht22_present():
        return dht22_temperature()
    elif ds18x20_present():
        return ds18x20_temperature()
    else:
        return None

def humidity():
    global __dht22__
    if dht22_present():
        dht22_measure_if_needed()
        return __dht22__.humidity()
    else:
        return None

def init():
    global __dht22__, __ds18x20__
    if config.exists('sensors.dht22'):
        pin = Pin(int(config.get('sensors.dht22')))
        __dht22__ = dht.DHT22(pin)
    if config.exists('sensors.ds18x20'):
        pin = Pin(int(config.get('sensors.ds18x20')))
        ow = onewire.OneWire(pin)
        __ds18x20__ = ds18x20.DS18X20(ow)

init()