import os
import sys
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
            inpip:str = None
            inpport:str = None
            if args and len(args.split('.'))>0 and len(args.split(':'))>0:
                if len(args.split('.'))==3+1:
                    inpip = args.split(':')[0]
                if len(args.split(':'))==1+1:
                    inpport = args.split(':')[1]

                if inpip and inpport:
                    NetworkAgent.SaveConnectionData(inpip, inpport)

                print(f"|{inpip}={len(args.split('.'))}|{inpport}={len(args.split(':'))}|")

            if inp in CMD_CLIENT:
                settitle("Game Client")
                networkagent = Client         
            if inp in CMD_HOST:
                settitle("Game Server")
                networkagent = Server
            if inp in CMD_OFFLINE:
                settitle("Game Offline")
                networkagent = NetworkAgent
                
        SCALE = 75
        #input()
        
        character = CharacterCreator("Server" if networkagent == Server else None)
        game = Game(networkagent, character)
        #game = Game2d(networkagent, (16, 9, SCALE))
    except KeyboardInterrupt:
        exit(0)

main()