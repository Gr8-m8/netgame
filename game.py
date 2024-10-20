import pygame
from networkagent import NetworkAgent

class Game:
    def __init__(self, networkagent:NetworkAgent, winxy: tuple) -> None:
        self.networkagent:NetworkAgent = networkagent
        self.winxySCALE = winxy[2]
        self.winxy:tuple = (winxy[0] * self.winxySCALE, winxy[1]*self.winxySCALE)
        self.window = pygame.display.set_mode(self.winxy)
        pygame.display.set_caption("Game")
        pygame.font.init()
        
        self.scene = scenario1()
        
        FONTSIZE = 24
        self.font = pygame.font.SysFont("monospace", int(16))
        self.clock = pygame.time.Clock()
        self.gameloop = True
        while self.gameloop:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameloop = False
                    pygame.quit()
            
            self.Update()
            self.Draw()

    def Draw(self):
        self.window.fill(rect=(0,0, self.winxy[0], self.winxy[1]),color=(0,0,0))
        pygame.draw.rect(self.window, (50, 50 ,50), (self.winxy[0]/self.winxySCALE, self.winxy[1]-4*(self.winxy[1]/self.winxySCALE), self.winxy[0]-2*(self.winxy[0]/self.winxySCALE), 3*self.winxy[1]/self.winxySCALE))
        self.scene.Draw(self.window, self.font)
        pygame.display.update()

    def Update(self):
        keys = pygame.key.get_pressed()

class GameObject:
    def __init__(self, name:str, desc:dict) -> None:
        self.name:str = name
        self.desc:dict = desc
        self.order = 99
    pass

class Location(GameObject):
    def __init__(self, name: str, desc: dict) -> None:
        super().__init__(name, desc)
        self.order = 0
        self.props:dict={}
        self.items:dict={}
        self.actors:dict={}

    def append(self, gameobject: GameObject, key = None):
        key = gameobject.name if not key else None
        if isinstance(gameobject, GameObject):
            if isinstance(gameobject, Prop):
                self.props.update({key: gameobject})
            if isinstance(gameobject, Item):
                self.items.update({key: gameobject})
            if isinstance(gameobject, Actor):
                self.actors.update({key: gameobject})

    def remove(self, gameobject: GameObject):
        if isinstance(gameobject, GameObject):
            if isinstance(gameobject, Prop):
                self.props.pop(gameobject.name)
            if isinstance(gameobject, Item):
                self.items.pop(gameobject.name)
            if isinstance(gameobject, Actor):
                self.actors.pop(gameobject.name)

class Prop(GameObject):
    def __init__(self, name: str, desc: dict, use) -> None:
        super().__init__(name, desc)
        self.order = 1
        self.use = use

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

class Scene:
    def __init__(self, player: Actor, location: Location) -> None:
        self.player:Actor = player
        self.location:Location = location

    def go(self, location: Location):
        self.location = location

    def Draw(self, canvas, font):
        #self.font.render('TEXT RENDER', True, (255,255,255))
        #self.window.blit(text, (20, 20))
        x = y = s = 16
        texts = []
        scenetitle = font.render(f'{self.location.name}{self.location.desc}', True, (255,255,255))
        canvas.blit(scenetitle, (x, y))
        y+=s
        #scenedescription = font.render(f'{self.location.name}', True, (255,255,255))
        #canvas.blit(scenetitle, (x, y))
        #y+=s
        for k,v in self.location.props.items()|self.location.items.items()|self.location.actors.items():
            text = font.render(f'{k}: {v.desc}', True, (255,255,255))
            canvas.blit(text, (x, y))
            y+=s
            texts.append(text)
        

def pack(key, value):
    return {key:value}


def scenario1():
    location_Outside = Location("Outside", {"outside": "dark and cold"})
    location_Outside.append(Prop("Tree", {"leaves": "Green", "branches": "sturdy"}, lambda: print(f"{scene.player.name} Climbs on Tree")))
    location_Outside.append(Prop("House", {"Door": "Green", "Inside": "Homely"}, lambda: scene.go(location_House)))

    location_House = Location("House", {"Room": "warm and cozy"})
    location_House.append(Prop("Chair", {"Chair": "wooden"}, lambda: print(f"{scene.player.name} Sits on Chair")))
    location_House.append(Prop("Door", {"Door": "Green", "Outside": "Cold and Dark"}, lambda: scene.go(location_Outside)))


    scene = Scene(Actor("Player", {"player": "Person"}), location_Outside)
    return scene