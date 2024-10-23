import time
import os
import msvcrt

from networkagent import NetworkAgent
from gameobject import GameObject, Location, Prop, Item, Actor
from scenario import Scenario, scenario_TheCabin

DEBUG = False

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
        self.input_cursor = 0
        self.input = ""
        self.input_response = ""
        self.action_log = ""
        self.timer = Timer(0.1)

        self.scenario:Scenario = scenario_TheCabin(self) #networkagent.connect(scenario_TheCabin(self))
        #self.scenario.Save()

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
        print(self.action_log, end="")
        print(f"\n> {self.input}", end=f"{f'{'\033[107m'} {'\033[0m'}'}{'\n'}{'\033[?25l'}") #'\033[?25h'
        print(self.debug) if DEBUG else None

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
        
        #self.debug = key
        if key in b'qwertyuiopasdfghjklzxcvbnm ,.!?"':
            self.input+= key.decode()
        
        if key in b'123456789+-':
            if key == b'+': self.input+="plus"
            if key == b'-': self.input+="minus"
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

        if key == b'H': self.input+="" #UP
        if key == b'P': self.input+="" #DOWN
        if key == b'K': self.input+="" #LEFT
        if key == b'M': self.input+="" #RIGHT

        if key in [b'\x08']:
            self.input = self.input[:-1]
        if key in [b'\t']:
            pass
        if key in [b'\r']:
            self.action_log = ""
            self.debug = self.networkagent.send(f"{self.input} as {f"{self.player.location} {self.player}"}", self)
            #self.debug = self.Action(data)
            #self.debug = self.Action(f"{self.input} as {f"{self.player.location} {self.player}"}", False)
            self.input = ""
            

        systemcommand = self.networkagent.getCommand()
        self.debug = self.Action(systemcommand) if systemcommand else None

    ACTION_CMD_MOVE = ['move', 'go']
    ACTION_CMD_USE = ['use']
    ACTION_CMD_SEE = ['see', 'inspect']
    ACTION_CMD_WAIT = [' ', 'wait']
    ACTION_CMD_SAY = ['say']
    ACTION_CMDS = ACTION_CMD_MOVE+ACTION_CMD_USE+ACTION_CMD_SEE+ACTION_CMD_WAIT+ACTION_CMD_SAY
    def Action(self, commandargs:str):
        TARGET = 'on'
        ACTOR = 'as'

        #commandargs = commandargs.split(' ')
        command:str = commandargs.split(' ')[0]
        args:list = commandargs.split(' ')[1:]
        gokey: list = commandargs.split(TARGET)[0].split(ACTOR)[0].split(' ')[1:] if ' ' in commandargs else None
        gokey = [i for i in gokey if i] if gokey else None
        targetkey: list = commandargs.split(TARGET)[1].split(ACTOR)[0].split(' ')[1:] if TARGET in commandargs else None
        targetkey = [i for i in targetkey if i] if targetkey else None
        actorkey: list = commandargs.split(ACTOR)[1].split(TARGET)[0].split(' ')[1:] if ACTOR in commandargs else None
        actorkey = [i for i in actorkey if i] if actorkey else None
        if command not in self.ACTION_CMDS:
            self.ActionLog(f"{self.player.name} can't '{command}'")
            return (False, "NOT IN CMDS")

        if command in self.ACTION_CMD_USE:
            if gokey and actorkey:
                return self.ActionUse(gokey=gokey, targetkey=targetkey,actorkey=actorkey)
        
        if command in self.ACTION_CMD_SEE:
            if actorkey:
                return self.ActionSee(gokey=gokey, actorkey=actorkey)

        if command in self.ACTION_CMD_MOVE:# and isSystem:
            if gokey and targetkey and actorkey:
                return self.ActionMove(gokey=gokey, destinationkey=targetkey, actorkey=actorkey)
            return (False, ("gokey", gokey, "target", targetkey, "actor", actorkey))
        
        if command in self.ACTION_CMD_SAY:
            if gokey and actorkey:
                return self.ActionLog(self.ActionSay(gokey, actorkey))


        self.ActionLog(f"{self.player.name} was idle")
        return (False, "NOT ACTIVATED", (command, gokey, targetkey, actorkey))

    def ActionUse(self, gokey: list, targetkey:list, actorkey: list):
        actor: Actor = self.scenario.getgo(actorkey)
        gokey = actorkey[:-1]+gokey[:]
        go: Prop = self.scenario.getgo(gokey)
        target: GameObject = self.scenario.getgo(targetkey)
        if isinstance(go, Prop):
            #self.ActionLog(f"{actor} used {go}")
            go.Use(target, actor)
            return (True, f"{actor} USED {go}")
        else:
            self.ActionLog(f"{actor} can't use {go if go else "'nothing'"}")
            return (False, "UNUSABLE")

    def ActionSee(self, gokey: list, actorkey: list):
        actor = self.scenario.getgo(actorkey)
        gokey = actorkey[:-1]+gokey[:] 
        go = self.scenario.getgo(gokey) #if gokey[-1]=='' else self.scenario.getgo(self.player.location)
        
        if actor == self.player:
            if go:
                self.player.see = go
                self.ActionLog(f"{self.player} inspects {go}")
                return (True, f"CAN SEE {go}", ("gokey", gokey, "actorkey", actorkey))
            else:
                self.ActionLog(f"{self.player} can't inspect {go if go else "'nothing'"}")
                return (False, f"CAN'T SEE {go}", ("gokey", gokey, "actorkey", actorkey))
        else:
            self.ActionLog(f"{self.player} inspects {go}")
            return (True, f"{actor} CAN SEE {go}", ("gokey", gokey, "actorkey", actorkey))

    def ActionMove(self, gokey: list, destinationkey: list, actorkey: list):
        go = self.scenario.getgo(gokey)
        source = self.scenario.getgo(gokey[:-1])
        destination = self.scenario.getgo(destinationkey)
        if not (destination and source and go): return (False, ("gokey", gokey), "source", gokey[-1], "destination", destinationkey)
        destination.append(source.remove(go)) 

        if go==self.player:
            self.player.location = destination
            self.player.see = destination
            self.ActionLog(f"{self.player} moved to {destination}")
        else:
            self.ActionLog(f"{go} was moved to {destination}")
        #self.networkagent.send(f'move {" ".join(gokey)} on {" ".join(destinationkey)} as {" ".join(actorkey)}')

    def ActionSay(self, message, actorkey):
        actor = self.scenario.getgo(actorkey)
        #self.networkagent.send(f"say ")
        return f"{actor}: {" ".join(message)}"

    def ActionLog(self, log):
        self.action_log += f"{log}\n"
        return (True, f"LOG: {log}")