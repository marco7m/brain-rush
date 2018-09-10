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
        self.RANDOM_MOVING = False
        self.start_random_moving = 0


    def has_ball_inside(self, ball):
        if (ball.pos.x > self.pos.x and ball.pos.x < (self.pos.x + self.width)) and (ball.pos.y > self.pos.y and ball.pos.y < (self.pos.y + self.height)):
            return True

    def move_left(self, internal_order=False):
        if self.RANDOM_MOVEMENT: 
            self.RANDOM_MOVEMENT = False
            self.RANDOM_MOVING = True
            self.start_random_moving = pygame.time.get_ticks()
        elif not self.RANDOM_MOVING or internal_order:
            self.images = self.images_esq
            self.image = self.images[self.index]
            if self.pos.x > 0:
                self.pos.x -= self.speed
    def move_right(self, internal_order=False):
        if self.RANDOM_MOVEMENT: 
            self.RANDOM_MOVEMENT = False
            self.RANDOM_MOVING = True
            self.start_random_moving = pygame.time.get_ticks()
        elif not self.RANDOM_MOVING or internal_order:
            self.images = self.images_dir
            self.image = self.images[self.index]
            if self.pos.x < CONST.DISPLAY_SIZE_X - self.width:
                self.pos.x += self.speed
    def move_up(self, internal_order=False):
        if self.RANDOM_MOVEMENT: 
            self.RANDOM_MOVEMENT = False
            self.RANDOM_MOVING = True
            self.start_random_moving = pygame.time.get_ticks()
        elif not self.RANDOM_MOVING or internal_order:
            if self.pos.y > 60:
                self.pos.y -= self.speed
    def move_down(self, internal_order=False):
        if self.RANDOM_MOVEMENT: 
            self.RANDOM_MOVEMENT = False
            self.RANDOM_MOVING = True
            self.start_random_moving = pygame.time.get_ticks()
        elif not self.RANDOM_MOVING or internal_order:
            if self.pos.y < CONST.DISPLAY_SIZE_Y - self.height:
                self.pos.y += self.speed

    def update(self):
        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y

        # faz ele sair do modo slow_down depois de um tempo
        if self.SLOWED_DOWN:
            if pygame.time.get_ticks() - self.start_slow_down > 2000:
                self.speed = CONST.ZOMBIE_SPEED
                self.SLOWED_DOWN = False

        # faz ele sair do modo random_movement depois de um tempo
        if self.RANDOM_MOVEMENT:
            if pygame.time.get_ticks() - self.start_random_movement > 3000:
                self.RANDOM_MOVEMENT = False

        if self.RANDOM_MOVING:
            print "moveu"
            print self.RANDOM_MOVEMENT
            print self.RANDOM_MOVING
            if pygame.time.get_ticks() - self.start_random_moving > 500:
                self.RANDOM_MOVING = False
                print "parou moving"
            elif self.drawn_rand_direction == 0:
                print "0"
                self.move_up(internal_order=True)
            elif self.drawn_rand_direction == 1:
                print "1"
                self.move_down(internal_order=True)
            elif self.drawn_rand_direction == 2:
                print "2"
                self.move_left(internal_order=True)
            elif self.drawn_rand_direction == 3:
                print "3"
                self.move_right(internal_order=True)

        # faz os frames se alternarem
        self.delay_time_index += 1
        if self.delay_time_index >= self.DELAY_TIME:
            self.delay_time_index = 0

            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

    def slow_down(self):
        self.speed = CONST.ZOMBIE_SLOWER_SPEED
        self.SLOWED_DOWN = True
        self.start_slow_down = pygame.time.get_ticks()

    def random_movement(self):
        self.RANDOM_MOVEMENT = True
        self.drawn_rand_direction = random.randint(0,3)
        self.start_random_movement = pygame.time.get_ticks()

    def zombie_error(self):
        erro = pygame.mixer.Sound('src/sounds/erro.wav')
        erro.play()

    def human_error(self):
        erro = pygame.mixer.Sound('src/sounds/human_error.wav')
        erro.play()
        time.sleep(1)

    def bite(self):
        erro = pygame.mixer.Sound('src/sounds/bite1.wav')
        erro.play()

    def wrong_way(self, number):
        if number == 0:
            return self.move_up()
        elif number == 1:
            return self.move_down()
        elif number == 2:
            return self.move_right()
        else:
            return self.move_left()
