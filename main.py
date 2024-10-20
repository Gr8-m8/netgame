import os
import pygame
from networkagent import Server, Client, NetworkAgent
from game import Game

CMD_CLIENT = ['1', 'connect', 'client']
CMD_HOST = ['2', 'host', 'server',]
CMD_OFFLINE = ['3', 'offline', '']

def main():
    networkagent: NetworkAgent

    print("Connect:")
    
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
                pass

        SCALE = 75
        game = Game(networkagent, (16, 9, SCALE))
    except KeyboardInterrupt:
        exit(0)

main()