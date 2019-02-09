import bluetooth
import sys
import socket
import json
import importlib

def invalidAction(name):
    return Exception('\'%s\' is not a correct action' % (name))

class BluetoothModule:
    port = 1
    socket = None
    clientSocket = None
    clientInfo = None
    socketOpen = False

    def send(self, data):
        try:
            if not type(data) is str:
                data = json.dumps(data)
            self.clientSocket.send(data)
            self.clientSocket.send('\n')
        except Exception as error:
            print(str(error))


    def route(self, data):
        try:
            if not 'route' in data:
                raise Exception('No route provided')
            moduleName, actionName, *parameters = data['route'].split('/')
            module = importlib.import_module(moduleName)
            action = getattr(module, actionName, None)
            if not callable(action):
                raise invalidAction(actionName)
            self.send(action(parameters, data))
        except Exception as error:
            print(str(error))


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
                print("Received %s" % data)
                self.route(json.loads(data))
            except Exception as error:
                print(str(error))
                break


    def initialize(self, port):
        self.port = port
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
            print(str(error))
            print("Disconnected")
            pass


if __name__ == "__main__":
    bluetoothModule = BluetoothModule()
    bluetoothModule.initialize(int(sys.argv[1]))
