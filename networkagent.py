#CREDIT@https://www.techwithtim.net/tutorials/python-online-game-tutorial
#CREDIT@https://www.youtube.com/watch?v=8Q7OF8TP6u0

import socket
import pickle
from threading import Thread
import os
from logger import logger

class networkdata:
    TAG_TARGET = "on"
    TAG_ACTOR = "as"
    TAG_SCENARIO = "SCENARIO"
    TAGS = [TAG_TARGET,TAG_ACTOR]
    KEY_COMMAND = "cmd"
    KEY_COMMANDARGS = "raw"

    
    @staticmethod #SPLIT AT ' ' AND INDEX
    def command(commandargs:str) -> dict:
        commandargs = str(commandargs)
        cmd = {}
        cmd.update({networkdata.KEY_COMMANDARGS: commandargs})
        key = commandargs.split(' ')[0]
        cmd.update({networkdata.KEY_COMMAND: key})
        
        TAGS = [cmd[networkdata.KEY_COMMAND]]+networkdata.TAGS
        tag = ""
        for arg in commandargs.split(' '):
            if arg in TAGS:
                tag = arg
                cmd.update({tag: []})
            else:
                cmd[tag].append(arg)

        return cmd
    
    @staticmethod
    def scenario(scenario) -> dict:
        d = {}
        d.update({networkdata.TAG_SCENARIO: scenario})
        return d

class NetworkAgent:
    DATAFILE = f"data/connection.data"
    def __init__(self) -> None:
        self.host, self.port = NetworkAgent.LoadConnectionData()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.commands = []

    def getCommand(self):
        return self.commands.pop(0) if len(self.commands)>0 else None

    def data_recive(self, data = None):
        self.commands.append(data) if data else None

    def data_send(self, data = None):
        self.data_recive(data)

    def connect(self, data = None):
        return data
        

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
                data:dict = pickle.loads(self.socket.recv(2048*DATASCALE))
                if data:
                    logger.Log(f"got {data}")
                    if "stop" in data[networkdata.KEY_COMMAND]:
                        os._exit(0)
                    self.commands.append(data)
        except:
            print("SERVER DOWN")
            os._exit(0)

    def data_send(self, data = None):
        self.socket.send(pickle.dumps(data)) if data else None


class Server(NetworkAgent):
    def __init__(self) -> None:
        super().__init__()
        self.clients = []
        self.addlogg = []
        self.scenario = None

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
            self.data_send(cliet_socket, self.scenario)
            Thread(target=self.data_recive, args=(cliet_socket,)).start()
            for data in self.addlogg:
                self.data_send(cliet_socket, data)

    def data_recive(self, client_socket: socket.socket):
        try:
            client_loop = True
            while client_loop: #client connection
                DATASCALE = 1
                data:dict = pickle.loads(client_socket.recv(2048*DATASCALE))
                if data:
                    if "stop" in data[networkdata.KEY_COMMAND]:
                        client_socket.close()
                        os._exit(0)

                    if "add" in data[networkdata.KEY_COMMAND]:self.addlogg.append(data)
                    print(f"got {data}")
                    for client in self.clients:
                        try:
                            self.data_send(client, data)
                        except: continue
                else:
                    print(f"CLIENT CONNECTION END as {self.clients.index(client_socket)}")
                    client_socket.close()
            
        except:
            print(f"SERVER CONNECTION END as {self.clients.index(client_socket)}")
            client_socket.close()
            #os._exit(0)
        

    def data_send(self, client_socket: socket.socket, data: str = None):
        client_socket.send(pickle.dumps(data)) if data else None
        print(f"send {data} to {self.clients.index(client_socket)}")