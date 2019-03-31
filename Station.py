import json
import os
import utils
from Firebase import firebase

stationFilePath = '/usr/share/VestaStation/station.json'
station = {
    'address': utils.getBluetoothAddress(),
    'settings': {
        'new': True,
        'measurementsInterval': 30 #seconds
    },
    'read': [],
    'write': []
}

def initialize():
    fileExists = os.path.isfile(stationFilePath)
    if not fileExists:
        file = open(stationFilePath, 'a+')
        file.write(json.dumps(station))

def _update(station):
    file = open(stationFilePath, 'w')
    file.write(json.dumps(station))
    print('Station updated: ')
    print(station)
    print('\n')
    firebase.send('stations', station['id'], station)
    return station

def get(data=None):
    initialize()
    file = open(stationFilePath, 'r')
    fileContent = file.read()
    print(fileContent)
    station = json.loads(fileContent)
    return station

def set(data):
    initialize()
    station = get()
    if 'settings' in data:
        station['settings'].update(data['settings'])
        data['settings'] = station['settings']
    station.update(data)
    if 'name' in station['settings']:
        file = open('/etc/machine-info', 'w')
        file.write('PRETTY_HOSTNAME='+station['settings']['name'])
    _update(station)
    return station

def addWriter(data):
    if not data['uid']:
        return { 'error': 'Missing uid' }
    initialize()
    station = get()
    if not data['uid'] in station['write']:
        station['write'].append(data['uid'])
        _update(station)
    return 'OK'
    
def addReader(data):
    if not data['uid']:
        return { 'error': 'Missing uid' }
    initialize()
    station = get()
    if not data['uid'] in station['read']:
        station['read'].append(data['uid'])
        _update(station)
    return 'OK'
