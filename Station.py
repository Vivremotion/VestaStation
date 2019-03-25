import json
import os
from Firebase import firebase

stationFilePath = '/usr/share/Station/station.json'
station = {
    'settings': {
        'new': True,
        'measurementsInterval': 30 #seconds
    }
}

def initialize():
    fileExists = os.path.isfile(stationFilePath)
    if not fileExists:
        file = open(stationFilePath, 'a+')
        file.write(json.dumps(station))

def get(parameters, data):
    initialize()
    file = open(stationFilePath, 'r')
    fileContent = file.read()
    print(fileContent)
    station = json.loads(fileContent)
    return station

def set(parameters, data):
    initialize()
    station = get(None, None)
    if 'settings' in data:
        station['settings'].update(data['settings'])
        data['settings'] = station['settings']
    station.update(data)
    print(station)
    file = open(stationFilePath, 'w')
    file.write(json.dumps(station))
    if 'name' in station['settings']:
        file = open('/etc/machine-info', 'w')
        file.write('PRETTY_HOSTNAME='+station['settings']['name'])
    firebase.send('stations', station['id'], station)
    return station
