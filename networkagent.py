import socket
from _thread import start_new_thread
import sys

class NetworkAgent:
    DATAFILE = f"data/connection.data"
    
    def send(self): pass

    @staticmethod
    def LoadConnectionData():
        address = "127.0.0.1"
        port = 7777
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

        try:
            datafile = open(NetworkAgent.DATAFILE, "w")
            datafile.write(address)
            datafile.write(port)
            datafile.close()
        except: pass

    

class Server(NetworkAgent):
    def __init__(self, address: str = None, port: int = None) -> None:
        self.server: str = address
        self.port: int = port

        self.playersNum = 0

        if not self.server or not self.port:
            server, port = Server.LoadConnectionData()
            self.server = server if not self.server else None
            self.port = port if not self.port else None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.bind((self.server,self.port))
        except socket.error as e:
            print(e)
            exit(-1)

        self.sock.listen()
        print("Server Set Up")
        server_loop = True
        try:
            while server_loop:
                connection, address = self.sock.accept()
                print(f"CONNECT FROM {address}")

                start_new_thread(self.TClient, (connection, self.playersNum))
                self.playersNum += 1
        except KeyboardInterrupt:
            server_loop = False
        except:
            exit(1)
        

    def TClient(self, connection: socket, playerID):
        connection.send(str.encode(str(playerID)))
        reply = ""
        client_loop = True
        while client_loop:
            try:
                DATASCALE = 1
                data = connection.recv(2048*DATASCALE)
                reply = data.decode("utf-8")

                if not data:
                    print("BREAK CONNECTION")
                    client_loop = False
                    break
                else:
                    print(f"RECIVE: {reply}")
                    print(f"SEND: {reply}")
                
                connection.sendall(str.encode(f"Server Got: {reply}"))
            except:
                client_loop = False
                break
        print("CONNECTION END")
        connection.close()
        

class Client(NetworkAgent):
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None
        self.port = None
        self.server, self.port = Client.LoadConnectionData()
        self.address = (self.server, self.port)
        self.id = self.connect()
        print(f"ID: {self.id}")


    def connect(self):
        try:
            self.client.connect(self.address)
            DATASCALE = 1
            return self.client.recv(2048*DATASCALE).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            DATASCALE = 1
            return self.client.recv(2048*DATASCALE).decode()
        except socket.error as e:
            print(e)