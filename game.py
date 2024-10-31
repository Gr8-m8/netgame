import select
import sys
import time
import os

from getch import getch
from networkagent import NetworkAgent, networkdata
from gameobject import GameObject, Location, Prop, Item, Actor
from scenario import Scenario, scenario_TheCabin

def iswindows():
    return True if os.name == 'nt' else False

DEBUG = True
        

class Timer:
    def __init__(self, step) -> None:
        self.time = 0
        self.step = step


    def Tick(self):
        self.time += self.step

class Player(Actor):
    def __init__(self, name: str, desc: dict, location:Location = None, see: GameObject = None) -> None:
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

        #self.SendScenario()
        self.scenario:Scenario = scenario_TheCabin(self) #networkagent.connect(scenario_TheCabin(self))
        #self.scenario.Save()

        self.networkagent.data_send(networkdata.command(f"add {player.name} on {list(self.scenario.container.values())[0]} as Player"))
        self.player = player
        self.player.location = list(self.scenario.container.values())[0]
        self.player.see = self.player.location
        lobby = True

        #try:
        if True:
            self.game_loop = True
            while self.game_loop:
                #self.Draw() #if not iswindows() else None
                self.Update()
        #except Exception as e:
        #    exc_type, exc_obj, exc_tb = sys.exc_info()
        #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #    self.Exit(f"GAME LOOP FAIL\nREASON: {e}\nAt:{exc_type, fname, exc_tb.tb_lineno}")

        print('\033[?25h')
        os.system('cls' if os.name == 'nt' else 'clear')

    def Exit(self, reason: str = None):
        print('\033[?25h'+'\033[0m')
        os.system('cls' if os.name == 'nt' else 'clear')
        print(reason) if reason else None
        os._exit(0)

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
        print(f"\n> {self.input}\033[107m \033[0m \033[?25l") #'\033[?25h'
        print(self.debug) if DEBUG else None

    def keyboard(self):
        key = getch.readkey()

        if key in b'':
            return False
        
        KEYS_APPEND = b'qwertyuiopasdfghjklzxcvbnm ,.!?"'
        if key in KEYS_APPEND:
            self.input+= key.decode()
            return True
        
        KEYS_REPLACE =b'123456789+-'
        if key in KEYS_REPLACE:
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
            return True

        KEYS_ACTIONS_ARROW = [b'H', b'P', b'K', b'M']
        KEYS_ACTIONS_BACKSPACE = [b'\x08', b'\x7f']
        KEYS_ACTIONS_TAB = [b'\t']
        KEYS_ACTIONS_RETURN = [b'\r', b'\n']
        KEYS_ACTIONS_ESC = [b'\x1b']
        KEYS_ACTIONS = KEYS_ACTIONS_ARROW+KEYS_ACTIONS_BACKSPACE+KEYS_ACTIONS_TAB+KEYS_ACTIONS_RETURN+KEYS_ACTIONS_ESC
        if key in KEYS_ACTIONS:
            if key == b'H': self.input+="" #UP
            if key == b'P': self.input+="" #DOWN
            if key == b'K': self.input+="" #LEFT
            if key == b'M': self.input+="" #RIGHT
            if key in KEYS_ACTIONS_BACKSPACE:
                self.input = self.input[:-1]
            if key in KEYS_ACTIONS_TAB:
                pass
            if key in KEYS_ACTIONS_RETURN:
                self.action_log = ""
                self.networkagent.data_send(networkdata.command(f"{self.input} as {self.player.location} {self.player}"))
                self.input = ""
            if key in KEYS_ACTIONS_ESC:
                self.input = ""
            return True


    def Update(self):
        systemcommand = self.networkagent.getCommand()
        key = self.keyboard()
        
        self.Action(systemcommand) if systemcommand else None
        self.Draw() if systemcommand or key else None

    ACTION_CMD_STOP = ['stop']
    ACTION_CMD_MOVE = ['move', 'go']
    ACTION_CMD_ADD = ['add']
    ACTION_CMD_USE = ['use']
    ACTION_CMD_SEE = ['see', 'inspect']
    ACTION_CMD_WAIT = [' ', 'wait']
    ACTION_CMD_SAY = ['say']
    ACTION_CMDS = ACTION_CMD_STOP+ACTION_CMD_MOVE+ACTION_CMD_ADD+ACTION_CMD_USE+ACTION_CMD_SEE+ACTION_CMD_WAIT+ACTION_CMD_SAY
    def Action(self, qcommand:dict):
        command:str = qcommand[networkdata.KEY_COMMAND] if networkdata.KEY_COMMAND in qcommand.keys() else None
        gokey = qcommand[command] if command in qcommand.keys() else None
        targetkey = qcommand[networkdata.TAG_TARGET] if networkdata.TAG_TARGET in qcommand.keys() else None
        actorkey = qcommand[networkdata.TAG_ACTOR]  if networkdata.TAG_ACTOR in qcommand.keys() else None

        actor = self.scenario.getgo(actorkey)

        
        if command not in self.ACTION_CMDS:
            self.ActionLog(f"{actor} can't '{command}'")
            return (False, "NOT IN CMDS")

        if command in self.ACTION_CMD_STOP:
            self.Exit("Stop")

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

        if command in self.ACTION_CMD_SAY:
            if gokey and actorkey:
                return self.ActionLog(self.ActionSay(gokey, actorkey))


        self.ActionLog(f"{actor} was idle")
        return (False, "NOT ACTIVATED", (command, gokey, targetkey, actorkey))

    def ActionUse(self, gokey: list, targetkey:list, actorkey: list):
        actor: Actor = self.scenario.getgo(actorkey)
        gokey = actorkey[:-1]+gokey[:]
        go: Prop = self.scenario.getgo(gokey)
        print(actorkey, gokey, targetkey)
        target: GameObject = self.scenario.getgo(targetkey) if targetkey else None

        if isinstance(go, Prop):
            go.Use(target, actor)
            return (True, f"{actor} USED {go}")
        else:
            nothingstr = "'nothing'"
            self.ActionLog(f"{actor} can't use {go if go else nothingstr}")
            return (False, "UNUSABLE")

    def ActionSee(self, gokey: list, actorkey: list):
        actor = self.scenario.getgo(actorkey)
        gokey = [i for i in actorkey[:-1]+gokey[:] if i]
        go = self.scenario.getgo(gokey) #if gokey[-1]=='' else self.scenario.getgo(self.player.location)

        if actor.name == self.player.name:
            if go:
                self.player.see = go
                self.ActionLog(f"{self.player} inspects {go}")
                return (True, f"CAN SEE {go}", ("gokey", gokey, "actorkey", actorkey))
            else:
                nothingstr = "'nothing'"
                self.ActionLog(f"{self.player} can't inspect {go if go else nothingstr}")
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

    def ActionAdd(self, data:str, locationkey:str, typekey:str):
        location = self.scenario.getgo(locationkey)
        gotype = GameObject
        if typekey == "Location":
            gotype = Location
        if typekey == "Prop":
            gotype = Prop
        if typekey == "Item":
            gotype = Item
        if typekey == "Actior":
            gotype = Actor
        if typekey == "Player":
            gotype = Player
        go = gotype(name=data[0], desc={"type":f"{typekey[0]}"}) if gotype != Player else Player(name=data[0], desc={"type":f"{typekey[0]}"}, location=location, see=location)
        location.append(go)

    def ActionSay(self, message, actorkey):
        actor = self.scenario.getgo(actorkey)
        return f"{actor}: {' '.join(message)}"

    def ActionLog(self, log):
        self.action_log += f"{log}\n"

    def SendScenario(self):
        self.networkagent.data_send(networkdata.scenario(self.scenario))
        return self.scenario