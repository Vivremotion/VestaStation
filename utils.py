import subprocess
import re

def getBluetoothAddress():
    hciOutput = subprocess.check_output(['hcitool', 'dev']).decode('utf8')
    bdaddr = re.search("([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", hciOutput).group(0)
    return bdaddr