from importlib_metadata import distribution
from depends import *
from gameVar import *
from Ball import Ball
from Wall import Wall
from gameFunc import *
import time
from models import *


model_type = 'linear'
balls_cnt = 30
epochs = 100
life_span = 1

pygame.init()
pygame.display.set_caption("Bonse")

if model_type=='chaos':
    model = ChaosModel(balls_cnt, life_span, epochs)
else:
    model = LinearModel(balls_cnt, life_span, epochs)

model.train()
pygame.quit()
