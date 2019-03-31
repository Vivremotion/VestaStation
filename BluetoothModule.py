import bluetooth
import sys
import socket
import json
from json import JSONDecoder
import importlib
import subprocess
import re
import Station
import utils

def invalidAction(name):
    return Exception('\'%s\' is not a correct action' % (name))

def decodeStacked(data, pos=0, decoder=JSONDecoder()):
    while True:
        try:
            obj, pos = decoder.raw_decode(data, pos)
            if len(data) == pos:
                yield obj
                return
        except Exception as error:
            print('An error occured while decoding incoming data from bluetooth: ', str(error))
        yield obj

class BluetoothModule:
    port = 1
    socket = None
    clientSocket = None
    clientInfo = None
    socketOpen = False
    localAddress = ''
    station = Station.get()

    def send(self, route, data):
        self.station = Station.get()
        dataToSend = {
            "stationId": self.station['id'],
            "address": self.localAddress,
            "route": route,
            "data": data
        }
        try:
            dataToSend = json.dumps(dataToSend)
            self.clientSocket.send(dataToSend)
            self.clientSocket.send('\n')
        except Exception as error:
            print('An error occured while sending via bluetooth: ', str(error))


    def route(self, data):
        try:
            if not 'route' in data:
                raise Exception('No route provided')
            if not 'address' in data:
                raise Exception('No address')
            if not data['address'] == self.localAddress:
                return
            route = data["route"]
            moduleName, actionName = route.split('/')
            module = importlib.import_module(moduleName)
            action = getattr(module, actionName, None)
            if not callable(action):
                raise invalidAction(actionName)
            del data['route']
            del data['address']
            self.send(route, action(data))
        except Exception as error:
            print('An error occured in the bluetooth module while routing', str(error))


    def listen(self):
        while True:
            try:
                data = self.clientSocket.recv(1024).decode('utf-8')
                if len(data) == 0: break
                if (data == 'stop'):
                    self.clientSocket.close()
                    self.socket.shutdown(socket.SHUT_RDWR)
                    self.socket.close()
                    self.socketOpen = False
                    break
                try:
                    for request in decodeStacked(data):
                        if len(request):
                            print("Received %s" % request)
                            self.route(request)
                except Exception as error:
                    print('An error occured in the bluetooth module after data was received: ', str(error))
                    pass
            except Exception as error:
                print('An error occured in the bluetooth module while listening: ', str(error))
                subprocess.check_output('service bluetooth restart', shell=True).decode('utf8')
                break


    def initialize(self, port):
        self.port = port
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.localAddress = utils.getBluetoothAddress()
        try:
            self.socket.bind(('', port))
            self.socketOpen = True
            self.socket.listen(1)
            while True:
                if self.socketOpen:
                    print("Waiting for connection on RFCOMM channel %d" % port)
                    clientSocket, clientInfo = self.socket.accept()
                    self.clientSocket = clientSocket
                    self.clientInfo = clientInfo
                    print("Accepted connection from ", self.clientInfo)
                    self.listen()
                else: break
        except Exception as error:
            print('An error occured in the blueototh module: ', str(error))
            print("Disconnected")
            pass
