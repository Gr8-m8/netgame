import time
import os
import msvcrt

from networkagent import NetworkAgent
from gameobject import GameObject, Location, Prop, Item, Actor
from scenario import scenario_TheCabin

class Timer:
    def __init__(self, step) -> None:
        self.time = 0
        self.step = step
        
    
    def Tick(self):
        self.time += self.step

class Player(Actor):
    def __init__(self, name: str, desc: dict, location:Location, see: GameObject = None) -> None:
        super().__init__(name, desc)
        self.location:Location = location
        self.see: GameObject = self.location if not see else see

class Game:
    def __init__(self, networkagent:NetworkAgent) -> None:
        self.networkagent:NetworkAgent = networkagent
        self.debug = ""
        self.input_suggest = ""
        self.input = ""
        self.input_response = ""
        self.timer = Timer(0.1)

        self.scenario = scenario_TheCabin(self)
        self.player = Player("player", {"player": "Person"}, list(self.scenario.container.values())[0])
        self.player.location.append(self.player)
        

        self.game_loop = True
        while self.game_loop:
            self.Draw()
            self.Update()

        print('\033[?25h')
        os.system('cls')

    def setResponse(self, response):
        self.input_response = response
        return self.input_response
    
    def Draw(self):
        #time.sleep(self.timer.step)
        self.timer.Tick()
        os.system('cls')
        print(self.player.see.Draw(), end="\n\n")
        print(self.input_response)
        print(f"\n> {self.input}", end=f"{f'{'\033[107m'} {'\033[0m'}'}{'\n'}{'\033[?25l'}") #'\033[?25h'
        print(self.debug)

    def Update(self):
        key = None
        waitforkey = True
        while waitforkey:
            try:
                if msvcrt.kbhit():
                    waitforkey = False
                    key = msvcrt.getch()
            except KeyboardInterrupt:
                waitforkey = False
                self.game_loop = False
                return
        
        self.debug = key
        if key in b'qwertyuiopasdfghjklzxcvbnm !?"':
            self.input+= key.decode()
        
        if key in b'123456789KHMP':
            if key == b'1': self.input+="one"
            if key == b'2': self.input+="two"
            if key == b'3': self.input+="three"
            if key == b'4': self.input+="four"
            if key == b'5': self.input+="five"
            if key == b'6': self.input+="six"
            if key == b'7': self.input+="seven"
            if key == b'8': self.input+="eight"
            if key == b'9': self.input+="nine"
            if key == b'0': self.input+="zero"

            if key == b'H': self.input+="north"
            if key == b'P': self.input+="south"
            if key == b'K': self.input+="west"
            if key == b'M': self.input+="east"

        if key in [b'\x08']:
            self.input = self.input[:-1]
        if key in [b'\t']:
            pass
        if key in [b'\r']:
            self.debug = self.Actions(self.input)
            self.input = ""

    ACTION_CMD_USE = ['use', 'go']
    ACTION_CMD_SEE = ['see', 'inspect']
    ACTION_CMD_WAIT = [' ', 'wait']
    ACTION_CMDS = ACTION_CMD_USE+ACTION_CMD_SEE+ACTION_CMD_WAIT
    def Actions(self, commandargs):
        self.input_response = ""
        commandargs = commandargs.split(' ')
        command, args = (commandargs[0], commandargs[1:])
        
        if command not in self.ACTION_CMDS:
            self.ActionResponse(f"{self.player.name} can't '{command}'")
            return (False, "NOT IN CMDS")

        if command in self.ACTION_CMD_USE:
            args.insert(0, self.player.location.name)
            go: Prop = self.scenario.getgo(args)
            if isinstance(go, Prop):
                #self.ActionResponse(f"{self.player.name} used {go.name}")
                go.Use()
                return (True, f"USED {go.name}")
            else:
                self.ActionResponse(f"{self.player.name} can't use {go.name.capitalize() if go else "'nothing'"}")
                return (False, "UNUSABLE")
            
        if command in self.ACTION_CMD_SEE:
            args.insert(0, self.player.location.name)
            go = self.scenario.getgo(args) if args else self.player.location
            if go:
                self.player.see = go

                self.ActionResponse(f"{self.player.name} inspects {go.name}")
                return (True, f"CAN SEE {go.name}")
            else:
                self.ActionResponse(f"{self.player.name} can't inspect {",".join(args)}")
                return (False, f"CAN'T SEE {args}")

        self.ActionResponse(f"{self.player.name} was idle")
        return (False, "NOT ACTIVATED")

    def ActionMove(self, gokey: list, destinationkey: list):
        go = self.scenario.getgo(gokey)
        source = self.scenario.getgo(gokey[:-1])
        destination = self.scenario.getgo(destinationkey)
        destination.append(source.remove(go))
        if go==self.player:
            self.player.location = destination
            self.player.see = destination
            self.ActionResponse(f"{self.player.name} moved to {destination.name}")
            return

        self.ActionResponse(f"{go} was moved to {destination}")

    def ActionSee(self, gokey = None):
        go = self.scenario.getgo(gokey) if gokey else self.player.location
        self.player.see = go

        self.ActionResponse(f"{self.player.name} inspects {go.name}")

    def ActionResponse(self, response):
        self.input_response = response