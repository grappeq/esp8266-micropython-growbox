# esp8266-micropython-growbox
Simple system written to control small indoor plant cultivation. It's still a working progress, but allows for basic control over grow box. Probably also can be a solid foundation for something bigger. 
DISCLAIMER: Python is not my first language.
## Getting Started
### Board
You need have [micropython](http://micropython.org/) installed on your esp8266 board. Instructions can be obtained from [here](http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html).

System should work with any esp8266-based board (and with pure esp8266) - as long as it runs micropython. Following boards were tested:
* Wemos D1 mini (V1 and V2.1)

### Wiring
Connect relays controlling lights and other devices (such as air pumps, water pumps etc.) to selected pins. *It is assumed that the relay is closed when the control line is LOW.* If your relay behaves in a different manner, you can always just change the electrical wiring (connect cable to NC instead of NO) to avoid changing the code.

Connect any sensors you might need according to their specifications.

#### Supported sensors
Following sensor modules are supported:
* DS18S20 and DS18B20 digital temperature sensor - remember about pull-up resistor on the data line
* DHT22 humidity and temperature sensor
* magnetic door sensor (closes circuit when the door is closed, e.g. [this one](https://www.adafruit.com/product/375)) - connect the sensor to 3.3V from one side and to the board pin from the other, connect pull-down resistor to that board pin (e.g. 4.7 KOhm resistor to GND).

### Install
Customize **config.json** file according to your needs (check out the configuration section for instructions). Then, simply copy all of the project files to your board. You may use [WebREPL](http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/repl.html) or any other method that is available on your board.

## Configuration
All of the configuration is located in **config.json** file. It contains <i>dict</i> in JSON format with following keys:

Key | Value | Description
------------- | ------------- | -------------
daytimeStart | [*hours*, *minutes*, *seconds*, *miliseconds*] | Time at which the day starts (and the grow lights are lit).
daytimeEnd | [*hours*, *minutes*, *seconds*, *miliseconds*] | Time at which the day ends (and the grow lights are being turned off).
devices | *array* | Array of dictionaries with device configuration. Check out **devices** subsection below.
sensors | *dict*: <br> { *sensor1*: *pin1*, *sensor2*: *pin2*, ... } | Dictionary containing list of all sensors - with sensor name as key and pin as value. Valid sensor names are: <ul><li>**door** - door sensor</li><li>**dht22** - DHT22 sensor</li><li>**ds18x20** - DS18S20 and DS18B20 sensors</li></ul>

### devices
Array of devices. Each record contains 3 keys:

Key | Value | Description
------------- | ------------- | -------------
name | *str* | Device name. Choose any.
pin | *int* | Pin to which the device is connected to.
controller | "on" \| "off" \| "day" \| "door" | Controller name. Depending on the selected controller, the device will be controlled in one of the following ways: <ul><li>**on** - always on</li><li>**off** - always off</li><li>**day** - on during the day, off during the night</li><li>**door** - on when the door is open</li></ul>

### Sample configuration
```
{
  "daytimeStart": [9,0,0,0],
  "daytimeEnd": [22,0,0,0],
  "devices":[
    {
      "name": "air pump",
      "pin": 12,
      "controller": "on"
    },
    {
      "name": "grow light",
      "pin": 14,
      "controller": "day"
    },
    {
      "name": "human light",
      "pin": 16,
      "controller": "door"
    }
  ],
  "sensors": {
    "door": 13,
    "dht22": 2,
    "ds18x20": 4
  }
}
```

## Other features
```
>>> import diagnostic 
>>> diagnostic.dump() 
== GLOBAL ==  
Time: (2017, 3, 28, 1, 7, 37, 23, 769)
Daytime start: [9, 0, 0, 0]   
Daytime end: [22, 0, 0, 0]
IT IS NIGHT TIME NOW  
  
  
== SENSORS == 
DHT22:
  Temperature: 28.8 C 
  Humidity: 31.2% 
DS18X20:  
  Temperature: 23.9375 C  
Door: 
  Closed 
```

## Does it work?
Yes it does! I use it to control grow box with my hydroponic herbs garden. With success.

## TO DO
* HTTP server daemon with:
   * current sensor data 
   * configuration customization
* water level sensor support & water pump controller
* aeroponics fogger controller
* timezone support

## LICENSE
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
