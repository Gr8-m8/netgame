import socket
from threading import Thread
import os
from logger import logger

class NetworkAgent:
    DATAFILE = f"data/connection.data"
    def __init__(self) -> None:
        self.host, self.port = NetworkAgent.LoadConnectionData()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.command = ""

    def getCommand(self):
        command = self.command
        self.command = ""
        return command

    def data_recive(self):
        pass

    def data_send(self, data = None):
        self.command = data if data else None
        

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
    def SaveConnectionData(qaddress:str, qport:str):
        address = qaddress
        port = qport

        if (not os.path.isfile(NetworkAgent.DATAFILE)):
            open(NetworkAgent.DATAFILE, "x")

        try:
            datafile = open(NetworkAgent.DATAFILE, "w")
            datafile.write(f"{address}\n{port}")
            datafile.write()
            datafile.close()
        except: pass


class Client(NetworkAgent):
    def __init__(self) -> None:
        super().__init__()
        self.socket.connect((self.host, self.port))

        Thread(target=self.data_recive, args=(None,)).start()
        #self.data_send(f"join")

    def data_recive(self, data = None):
        try:
            while True: #server connection
                DATASCALE = 1
                data = self.socket.recv(2048*DATASCALE).decode()
                if data:
                    logger.Log(f"got {data}")
                    if data.startswith("stop"):
                        os._exit(0)
                    self.command = data
        except:
            print("SERVER DOWN")
            os._exit(0)

    def data_send(self, data = None):
        self.socket.send(data.encode()) if data else None


class Server(NetworkAgent):
    def __init__(self) -> None:
        super().__init__()
        self.clients = []
        self.addlogg = []

        try:
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print("UNABLE TO OPEN SERVER\n",e)
            os._exit(-1)

        self.socket.listen()
        print(f"SERVER OPEN on {self.host}:{self.port}")

        while True: # serverloop
            cliet_socket, address = self.socket.accept()
            self.clients.append(cliet_socket)
            print(f"CONNECTION {address} as {self.clients.index(cliet_socket)}")
            Thread(target=self.data_recive, args=(cliet_socket,)).start()
            for data in self.addlogg:
                self.data_send(cliet_socket, data)

    def data_recive(self, client_socket: socket.socket):
        try:
            client_loop = True
            while client_loop: #client connection
                DATASCALE = 1
                data = client_socket.recv(2048*DATASCALE).decode()
                if data:
                    if data.startswith("stop"):
                        client_loop=False
                    if data.startswith("add"):self.addlogg.append(data)
                    print(f"got {data}")
                    for client in self.clients:
                        self.data_send(client, data)
        except:
            print(f"CONNECTION END as {self.clients.index(client_socket)}")
            client_socket.close()
        
        os._exit(0)

    def data_send(self, client_socket: socket.socket, data: str = None):
        client_socket.send(data.encode()) if data else None
        print(f"send {data} to {self.clients.index(client_socket)}")