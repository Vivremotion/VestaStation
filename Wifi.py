from wifi import Cell
import time
import re
import subprocess
import os

def _getConfigurationForSSID(ssid):
    wpaPath = '/etc/wpa_supplicant/wpa_supplicant.conf'
    file = open(wpaPath, 'r')
    content = file.read()
    return re.search('(network=\{{\n.*ssid="{ssid}"\n(.|\n)*?\}}\n*)+?'.format(ssid=ssid), c$

def _updateWpa(ssid, psk=False):
    wpaPath = '/etc/wpa_supplicant/wpa_supplicant.conf'
    file = open(wpaPath, 'r')
    content = file.read()
    networkText = re.search('(network=\{{\n.*ssid="{ssid}"\n(.|\n)*?\}}\n*)+?'.format(ssid=s$
    if not networkText and not psk:
        return False
    if networkText:
        networkText=networkText.group(0)
    else:
        networkText = ''
    if not len(content):
        content = """country=FR
update_config=1
ctrl_interface=/var/run/wpa_supplicant\n"""
    if not psk:
        psk=re.search('(?<=psk=").*(?=")', networkText)
        if psk:
            psk = psk.group(0)
        else:
            return False
    content = content.replace(networkText, '')
    content = content.replace("priority=2", "priority=1")
    newNetwork="""\nnetwork={{
  ssid="{ssid}"
  psk="{psk}"
  priority=2
}}\n""".format(ssid=ssid, psk=psk)
    file = open(wpaPath, 'w')
    file.write(content + newNetwork)
    return True

def _getValues(network):
    return {
        "ssid": network.ssid,
        "signal": network.signal,
        "quality": network.quality,        "address": network.address
        "address": network.address
    }

def getAll(parameters, data):
    networks = []
    for network in Cell.all('wlan0'):
        networks.append(_getValues(network))
    return [{
        "type": "Wifi/getAll",
        "value": networks
    }]


def _getCurrent():
    current = subprocess.check_output('iwgetid -r', shell=True).decode('utf8')
    if not current:
        return ''
    return current.replace('\n', '')

def getCurrentSSID(parameters, data):
    return {
        "ssid": _getCurrent()
    }

def connect(parameters, data):
    if not 'passkey' in data:
        data['passkey'] = None
    valid = _updateWpa(data['ssid'], data['passkey'])
    answer = {
        "route": "Wifi/connect",
        "ssid": data["ssid"],
        "connected": False
    }
    if not valid:
        return answer
    output = subprocess.check_output('sudo wpa_cli -i wlan0 reconfigure', shell=True).decode$
    if not 'OK' in output:
        return answer
    # todo: find a solution to get rid of that time.sleep
    time.sleep(10)
    current = _getCurrent()
    if len(current) == 0:
        return answer
    print('Now connected to: '+current)
    if not current == data['ssid']:
        return answer
    answer['connected'] = True
    return answer

def disconnect(parameters, data):
    answer = {
        "route": "Wifi/disconnect",        "disconnected": False
        "disconnected": False
    }
    wpaPath = '/etc/wpa_supplicant/wpa_supplicant.conf'
    file = open(wpaPath, 'r')
    content = file.read()
    networkText = re.search('(network=\{{\n.*ssid="{ssid}"\n(.|\n)*?\}}\n*)+?'.format(ssid=d$
    if not networkText:
        return answer
    networkText=networkText.group(0)
    newNetworkText = '#'+networkText.replace('\n', '\n#')
    content = content.replace(networkText, newNetworkText)
    print(content)
    file = open(wpaPath, 'w+')
    file.write(content)
    output = subprocess.check_output('sudo wpa_cli -i wlan0 reconfigure', shell=True).decode$
    if not 'OK' in output:
        return answer
    # todo: find a solution to get rid of that time.sleep
    time.sleep(10)
    current = _getCurrent()
    if current == data["ssid"]:
        return answer
    answer["disconnected"] = True
    return answer