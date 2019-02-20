

from wifi import Cell, Scheme

def _getValues(network):
    print(network)
    return {
        "ssid": network.ssid,
        "signal": network.signal,
        "quality": network.quality,
        "address": network.address
    }

def getAll(parameters, data):
    networks = []
    for network in Cell.all('wlan0'):
        networks.append(_getValues(network))

    return [{
        "type": "wifiAccessPoints",
        "value": networks
    }]

def connectIfExists(parameters, data):
    scheme = Scheme.find('wlan0', data["ssid"])
    if scheme:
       scheme.activate()
    return {
        "type": "wifiConnectIfExists",
        "value": True if not scheme != None else False
    }

def connect(parameters, data):
    scheme = Scheme.find('wlan0', data["ssid"])
    if not scheme:
        cell = Cell.where('wlan0', lambda cell: cell.ssid == data["ssid"])[0]
        if cell:
            scheme = Scheme.for_cell('wlan0', data["ssid"], cell, data["passkey"])
            scheme.save()
        else:
            connection = "Invalid ssid"
    if not connection:
        connection = scheme.activate()
    return {
        "type": 'wifiConnection',
        "value": connection
    }
