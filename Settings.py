import json
import os

settingsFilePath = '/usr/share/Station/settings.json'

def get(parameters, data):
    fileExists = os.path.isfile(settingsFilePath)
    if not fileExists:
        file = open(settingsFilePath, 'a+')
        file.write(json.dumps({}))
    file = open(settingsFilePath, 'r')
    fileContent = file.read()
    settings = json.loads(fileContent)
    return settings

def set(parameters, data):
    settings = get(None, None)
    print(type(settings))
    settings.update(data["settings"])
    file = open(settingsFilePath, 'w')
    file.write(json.dumps(settings))
    return settings
