from wifi import Cell, Scheme 

def getAll(parameters, data):
    return [{
        "type": "wifiAccessPoints",
        "value": Cell.all('wlan0') # Map is not serializable
    }]