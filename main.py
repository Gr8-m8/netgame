import os
import sys
import pygame
from networkagent import Server, Client, NetworkAgent
from game import Game, CharacterCreator

CMD_CLIENT = ['1', 'connect', 'client', 'join']
CMD_HOST = ['2', 'host', 'server','start']
CMD_OFFLINE = ['3', 'offline']

DATAPATH = "data/"

def settitle(title = ""):
    os.system(f'title {title}') if os.name == 'nt' else None
    sys.stdout.write(f"\x1b]2;{title}\x07") if not os.name == 'nt' else None

def main():
    def __init__(self):
        os.makedirs(DATAPATH, exist_ok=True)

    networkagent: NetworkAgent
    os.system('cls' if os.name == 'nt' else 'clear')
    settitle('Main Menu')
    print('\033[?25h')
    print(f"Main Menu:\n|-Join\n|-Host\n|-Offline")
    
    inp = None
    try:
        while inp not in CMD_CLIENT+CMD_HOST+CMD_OFFLINE:
            print(f"Invalid input '{inp}' try {CMD_CLIENT} OR {CMD_HOST} OR {CMD_OFFLINE}") if inp else None
            inpraw = input("> ").lower()
            inp:str = inpraw.split(' ')[0]
            args:str = " ".join(inpraw.split(' ')[1:]) if ' ' in inpraw else ""
        if inp in CMD_CLIENT:
            if len(args.split('.'))==3 and len(args.split(':')==1): 
                NetworkAgent.SaveConnectionData(args.split(':')[0], int(args.split(':')[1]))
            settitle("Game Client")
            networkagent = Client         
        if inp in CMD_HOST:
            if len(args.split('.'))==3 and len(args.split(':')==1):
                NetworkAgent.SaveConnectionData(args.split(':')[0], int(args.split(':')[1]))
            settitle("Game Server")
            networkagent = Server
        if inp in CMD_OFFLINE:
            if len(args.split('.'))==3 and len(args.split(':')==1):
                NetworkAgent.SaveConnectionData(args.split(':')[0], int(args.split(':')[1]))
            settitle("Game Offline")
            networkagent = NetworkAgent
        SCALE = 75
        #input()
        character = CharacterCreator()
        game = Game(networkagent, character)
        #game = Game2d(networkagent, (16, 9, SCALE))
    except KeyboardInterrupt:
        exit(0)

main()