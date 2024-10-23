import os
import pygame
from networkagent import Server, Client, NetworkAgent
from game import Game

CMD_CLIENT = ['1', 'connect', 'client', 'join']
CMD_HOST = ['2', 'host', 'server','start']
CMD_OFFLINE = ['3', 'offline']

DATAPATH = "data/"
def main():
    def __init__(self):
        os.makedirs(DATAPATH, exist_ok=True)

    networkagent: NetworkAgent
    os.system('cls')
    os.system(f'title {'Main Menu'}')
    print(f"{'\033[?25h'}Main Menu:\n|-Join\n|-Host\n|-Offline")
    
    inp = None
    try:
        while inp not in CMD_CLIENT+CMD_HOST+CMD_OFFLINE:
            print(f"Invalid input '{inp}' try {CMD_CLIENT} OR {CMD_HOST} OR {CMD_OFFLINE}") if inp else None
            inpraw = input("> ").lower()
            inp:str = inpraw.split(' ')[0]
            args:str = " ".join(inpraw.split(' ')[1:]) if ' ' in inpraw else ""
        if inp in CMD_CLIENT:
            if len(args.split('.'))==3 and len(args.split(':')==1): pass
                #NetworkAgent.SaveConnectionData(args.split(':')[0], int(args.split(':')[1]))
            os.system(f'title {'Client'}')
            networkagent = Client()            
        if inp in CMD_HOST:
            if len(args.split('.'))==3 and len(args.split(':')==1):pass
                #NetworkAgent.SaveConnectionData(args.split(':')[0], int(args.split(':')[1]))
            os.system(f'title {'Server'}')
            networkagent = Server()
        if inp in CMD_OFFLINE:
            if len(args.split('.'))==3 and len(args.split(':')==1):pass
                #NetworkAgent.SaveConnectionData(args.split(':')[0], int(args.split(':')[1]))
            os.system(f'title {'Offline'}')
            networkagent = NetworkAgent()
        SCALE = 75
        #input()
        game = Game(networkagent)
        #game = Game2d(networkagent, (16, 9, SCALE))
    except KeyboardInterrupt:
        exit(0)

main()