from depends import *

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 700
wall_width = 5
ball_radius = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREY = (220, 220, 220)
DARK_GREY = (30, 30, 30)
PURPLE = (128, 0, 128)
VIOLET = (238, 130, 238)
YELLOW = (255, 255, 0)
DARK_YELLOW = (204, 204, 0)
CYAN = (0, 255, 255)

screen = pygame.display.set_mode((screen_width, screen_height))
space = pymunk.Space()
