import pygame

SCALE = 2
winxy = (500*SCALE,500*SCALE)
window = pygame.display.set_mode(winxy)
pygame.display.set_caption("ItsaGame")

FRICTION = 1#0.98
ACCMAX = 6

class XY:
    def __init__(self, x:int = 0, y:int = 0) -> None:
        self.x = x
        self.y = y

    def move(self, x = 0, y = 0):
        self.x += x
        self.y += y

    def moveabs(self, x = 0, y = 0):
        self.x = x
        self.y = y

class Camera:
    def __init__(self, position:XY, offset:XY) -> None:
        self.position = position
        self.offset = offset

class Player:
    def __init__(self, position: XY) -> None:
        self.position = position
        self.size = 10
        self.velocity = XY(0,0)
        self.speed = 1

        self.color = (255, 0, 0)

    def draw(self, window, camera:Camera):
        pygame.draw.circle(surface=window, color=self.color, center=(self.position.x-camera.position.x, self.position.y-camera.position.y), radius=self.size)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.move(-self.speed, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.move(self.speed, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.move(0, -self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.move(0, self.speed)

        self.position.move(self.velocity.x, self.velocity.y)
        
        self.velocity.moveabs(
            min(max(self.velocity.x*FRICTION, -ACCMAX), ACCMAX),
            min(max(self.velocity.y*FRICTION, -ACCMAX), ACCMAX)
            )
        #self.velocity.x *= FRICTION
        #self.velocity.y *= FRICTION

        self.position.moveabs(
            min(max(self.position.x, self.size), window.get_width()-self.size),
            min(max(self.position.y, self.size), window.get_height()-self.size)
            )


def redrawWindow(player: Player, camera:Camera):
    window.fill(rect=(0,0, window.get_width(), window.get_height()),color=(0,0,0))
    window.fill(rect=(0-camera.position.x,0-camera.position.y, window.get_width()-camera.position.x, window.get_height()-camera.position.y),color=(200,200,200))
    pygame.draw.circle(window, (0, 0, 200), (20-camera.position.x, 20-camera.position.y), 10)
    player.draw(window, camera)
    pygame.display.update()

def main():
    player = Player(XY(20, 20))
    camera = Camera(XY(0,0), XY(-window.get_width()/2, -window.get_height()/2))
    gameloop = True
    clock = pygame.time.Clock()

    while gameloop:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        camera.position.moveabs(player.position.x+camera.offset.x, player.position.y+camera.offset.y)
        player.move()
        redrawWindow(player, camera)


main()