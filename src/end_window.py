# -*- encoding:utf-8 -*-
import os
import pygame
import src.const as CONST


_image_library = {}
class EndWindow:
    def __init__(self):
        
        screen = pygame.display.set_mode((CONST.DISPLAY_SIZE_X, CONST.DISPLAY_SIZE_Y))
        done = False
        clock = pygame.time.Clock()

        # loop principal
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
           
            screen.fill((255, 255, 255))
            pygame.display.flip()
            clock.tick(60)

