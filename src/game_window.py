# -*- encoding:utf-8 -*-
import os
import pygame
import random
from src.position import Position
from src.hero import Zombie
from src.ball import Ball
import src.const as CONST


_image_library = {}

class GameWindow:
    def __init__(self):
        
        pygame.font.init()
        #pygame.mixer.init()

        # coloca o background
        background = pygame.image.load("img/cemiterio.jpg")

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
        done = False
        clock = pygame.time.Clock()

        # loop principal
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.USEREVENT:
                    if time_left > 0:
                        seconds=(pygame.time.get_ticks()-start_ticks)/1000

                        # só tem possibilidade de bug depois de 8 segundos de jogo
                        if seconds > 8:
                            error_probability = random.randint(0,5)

                            if error_probability == 1:
                                hero.slow_down()
                            if error_probability == 0:
                                hero.random_movement()
                                
                            else:
                                pass
                            if (seconds % 5) == 0:
                                mirror = True
                                opc0 = random.randint(0,3)
                                opc1 = random.randint(0,3)
                                opc2 = random.randint(0,3)
                                opc3 = random.randint(0,3)
                                hero.zombie_error()
                            elif (seconds % 4) == 0:
                                mirror = False
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
            
            # pega as teclas pressionadas
            pressed = pygame.key.get_pressed()
            
            if pressed[pygame.K_ESCAPE]:
                quit(0)

#            if bug:
#                if pressed[pygame.K_UP]:
#                    hero.human_error()
#                elif pressed[pygame.K_DOWN]:
#                    hero.human_error()
#                elif pressed[pygame.K_LEFT]:
#                    hero.human_error()
#                elif pressed[pygame.K_RIGHT]:
#                    hero.human_error()
#            elif mirror:
#                if pressed[pygame.K_UP]:
#                    hero.wrong_way(opc0)
#                elif pressed[pygame.K_DOWN]:
#                    hero.wrong_way(opc1)
#                elif pressed[pygame.K_LEFT]:
#                    hero.wrong_way(opc2)
#                elif pressed[pygame.K_RIGHT]:
#                    hero.wrong_way(opc3)
            else:
                if pressed[pygame.K_UP]:
                    if hero.RANDOM_MOVEMENT:
                        hero.random_movement()
                    else:
                        hero.move_up()
                elif pressed[pygame.K_DOWN]:
                    if hero.RANDOM_MOVEMENT:
                        hero.random_movement()
                    else:
                        hero.move_down()
                elif pressed[pygame.K_LEFT]:
                    if hero.RANDOM_MOVEMENT:
                        hero.random_movement()
                    else:
                        hero.move_left()
                elif pressed[pygame.K_RIGHT]:
                    if hero.RANDOM_MOVEMENT:
                        hero.random_movement()
                    else:
                        hero.move_right()
            # checa se a bola está dentro do heroi
            if hero.has_ball_inside(ball):
                score += 1
                score_text_surface = game_font.render('Pontos: ' + str(score), False,(255,255,255))
                hero.bite()
                ball.set_random_position(hero)
                #if time_left > 5:
                time_left += 2
                #else:
                #    time_left += (5 - time_left) + 1

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
