import pygame
from spirit import *

class Monster(Spirit):

    def __init__(self, pos, m_type):
        super().__init__(pos)
        self.name = m_type
        self.im_size = 150
        
    def set_frame(self):
        self.frame={
            "attack": get_frame(f"asset/monster/{self.name}/attack",self.im_size,self.im_size,255),
            "idle": get_frame(f"asset/monster/{self.name}/idle",self.im_size,self.im_size,255),
            "spin": get_frame(f"asset/monster/{self.name}/spin",self.im_size,self.im_size,255)
        }

class Water_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "water")
        self.im_size=96

class Light_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "light")
        self.im_size=120

class Stone_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "stone")
        self.im_size=120

class Fire_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "fire")
        self.im_size=130
        self.frame_speed=1.5

class Dark_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "dark")
        self.im_size=120

class Grass_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "grass")
        self.im_size=144