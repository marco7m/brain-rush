# -*- encoding:utf-8 -*-
import pygame
import time
import os
from src.game_window import GameWindow
from src.end_window import EndWindow
import src.data_harvest as data_harvest

#pygame.init()
pygame.mixer.init()

#pygame.mixer.music.load('sounds/back1.ogg')
#pygame.mixer.music.play(-1)
#pygame.mixer.music.set_volume(0.8)

if not os.path.exists('data'):
    os.makedirs('data')

data_harvest.player_name = 'Jorge'
game_window = GameWindow()
end_window = EndWindow()
