import json
#from game import Game
from gameobject import GameObject, Location, Prop, Actor

class Scenario(GameObject):
    DATAPATH = "data/"
    def __init__(self, name: str, desc: dict) -> None:
        super().__init__(name, desc)

    def Save(self):
        try:
            datafile = open(f"{self.DATAPATH}{"_".join(self.name.split(' '))}.scenario", "w")
            datafile.writelines(self.toJSON())
            datafile.close()
        except: pass

    def Load(self):
        pass

def scenario_TheCabin(game):
    scenario = Scenario("The Cabin", {"desc":"You are lost on a cold night and find a cabin"})
    #scenario.update(pack(Actor("player", {"player": "Person"})))
    scenario.append(Location("outside", {"outside": "dark and cold"}))
    scenario.append(Location("house", {"room": "warm and cozy"}))
    
    scenario.getgo(['outside']).append(Prop("tree", {"leaves": "Green", "branches": "sturdy"}, lambda target, actor: game.ActionLog(f"{actor} climbs on Tree")))
    scenario.getgo(['outside']).append(Prop("house", {"inside": "Homely"}, lambda target, actor: game.ActionLog(f"The house has a Door that can be Used")))
    scenario.getgo(['outside', "house"]).append(Prop("door", {"color": "Green"}, lambda target, actor: game.Action(f"move outside {actor} on house as outside {actor}")))
    scenario.getgo(['outside', "house", "door"]).append(Prop("window", {"glass": "Green"}, lambda target, actor: None))

    scenario.getgo(['house']).append(Prop("chair", {"chair": "wooden"}, lambda target, actor: game.ActionLog(f"{actor} sits on Chair")))
    scenario.getgo(['house']).append(Prop("door", {"door": "Green", "outside": "Cold and Dark"}, lambda target, actor: game.Action(f"move house {actor} on outside as house {actor}")))

    return scenario