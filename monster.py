import pygame
from spirit import *

class Monster(Spirit):

    def __init__(self, self_pos, index,m_type):
        super().__init__(self_pos,index, m_type)
        self.im_size = 150
        self.target_pos = 0
        self.move_speed = 100 
        self.is_moving = True
        self.reroad=False
    def set_frame(self):
        self.frame={
            "attack": get_frame(f"asset/monster/{self.name}/attack",self.im_size,self.im_size,255),
            "idle": get_frame(f"asset/monster/{self.name}/idle",self.im_size,self.im_size,255),
            "spin": get_frame(f"asset/monster/{self.name}/spin",self.im_size,self.im_size,255),
        }
    def set_target(self,target_l):
        for i in target_l.reverse():
            if i:
                self.target_pos=i

    def reset_position(self):
        self.is_moving = True
        self.has_arrived = False
        self.condition = "move"
        self.frame_index = 0

class Water_Monster(Monster):
    def __init__(self, pos,line):
        super().__init__(pos,line, "water")
        self.im_size = 96

class Light_Monster(Monster):
    def __init__(self, pos,line):
        super().__init__(pos,line, "light")
        self.im_size = 120

class Stone_Monster(Monster):
    def __init__(self, pos,line):
        super().__init__(pos,line, "stone")
        self.im_size = 120

class Fire_Monster(Monster):
    def __init__(self, pos,line):
        super().__init__(pos,line, "fire")
        self.im_size = 130
        self.frame_speed = 1.5

class Dark_Monster(Monster):
    def __init__(self, pos,line):
        super().__init__(pos,line, "dark")
        self.im_size = 120

class Grass_Monster(Monster):
    def __init__(self, pos,line):
        super().__init__(pos,line, "grass")
        self.im_size = 144