# -*- encoding:utf-8 -*-
import pygame
import time
import random
from src.position import Position
from src.ball import Ball
import src.const as CONST

class Zombie(pygame.sprite.Sprite):
    def __init__(self):

        super(Zombie, self).__init__()
        self.images_esq = []
        self.images_esq.append(pygame.image.load("img/zumbi_esquerdo_fechado.png"))
        self.images_esq.append(pygame.image.load("img/zumbi_esquerdo_aberto.png"))

        self.images_dir = []
        self.images_dir.append(pygame.image.load("img/zumbi_direito_fechado.png"))
        self.images_dir.append(pygame.image.load("img/zumbi_direito_aberto.png"))

        self.images = self.images_dir

        self.index = 0
        self.DELAY_TIME = 20
        self.delay_time_index = 0

        self.image = self.images[self.index]

        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]

        x = CONST.DISPLAY_SIZE_X/2 - self.width/2
        y = CONST.DISPLAY_SIZE_Y/2 - self.height/2
        self.pos = Position(x,y)

        # ver se é necessário depois essa linha
        self.rect = pygame.Rect(x,y,self.width,self.height)

        self.speed = CONST.ZOMBIE_SPEED

        # variaveis dos erros
        self.SLOWED_DOWN = False
        self.start_slow_down = 0
        
        self.RANDOM_MOVEMENT = False
        self.start_random_movement = 0

        self.drawn_rand_direction = 0

    def has_ball_inside(self, ball):
        if (ball.pos.x > self.pos.x and ball.pos.x < (self.pos.x + self.width)) and (ball.pos.y > self.pos.y and ball.pos.y < (self.pos.y + self.height)):
            return True

    def move_left(self, rand=False):
        if self.RANDOM_MOVEMENT and not rand:
#            while self.rand_direction == 3:
#                self.shuffle_random_direction()
            self.move_random()
        elif rand or not self.RANDOM_MOVEMENT:
     
            self.images = self.images_esq
            self.image = self.images[self.index]
            if self.pos.x > 0:
                self.pos.x -= self.speed
                
    def move_right(self, rand=False):
        if self.RANDOM_MOVEMENT and not rand:
#            while self.rand_direction == 3:
#                self.shuffle_random_direction()
            self.move_random()
        elif rand or not self.RANDOM_MOVEMENT:
            
            self.images = self.images_dir
            self.image = self.images[self.index]
            if self.pos.x < CONST.DISPLAY_SIZE_X - self.width:
                self.pos.x += self.speed

    def move_up(self, rand=False):
        if self.RANDOM_MOVEMENT and not rand:
#            while self.rand_direction == 3:
#                self.shuffle_random_direction()
            self.move_random()
        elif rand or not self.RANDOM_MOVEMENT:

            if self.pos.y > 60:
                self.pos.y -= self.speed

    def move_down(self, rand=False):
        if self.RANDOM_MOVEMENT and not rand:
#            while self.rand_direction == 3:
#                self.shuffle_random_direction()
            self.move_random()
        elif rand or not self.RANDOM_MOVEMENT:

            if self.pos.y < CONST.DISPLAY_SIZE_Y - self.height:
                self.pos.y += self.speed

    def move_random(self):
        if self.drawn_rand_direction == 0:
            self.move_left(rand=True)
        if self.drawn_rand_direction == 1:
            self.move_right(rand=True)
        if self.drawn_rand_direction == 2:
            self.move_up(rand=True)
        if self.drawn_rand_direction == 3:
            self.move_down(rand=True)

    def shuffle_random_direction(self):
        self.drawn_rand_direction = random.randint(0,3)

    def update(self):
        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y

        # faz ele sair do modo slow_down depois de um tempo
        if self.SLOWED_DOWN:
            if pygame.time.get_ticks() - self.start_slow_down > 2000:
                self.speed = CONST.ZOMBIE_SPEED
                self.SLOWED_DOWN = False
                print "fim SLOWED_DOWN"

        # faz ele sair do modo random_movement depois de um tempo
        if self.RANDOM_MOVEMENT:
            if pygame.time.get_ticks() - self.start_random_movement > 3000:
                self.RANDOM_MOVEMENT = False
                print "fim RANDOM"

        # faz os frames se alternarem
        self.delay_time_index += 1
        if self.delay_time_index >= self.DELAY_TIME:
            self.delay_time_index = 0

            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

    def slow_down(self):
        if not self.SLOWED_DOWN or not self.RANDOM_MOVEMENT:
            print "inicio SLOWED_DOWN"
            self.speed = CONST.ZOMBIE_SLOWER_SPEED
            self.SLOWED_DOWN = True
            self.start_slow_down = pygame.time.get_ticks()

    def random_movement(self):
        if not self.SLOWED_DOWN or not self.RANDOM_MOVEMENT:
            print "inicio RANDOM"
            self.RANDOM_MOVEMENT = True
            self.drawn_rand_direction = random.randint(0,3)
            self.start_random_movement = pygame.time.get_ticks()

    def human_error(self):
        if not self.SLOWED_DOWN or not self.RANDOM_MOVEMENT:
            print "inicio human_error"
            erro = pygame.mixer.Sound('sounds/human_error.wav')
            erro.play()
            time.sleep(1)
            print "fim human_error"

    def zombie_scream(self):
        erro = pygame.mixer.Sound('sounds/erro.wav')
        erro.play()

    def bite(self):
        erro = pygame.mixer.Sound('sounds/bite1.wav')
        erro.play()
