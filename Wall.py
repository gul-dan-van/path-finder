from depends import *
from gameVar import *


class Wall:
    def __init__(self, screen, space, x1, y1, x2, y2, width, collision_type = 0, color=BLUE):
        self.screen = screen
        self.space = space
        self.width = width
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (x1, y1), (x2, y2), width)
        self.shape.elasticity = 1
        self.shape.collision_type = collision_type
        space.add(self.body, self.shape)
        self.c1 = pygame.Vector2(x1,y1)
        self.c2=pygame.Vector2(x2,y2)
        self.color = color

    def draw(self):
        pygame.draw.line(
            self.screen, self.color, self.c1, self.c2, self.width
        )
