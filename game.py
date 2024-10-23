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

def CharacterCreator(name = None):
    name = input(f"Character Name:\n> ") if not name else name
    return Player(name=name, desc={f"{name}": "Person"}, location=None)

class Game:
    def __init__(self, networkagent:NetworkAgent, player: Player) -> None:
        self.networkagent:NetworkAgent = networkagent()
        self.debug = ""
        self.input_suggest = ""
        self.input_cursor = 0
        self.input = ""
        self.input_response = ""
        self.action_log = ""
        self.timer = Timer(0.1)

        self.scenario:Scenario = scenario_TheCabin(self) #networkagent.connect(scenario_TheCabin(self))
        #self.scenario.Save()

        self.player = player #Player("player", {"player": "Person"}, list(self.scenario.container.values())[0])
        self.player.location = list(self.scenario.container.values())[0]
        self.player.see = self.player.location
        self.networkagent.data_send(f"add {player.name} on {list(self.scenario.container.values())[0]} as PLAYER")
        lobby = True
        #self.ActionAdd
        #networkagent.getCommand()
        #self.player.location.append(self.player)
        

        self.game_loop = True
        while self.game_loop:
            #self.Draw() if self.draw else None
            self.Update()

        print('\033[?25h')
        os.system('cls' if os.name == 'nt' else 'clear')

    def setResponse(self, response):
        self.input_response = response
        return self.input_response
    
    def Draw(self):
        self.draw = False
        #time.sleep(self.timer.step)
        self.timer.Tick()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.player.see.Draw(), end="\n\n")
        print(self.action_log, end="")
        print(f"\n> {self.input}", end=f"\033[107m"+ "\033[0m"+ "\n"+ "\033[?25l") #'\033[?25h'
        print(self.debug) if DEBUG else None

    def Update(self):
        systemcommand = self.networkagent.getCommand()
        key = b""
        try:
            if msvcrt.kbhit():
                key = msvcrt.getch()
        except KeyboardInterrupt:
            self.game_loop = False
            return
        if key in b'' and not systemcommand:
            return False
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
            self.debug = self.networkagent.data_send(f"{self.input} as {f"{self.player.location} {self.player}"}")
            #self.debug = self.Action(data)
            #self.debug = self.Action(f"{self.input} as {f"{self.player.location} {self.player}"}", False)
            self.input = ""
            
        self.debug = self.Action(systemcommand) if systemcommand else None
        self.Draw()

    ACTION_CMD_STOP = ['stop']
    ACTION_CMD_MOVE = ['move', 'go']
    ACTION_CMD_ADD = ['add']
    ACTION_CMD_JOIN = ['join']
    ACTION_CMD_USE = ['use']
    ACTION_CMD_SEE = ['see', 'inspect']
    ACTION_CMD_WAIT = [' ', 'wait']
    ACTION_CMD_SAY = ['say']
    ACTION_CMDS = ACTION_CMD_STOP+ACTION_CMD_MOVE+ACTION_CMD_ADD+ACTION_CMD_JOIN+ACTION_CMD_USE+ACTION_CMD_SEE+ACTION_CMD_WAIT+ACTION_CMD_SAY
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
        actor = self.scenario.getgo(actorkey) if actorkey else None
        if command not in self.ACTION_CMDS:
            self.ActionLog(f"{actor} can't '{command}'")
            return (False, "NOT IN CMDS")

        if command in self.ACTION_CMD_STOP:
            print('\033[?25h'+'\033[0m')
            os.system('cls' if os.name == 'nt' else 'clear')
            os._exit(0)

        if command in self.ACTION_CMD_USE:
            if gokey and actorkey:
                return self.ActionUse(gokey=gokey, targetkey=targetkey,actorkey=actorkey)
        
        if command in self.ACTION_CMD_SEE:
            if actorkey:
                return self.ActionSee(gokey=gokey, actorkey=actorkey)

        if command in self.ACTION_CMD_MOVE:
            if gokey and targetkey and actorkey:
                return self.ActionMove(gokey=gokey, destinationkey=targetkey, actorkey=actorkey)
        
        if command in self.ACTION_CMD_ADD:
            if gokey and targetkey and actorkey:
                return self.ActionAdd(gokey, targetkey, actorkey)
            
        if command in self.ACTION_CMD_JOIN:
            if gokey and targetkey and actorkey:
                return self.ActionJoin(targetkey, gokey)
        
        if command in self.ACTION_CMD_SAY:
            if gokey and actorkey:
                return self.ActionLog(self.ActionSay(gokey, actorkey))


        self.ActionLog(f"{actor} was idle")
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
        
        if actor.name == self.player.name:
            if go:
                self.player.see = go
                self.ActionLog(f"{self.player} inspects {go}")
                return (True, f"CAN SEE {go}", ("gokey", gokey, "actorkey", actorkey))
            else:
                self.ActionLog(f"{self.player} can't inspect {go if go else "'nothing'"}")
                return (False, f"CAN'T SEE {go}", ("gokey", gokey, "actorkey", actorkey))
        else:
            self.ActionLog(f"{actor} inspects {go}")
            return (True, f"{actor} CAN SEE {go}", ("gokey", gokey, "actorkey", actorkey))

    def ActionMove(self, gokey: list, destinationkey: list, actorkey: list):
        go = self.scenario.getgo(gokey)
        source = self.scenario.getgo(gokey[:-1])
        destination = self.scenario.getgo(destinationkey)
        if not (destination and source and go): return (False, ("gokey", gokey), "source", gokey[-1], "destination", destinationkey)
        destination.append(source.remove(go)) 

        if go.name==self.player.name:
            self.player.location = destination
            self.player.see = destination
            self.ActionLog(f"{self.player} moved to {destination}")
        else:
            self.ActionLog(f"{go} was moved to {destination}")
        #self.networkagent.send(f'move {" ".join(gokey)} on {" ".join(destinationkey)} as {" ".join(actorkey)}')

    def ActionAdd(self, data:str, locationkey:str, type:str):
        location = self.scenario.getgo(locationkey)
        go = GameObject(name=data[0], desc={"type":f"{type[0]}"})
        location.append(go)

    def ActionSay(self, message, actorkey):
        actor = self.scenario.getgo(actorkey)
        #self.networkagent.send(f"say ")
        return f"{actor}: {" ".join(message)}"

    def ActionLog(self, log):
        self.action_log += f"{log}\n"
        return (True, f"LOG: {log}")