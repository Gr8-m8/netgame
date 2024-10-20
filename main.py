import os
import pygame
from networkagent import Server, Client, NetworkAgent
from game import Game

CMD_CLIENT = ['1', 'connect', 'client']
CMD_HOST = ['2', 'host', 'server',]
CMD_OFFLINE = ['3', 'offline', '']

DATAPATH = "data/"
def main():
    def __init__(self):
        os.makedirs(DATAPATH, exist_ok=True)

    if (not os.path.isfile(NetworkAgent.DATAFILE)):
        open(NetworkAgent.DATAFILE, "x")
        NetworkAgent.SaveConnectionData("127.0.0.1", 7777)

    networkagent: NetworkAgent

    print("Start:")
    
    inp = None
    try:
        while inp not in CMD_CLIENT+CMD_HOST+CMD_OFFLINE:
            print(f"Invalid input '{inp}' try {CMD_CLIENT} OR {CMD_HOST} OR {CMD_OFFLINE}") if inp else None
            inp = input("> ").lower()

        if inp in CMD_CLIENT:
            networkagent = Client()            
        if inp in CMD_HOST:
            networkagent = Server()
        if inp in CMD_OFFLINE:
            networkagent = NetworkAgent()

        SCALE = 75
        game = Game(networkagent, (16, 9, SCALE))
    except KeyboardInterrupt:
        exit(0)

main()