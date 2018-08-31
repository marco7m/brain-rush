# -*- encoding:utf-8 -*-
import random
from src.position import Position
import src.const as CONST

class Ball:
    def __init__(self,x=0,y=0):
        self.pos = Position(x,y)
    
    def set_random_position(self,hero):
        while True:
            pos_x = random.randint(0,CONST.DISPLAY_SIZE_X)
            pos_y = random.randint(0,CONST.DISPLAY_SIZE_Y)
            if (pos_x < hero.pos.x or pos_x > (hero.pos.x + hero.width)) and (pos_y < hero.pos.y or pos_y > (hero.pos.y + hero.height)):
                # faz ele ficar dentro da borda pré estabelecida
                if (pos_x > CONST.BRAIN_RESPAWN_BORDER and
                    pos_x < CONST.DISPLAY_SIZE_X - CONST.BRAIN_RESPAWN_BORDER and
                    pos_y > CONST.BRAIN_RESPAWN_BORDER and
                    pos_y < CONST.DISPLAY_SIZE_Y - CONST.BRAIN_RESPAWN_BORDER):

                    self.pos.x = pos_x
                    self.pos.y = pos_y
                    return


