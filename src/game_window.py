# -*- encoding:utf-8 -*-
import os
import pygame
import random
import datetime
import pandas as pd
from src.position import Position
from src.hero import Zombie
from src.ball import Ball
import src.const as CONST
import src.data_harvest as data_harvest


_image_library = {}

class GameWindow:
    def __init__(self):
       
        pygame.font.init()

        # coloca o background
        background = pygame.image.load("img/background2.jpg")

        game_font = pygame.font.SysFont('Comic Sans MS', 45)
        placar_font = pygame.font.SysFont('Comic Sans MS', 20)

        score = 0
        score_text_surface = game_font.render('Pontos: '+str(score), False,(255,255,255))

        placar = 35
        name = "Carlos"
        placar_text_surface = placar_font.render('Melhor Jogador: ' + name + ' - '+str(placar), False, (0,0,255))

        def get_image(path):
            global _image_library
            image = _image_library.get(path)
            if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
            return image

        # variaveis do heroi
        hero = Zombie()
        hero_group = pygame.sprite.Group(hero)

        # variaveis da bolinha
        ball = Ball()
        ball.set_random_position(hero)

        #Timer Novo (bug do mouse)
        start_ticks = pygame.time.get_ticks()
        time_left = CONST.GAME_TIME

        mirror = False
        alreadySaid = [False, False, False, False, False, False] 
        opc0 = opc1 = opc2 = opc3 = 0

        time_text_surface = game_font.render(str(time_left), False,(255,255,255))
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        screen = pygame.display.set_mode((CONST.DISPLAY_SIZE_X, CONST.DISPLAY_SIZE_Y), pygame.FULLSCREEN)
#        screen = pygame.display.set_mode((CONST.DISPLAY_SIZE_X, CONST.DISPLAY_SIZE_Y))
        done = False
        clock = pygame.time.Clock()

        # loop principal
        while not done:
            for event in pygame.event.get():
                print event
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        data_harvest.pressed_keys.append(['PRESS_K_UP',datetime.datetime.now()])
                        hero.shuffle_random_direction()
                    if event.key == pygame.K_DOWN: 
                        data_harvest.pressed_keys.append(['PRESS_K_DOWN',datetime.datetime.now()])
                        hero.shuffle_random_direction()
                    if event.key == pygame.K_LEFT: 
                        data_harvest.pressed_keys.append(['PRESS_K_LEFT',datetime.datetime.now()])
                        hero.shuffle_random_direction()
                    if event.key == pygame.K_RIGHT:
                        data_harvest.pressed_keys.append(['PRESS_K_RIGHT',datetime.datetime.now()])
                        hero.shuffle_random_direction()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        data_harvest.pressed_keys.append(['RELEASE_K_UP',datetime.datetime.now()])
                    if event.key == pygame.K_DOWN: 
                        data_harvest.pressed_keys.append(['RELEASE_K_DOWN',datetime.datetime.now()])
                    if event.key == pygame.K_LEFT: 
                        data_harvest.pressed_keys.append(['RELEASE_K_LEFT',datetime.datetime.now()])
                    if event.key == pygame.K_RIGHT:
                        data_harvest.pressed_keys.append(['RELEASE_K_RIGHT',datetime.datetime.now()])

                if event.type == pygame.USEREVENT:
                    if time_left > 0:
                        seconds=(pygame.time.get_ticks()-start_ticks)/1000

                        # configura as probabilidades de bug
                        if seconds < 8:
                            error_probability = 0
                        elif seconds < 25:
                            error_probability = random.randint(0,15)
                        elif seconds < 40:
                            error_probability = random.randint(0,11)
                        else:
                            error_probability = random.randint(0,7)
 
                        if error_probability == 1:
                            hero.random_movement()

                        if error_probability == 2:
                            hero.slow_down()
                         
                        if error_probability == 3:
                            hero.human_error()
                          
                        if (seconds % 5) == 0:
                            hero.zombie_scream()

                        #countDown sound     
                        if (time_left == 6):
                            for i in range (0,6):
                                alreadySaid[i] = False
                        if (time_left == 6 and alreadySaid[time_left-1] == False):
                            countdown = pygame.mixer.Sound('src/sounds/5.wav')
                            alreadySaid[time_left-1] = True
                            countdown.play()
                        if (time_left == 5 and alreadySaid[time_left-1] == False) :
                            countdown = pygame.mixer.Sound('src/sounds/4.wav')
                            alreadySaid[time_left-1] = True
                            countdown.play()
                        if (time_left == 4 and alreadySaid[time_left-1] == False):
                            countdown = pygame.mixer.Sound('src/sounds/3.wav')
                            alreadySaid[time_left-1] = True
                            countdown.play()
                        if (time_left == 3 and alreadySaid[time_left-1] == False):
                            countdown = pygame.mixer.Sound('src/sounds/2.wav')
                            alreadySaid[time_left-1] = True
                            countdown.play()
                        if (time_left == 2 and alreadySaid[time_left-1] == False):
                            countdown = pygame.mixer.Sound('src/sounds/1.wav')
                            alreadySaid[time_left-1] = True
                            countdown.play()
                        if (time_left == 1 and alreadySaid[time_left-1] == False):
                            countdown = pygame.mixer.Sound('src/sounds/0.wav')
                            alreadySaid[time_left-1] = True
                            countdown.play()
                        time_left -= 1
                    else:
                        done = True
                        
                        # salva os dados coletados
                        pd.DataFrame(data_harvest.pressed_keys).to_csv("data/pressed_keys.csv",index=None)
                        pd.DataFrame(data_harvest.random_events).to_csv("data/random_events.csv",index=None)
                        pd.DataFrame(data_harvest.hero_movement).to_csv("data/hero_movement.csv",index=None)
 
            
            # pega as teclas pressionadas
            pressed = pygame.key.get_pressed()
            
            if pressed[pygame.K_ESCAPE]:
                quit(0)

            else:
                if pressed[pygame.K_UP]:
                    hero.move_up()
                elif pressed[pygame.K_DOWN]:
                    hero.move_down()
                elif pressed[pygame.K_LEFT]:
                    hero.move_left()
                elif pressed[pygame.K_RIGHT]:
                    hero.move_right()
            # checa se a bola está dentro do heroi
            if hero.has_ball_inside(ball):
                data_harvest.random_events.append(['ZOMBIE_EATS',datetime.datetime.now()])
                score += 1
                score_text_surface = game_font.render('Pontos: ' + str(score), False,(255,255,255))
                hero.bite()
                ball.set_random_position(hero)
                time_left += 2

            # atualiza o tempo
            if time_left < 6:
                time_text_surface = game_font.render(str(time_left), False,(255,0,0))
            else:
                time_text_surface = game_font.render(str(time_left), False,(255,255,255))

            screen.fill((0, 0, 0))
            screen.blit(background,(0,70))
            hero_group.update()
            hero_group.draw(screen)
            screen.blit(get_image('img/cerebro.png'), (ball.pos.x, ball.pos.y))
            screen.blit(score_text_surface,(CONST.DISPLAY_SIZE_X - 250,10))
            screen.blit(time_text_surface,(CONST.DISPLAY_SIZE_X/2 - 0,10))
            screen.blit(placar_text_surface,(CONST.DISPLAY_SIZE_X/2 - 450,30))
            pygame.display.flip()
            clock.tick(60)
