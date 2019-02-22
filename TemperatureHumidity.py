import sys
import datetime
import Adafruit_DHT

sensorNumber = 11
port = 4

def get(parameters, data):
    humidity, temperature = Adafruit_DHT.read_retry(sensorNumber, port)
    date = str(datetime.datetime.now())
    return [{
        "type": 'temperature',
        "value": temperature,
        "date": date
    }, {
        "type": 'humidity',
        "value": humidity,
        "date": date
    }]