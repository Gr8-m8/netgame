import json

class GameObject:
    def __init__(self, name:str, desc:dict) -> None:
        self.name:str = name
        self.desc:dict = desc
        self.container: dict = {}
        self.type = GAMEOBJECT
    
    def __str__(self):
        return self.name
    
    def append(self, gameobject: "GameObject"):
        key = gameobject.name
        self.container.update({key: gameobject})

    def remove(self, gameobject: "GameObject"):
        key = gameobject.name
        return self.container.pop(key)
    
    def getgo(self, key:list):
        gameobject: GameObject = None
        if len(key)>1: gameobject = self.container[key[0]].getgo(key[1:])
        else: gameobject = self.container[key[0]] if key[0] in self.container else None
        return gameobject
    
    
    def Update(self):
        pass

    def Draw(self, indent = 0):
        basicdesclist = [f'{k.capitalize()} is {v}' for k, v in self.desc.items()]
        retur = f"{self.name.capitalize()}: {', '.join(basicdesclist)}"
        items = self.container.values()
        if len(items)>0:
            retur += '\n'
            for go in self.container.values():
                retur += "".join(["  " for i in range(indent)]) + "|-"
                retur += go.Draw(indent+1)
                retur += '\n' if go.name != list(self.container)[-1] else ""
            
        return retur
    
    def toJSON(self):
        key = self.name
        value = {
            "type": self.type[0],
            "name": self.name,
            "desc": self.desc,
            "container": [{i.toJSON()} for i in self.container.values()]
        }
        return json.dumps(f"{key}:{value}", indent=4,)

    @staticmethod
    def fromJSON(self, dataraw):
        data = json.load(dataraw)
        type = data['type']
        name = data['name']
        desc = json.loads(data['desc'])
        container = {}
        [container.update({k: v.fromJSON()}) for k, v in json.load(data['container'])]
        
        
        

class Location(GameObject):
    def __init__(self, name: str, desc: dict) -> None:
        super().__init__(name, desc)
        self.type = LOCATION

class Prop(GameObject):
    def __init__(self, name: str, desc: dict, use) -> None:
        super().__init__(name, desc)
        self.type = PROP
        self.Use = use

class Item(Prop):
    def __init__(self, name: str, desc: dict, use) -> None:
        super().__init__(name, desc, use)
        self.type = ITEM
    pass

class Actor(GameObject):
    def __init__(self, name: str, desc: dict) -> None:
        super().__init__(name, desc)
        self.type = ACTOR
    pass

GAMEOBJECT = ("GameObject", GameObject)
LOCATION = ("Location", Location)
PROP = ("Prop", Prop)
ITEM = ("Item", Item)
ACTOR = ("Actor", Actor)