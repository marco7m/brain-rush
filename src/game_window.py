# -*- encoding:utf-8 -*-
import os
import pygame
from src.position import Position
from src.hero import Zombie
from src.ball import Ball
import src.const as CONST


_image_library = {}
class GameWindow:
    def __init__(self):
        
        pygame.font.init()
        game_font = pygame.font.SysFont('Comic Sans MS', 45)
        placar_font = pygame.font.SysFont('Comic Sans MS', 20)

        score = 0
        score_text_surface = game_font.render('Pontos: '+str(score), False,(0,0,0))

        placar = 100
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
        #ball_position = get_ball_positon()
        ball = Ball()
        ball.set_random_position(hero)

        # cria o timer
        time_left = CONST.GAME_TIME
        time_text_surface = game_font.render(str(time_left), False,(0,0,0))
        DEC_TIME = 1
        pygame.time.set_timer(DEC_TIME, 1000)

        screen = pygame.display.set_mode((CONST.DISPLAY_SIZE_X, CONST.DISPLAY_SIZE_Y))
        done = False
        clock = pygame.time.Clock()

        # loop principal
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == DEC_TIME:
                    if time_left > 0:
                        time_left -= 1
                    else:
                        done = True
            
            # pega as teclas pressionadas
            pressed = pygame.key.get_pressed()

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
                score += 1
                score_text_surface = game_font.render('Pontos: ' + str(score), False,(0,0,0))
                ball.set_random_position(hero)

            # atualiza o tempo
            if time_left < 6:
                time_text_surface = game_font.render(str(time_left), False,(255,0,0))
            else:
                time_text_surface = game_font.render(str(time_left), False,(0,0,0))

            screen.fill((0, 0, 0))
            hero_group.update()
            hero_group.draw(screen)
            screen.blit(get_image('img/cerebro.png'), (ball.pos.x, ball.pos.y))
            screen.blit(score_text_surface,(CONST.DISPLAY_SIZE_X - 250,10))
            screen.blit(time_text_surface,(CONST.DISPLAY_SIZE_X/2 - 0,10))
            screen.blit(placar_text_surface,(CONST.DISPLAY_SIZE_X/2 - 450,30))
            pygame.display.flip()
            clock.tick(60)

