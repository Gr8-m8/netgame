import socket
from _thread import start_new_thread
from threading import Thread
import sys
import os

class NetworkAgent:
    DATAFILE = f"data/connection.data"
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server, self.port = NetworkAgent.LoadConnectionData()
        self.address = (self.server, self.port)

        self.scenario:str = f"{self.connect()}"
        self.command:str = ""

    def getscenario(self):
        return self.scenario

    def getCommand(self):
        command = self.command
        self.command = ""
        return command
    
    def connect(self, data = None):
        return data

    def send(self, data, game = None):
        return game.Action(data) if game else None

    @staticmethod
    def LoadConnectionData():
        address = "127.0.0.1"
        port = 7777
        if (not os.path.isfile(NetworkAgent.DATAFILE)):
            open(NetworkAgent.DATAFILE, "x")
            NetworkAgent.SaveConnectionData(address, port)

        try:
            datafile = open(NetworkAgent.DATAFILE, "r")
            address = str(datafile.readline()[:-1])
            port = int(datafile.readline())
            datafile.close()
        except:
            pass
        
        DEBUG = False
        print(f"[{address}:{port}]") if DEBUG else None
        return address, port
    
    @staticmethod
    def SaveConnectionData(qaddress:str, qport:int):
        address = qaddress
        port = qport

        if (not os.path.isfile(NetworkAgent.DATAFILE)):
            open(NetworkAgent.DATAFILE, "x")

        try:
            datafile = open(NetworkAgent.DATAFILE, "w")
            datafile.write(address)
            datafile.write(port)
            datafile.close()
        except: pass

class Client(NetworkAgent):
    def _init__(self) -> None:
        super().__init__()

    def connect(self, data = None):
        try:
            self.sock.connect(self.address)
            DATASCALE = 1
            #input("connect")
            return self.sock.recv(2048*DATASCALE).decode()
        except socket.error as e:
            print(e)
        except Exception as e:
            print(e)

    def send(self, data, game = None):
        try:
            self.sock.send(str.encode(data))
            DATASCALE = 1
            reply = self.sock.recv(2048*DATASCALE).decode()
            self.command = reply
            return data
        except socket.error as e:
            print(e)
        except Exception as e:
            print(e)
        return data
from scenario import Scenario, scenario_TheCabin
class Server(NetworkAgent):
    def __init__(self) -> None:
        super().__init__()
        self.scenario = ""#scenario_TheCabin()
        self.clients = list()

        try:
            self.sock.bind((self.server,self.port))
        except socket.error as e:
            print(e)
            exit(-1)

        self.sock.listen()
        print("WAITING FOR CLIENT")
        server_loop = True
        
        while server_loop:
            connection, address = self.sock.accept()
            self.clients.append(connection)
            print(f"CONNECT FROM {address} as {self.clients.index(connection)}")
            start_new_thread(self.TClient, (connection,))
        
    def TClient(self, connection: socket.socket):
        connection.send(str.encode(str(self.clients.index(connection))))
        client_loop = True
        while client_loop:
            try:
                DATASCALE = 1
                data = connection.recv(2048*DATASCALE).decode()
                if data.startswith("stop"):
                    sys.exit(1)
                self.command = data

                if not data:
                    print(f"BREAK CONNECTION as {self.clients.index(connection)}")
                    self.clients.remove(connection)
                    client_loop = False
                    break
                else:
                    print(f"DATA: '{data}'")
                    
                    #print(f"SEND: {reply}")
                for client in self.clients:
                    #client: socket.socket
                    print(f"sendto {self.clients.index(client)}")
                    client.sendall(str.encode(f"{self.command}"))
            except:
                client_loop = False
                break
        print(f"CONNECTION END as {self.clients.index(connection)}")
        connection.close()