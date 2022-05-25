from depends import *
from gameVar import *
from numpy import dot
from numpy.linalg import norm


class Ball:
    total_cnt=10

    def __init__(
        self,
        screen,
        space,
        x,
        y,
        goal_walls,
        collision_type=1,
        paths=None,
        randomness_index = 7,
        rad=10,
        color=RED,
    ):
        self.screen = screen
        self.space = space
        self.body = pymunk.Body()
        self.paths = paths
        # self.body.velocity = 300, 300
        velocity = pygame.Vector2(random.randint(-300,300), random.randint(-300,300))
        self.body.velocity = list(velocity.normalize()*300)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, rad)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = collision_type
        self.rad = rad
        space.add(self.body, self.shape)
        self.color = color
        self.randomness_index = randomness_index
        self.goal_walls = goal_walls

        self.should_pause = False
        self.counter = 0
        self.best = 100000
        self.prev_score = -1
        self.new_score = 0
        self.total_cnt+=1


    def draw(self):
        if self.should_pause:
            self.body.velocity = 0, 0
        elif self.counter%self.randomness_index==0 and self.paths!=None:
            self.body.velocity = self.paths[min(self.counter, len(self.paths) - 1)]
        self.counter += 1

        x, y = map(int, self.body.position)
        pygame.draw.circle(self.screen, self.color, (x, y), self.rad)

        self.distance_from_goal()

    def distance_from_goal(self):
        p1 = self.body.position
        for wall in self.goal_walls:
            p2 = wall.c1
            p3 = wall.c2

            v1 = p1 - p2
            v2 = p1 - p3
            v3 = p2 - p3

            cos1 = dot(v1,v3)/norm(v3)/norm(v1)
            cos2 = dot(v2,v3)/norm(v3)/norm(v2)
            sin1 = (1-cos1**2)**0.5
            sin2 = (1-cos2**2)**0.5

            self.best = min(min(abs(sin1*norm(v1)), abs(abs(sin2*norm(v2)))),self.best)

    def pause(self, arbiter, space, data):
        self.should_pause = True
        self.body.velocity = 0, 0
        print('ehre')

        return True

    def remove(self):
        space.remove(self.shape, self.body)
