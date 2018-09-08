# -*- encoding:utf-8 -*-
import pygame
import time
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

        self.speed = 6

    def has_ball_inside(self, ball):
        if (ball.pos.x > self.pos.x and ball.pos.x < (self.pos.x + self.width)) and (ball.pos.y > self.pos.y and ball.pos.y < (self.pos.y + self.height)):
            return True

    def move_left(self):
        self.images = self.images_esq
        self.image = self.images[self.index]
        if self.pos.x > 0:
            self.pos.x -= self.speed
    def move_right(self):
        self.images = self.images_dir
        self.image = self.images[self.index]
        if self.pos.x < CONST.DISPLAY_SIZE_X - self.width:
            self.pos.x += self.speed
    def move_up(self):
        if self.pos.y > 60:
            self.pos.y -= self.speed
    def move_down(self):
        if self.pos.y < CONST.DISPLAY_SIZE_Y - self.height:
            self.pos.y += self.speed

    def update(self):
        self.rect[0] = self.pos.x
        self.rect[1] = self.pos.y

        self.delay_time_index += 1
        if self.delay_time_index >= self.DELAY_TIME:
            self.delay_time_index = 0

            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

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
