import sys
import Adafruit_DHT

sensorNumber = 11
port = 4

def get(parameters, data):
    humidity, temperature = Adafruit_DHT.read_retry(sensorNumber, port)
    return [temperature, humidity]