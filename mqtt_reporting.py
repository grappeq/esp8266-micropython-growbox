from umqtt.simple import MQTTClient
from machine import Timer
import ujson
import config
import sensors

__mqtt__ = None

def prepare_sensor_data():
    data = {}
    temperature = sensors.temperature()
    if temperature is not None:
        data["temperature"] = str(temperature)
    humidity = sensors.humidity()
    if humidity is not None:
        data["humidity"] = str(humidity)
    if sensors.door_sensor_set():
        if sensors.is_door_open():
            data["door"] = "open"
        else:
            data["door"] = "closed"
    return data

def report_sensor_data():
    global __mqtt__
    data = prepare_sensor_data()
    try:
        __mqtt__.connect()
        __mqtt__.publish(config.get("mqtt.topic"), bytes(ujson.dumps(data), 'utf-8'))
    except OSError:
        print("Couldn't connect to MQTT broker")

def run():
    if not config.exists("mqtt"):
        return
    report_sensor_data()

def setup():
    global __mqtt__
    if not config.exists("mqtt"):
        return
    __mqtt__ = MQTTClient(config.get("mqtt.clientID"), config.get("mqtt.brokerIP"))