from machine import RTC
import config
import sensors
import control

def dump_sensors():
    print("== SENSORS ==")
    if sensors.dht22_present():
        print("DHT22:")
        print("  Temperature: "+str(sensors.dht22_temperature()) + " C")
        print("  Humidity: "+str(sensors.humidity()) + "%")
    if sensors.ds18x20_present():
        print("DS18X20:")
        print("  Temperature: "+str(sensors.ds18x20_temperature()) + " C")
    if sensors.door_sensor_set():
        print("Door: ")
        if sensors.is_door_open():
            print("  Open")
        else:
            print("  Closed")

def dump():
    print("== GLOBAL ==")
    print("Time: "+str(RTC().datetime()))
    print("Daytime start: "+str(config.get("daytimeStart")))
    print("Daytime end: "+str(config.get("daytimeEnd")))
    if control.is_it_daytime():
        print("IT IS DAYTIME NOW")
    else:
        print("IT IS NIGHT TIME NOW")
    print("\n")

    dump_sensors()