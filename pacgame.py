# -*- encoding:utf-8 -*-
import pygame
import time
#import pandas as pd
from src.game_window import GameWindow
from src.end_window import EndWindow

#pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('sounds/back1.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.8)

game_window = GameWindow()
end_window = EndWindow()
