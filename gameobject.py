class GameObject:
    def __init__(self, name:str, desc:dict) -> None:
        self.name:str = name
        self.desc:dict = desc
        self.container: dict = {}
        self.order = 99
    
    def __str__(self):
        return {self.name: self}
    
    def append(self, gameobject: "GameObject"):
        key = gameobject.name
        self.container.update({key: gameobject})

    def remove(self, gameobject: "GameObject", key: str = None):
        key = gameobject.name if not key else None
        return self.container.pop(key)
    
    def getgo(self, key:list):
        gameobject: GameObject = None
        try:
            if len(key)>1: gameobject = self.container[key[0]].getgo(key[1:])
            else: gameobject = self.container[key[0]]
        except: pass
        return gameobject
    
    
    def Update(self):
        pass

    def Draw(self, indent = 1):
        retur = f"{self.name.capitalize()}: {", ".join([f"{k.capitalize()} is {v}" for k, v in self.desc.items()])}"
        items = self.container.values()
        if len(items)>0:
            retur += '\n'
            for go in self.container.values():
                retur += "".join(["  " for i in range(indent)]) + "|-"
                retur += go.Draw(indent+1)
                retur += '\n' if go.name != list(self.container)[-1] else ""
            
        return retur
        

class Location(GameObject):
    def __init__(self, name: str, desc: dict) -> None:
        super().__init__(name, desc)
        self.order = 0

class Prop(GameObject):
    def __init__(self, name: str, desc: dict, use) -> None:
        super().__init__(name, desc)
        self.order = 1
        self.Use = use

class Item(Prop):
    def __init__(self, name: str, desc: dict, use) -> None:
        super().__init__(name, desc, use)
        self.order = 2
    pass

class Actor(GameObject):
    def __init__(self, name: str, desc: dict) -> None:
        super().__init__(name, desc)
        self.order = 3
    pass