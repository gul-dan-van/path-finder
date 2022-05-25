from matplotlib.colors import LightSource
from depends import *
from gameVar import *
from Ball import Ball
from Wall import Wall
import time

from numpy import random


class SpawnArea:
    def __init__(self, rect, color=LIGHT_GREY):
        self.rect = rect
        self.x = rect.centerx
        self.y = rect.centery
        self.center = (self.x, self.y)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


def makeRoom():

    walls = []
    mouse_button_down = False
    spawn = False
    while not spawn:
        clock.tick(fps)

        draw_bg(screen)
        update_bg([walls])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button_down = True
                tempX, tempY = pygame.mouse.get_pos()

            if mouse_button_down and event.type == pygame.MOUSEBUTTONUP:
                mouse_button_down = False
                x, y = pygame.mouse.get_pos()
                walls.append(Wall(screen, space, tempX, tempY, x, y, wall_width))

        keys = pygame.key.get_pressed()

        if keys[K_SPACE]:
            # balls.append(Ball(screen, space))
            spawn = True

        if mouse_button_down == True:
            x, y = pygame.mouse.get_pos()
            pygame.draw.line(screen, BLUE, (tempX, tempY), (x, y), wall_width)

        pygame.display.update()

    return walls


def makeSpawnArea(goal_walls, walls, ball_radius):

    mouse_button_down = False
    made = False
    spawnArea = None
    while not made:
        clock.tick(fps)

        draw_bg(screen)
        update_bg([goal_walls, walls])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button_down = True

            if mouse_button_down:
                x, y = pygame.mouse.get_pos()
                spawnArea = pygame.Rect(
                    x - 2 * ball_radius,
                    y - 2 * ball_radius,
                    ball_radius * 4,
                    ball_radius * 4,
                )

            if mouse_button_down and event.type == pygame.MOUSEBUTTONUP:
                spawnArea = SpawnArea(spawnArea)
                return spawnArea
        if spawnArea:
            pygame.draw.rect(screen, LIGHT_GREY, spawnArea)
        pygame.display.update()

def runMotion(goal_walls, walls, balls, spawnArea, life_span):

    time_stamp1 = time.time()

    run = True
    while run:
        time_stamp2 = time.time()
        if time_stamp2 - time_stamp1 > life_span:
            return

        clock.tick(fps)
        space.step(1 / fps)

        draw_bg(screen)
        update_bg(
            [
                spawnArea,
                goal_walls,
                walls,
                balls,
            ]
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        pygame.display.update()



def random_path(largest_step=150, smallest_step=50, var=70, n_steps=500):
    distribution_range = [*range(smallest_step, largest_step + 1)] + [
        *range(-largest_step, -smallest_step + 1)
    ]
    n = len(distribution_range)

    path = []
    for i, j in zip(
        random.normal(n // 2, var, n_steps), random.normal(n // 2, var, n_steps)
    ):
        if i < 0:
            i = 0
        if i >= n:
            i = n - 1
        if j < 0:
            j = 0
        if j >= n:
            j = n - 1

        path += [(distribution_range[int(i)], distribution_range[int(j)])]

    return path


def generate_balls(balls_cnt, spawnArea,goal_walls, max_step_size=150, min_step_size=50, var=70, steps_n=500, chaos = True):
    def no_collision(arbiter, space, data):
        return False

    balls = []
    paths = [random_path(max_step_size, min_step_size, var, steps_n) for _ in range(balls_cnt)]
    handlers = []
    for i in range(1, balls_cnt + 1):
        if chaos:
            ball = Ball(
                screen, space, spawnArea.x, spawnArea.y,goal_walls, collision_type=i, paths=paths[i - 1],rad= ball_radius
            )
        else:
            ball = Ball(
                screen, space, spawnArea.x, spawnArea.y,goal_walls, collision_type=i,rad= ball_radius
            )
        balls.append(ball)
        for j in range(1, balls_cnt + 1):
            h1 = space.add_collision_handler(i, j)
            h1.begin = no_collision
            handlers.append(h1)

        h2 = space.add_collision_handler(i, 100)
        h2.begin = ball.pause
        handlers.append(h2)

    return balls


def draw_bg(screen):
    screen.fill(BLACK)


def update_bg(args):
    for arg in args:
        if type(arg) == list:
            for a in arg:
                a.draw()
            if len(arg)>0 and type(arg[0])==Ball:
                center_n = ( int(sum(x.body.position.x for x in arg)/len(arg)), int(sum(x.body.position.y for x in arg)/len(arg)) )
                pygame.draw.circle(screen,LIGHT_GREY,center_n,10)    

        else:
            arg.draw()


def setupStage():

    goal_walls = [
        Wall(screen, space, 0, 0, 0, screen_height, 2 * wall_width, 100, RED),
        # Wall(screen, space, 0, 0, screen_width, 0, 2 * wall_width, 100, RED),
        # Wall(
        #     screen,
        #     space,
        #     0,
        #     screen_height,
        #     screen_width,
        #     screen_height,
        #     2 * wall_width,
        #     100,
        #     RED,
        # ),
        # Wall(
        #     screen,
        #     space,
        #     screen_width,
        #     0,
        #     screen_width,
        #     screen_height,
        #     2 * wall_width,
        #     100,
        #     RED,
        # ),
    ]

    walls = makeRoom()
    spawnArea = makeSpawnArea(goal_walls, walls, ball_radius)

    return goal_walls, walls, spawnArea
