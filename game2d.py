import pygame
from game import Game, Scene
from networkagent import NetworkAgent
from scenario import scenario1
class Game2d(Game):
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


class Scene2d(Scene):
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