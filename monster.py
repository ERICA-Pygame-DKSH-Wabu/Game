import pygame
from spirit import *

class Monster(Spirit):

    def __init__(self,pos, index, m_type):
        super().__init__(pos,index, m_type)
        self.name = m_type 
        self.im_size = 150 
        self.target = 0
        self.move_speed = 100 
        self.is_moving = True 
        self.has_arrived = False  
        self.index = index 
        self.target_col = 0 
        self.condition = "spin"

    def set_frame(self):
        self.frame={
            "attack": get_frame(f"asset/monster/{self.name}/attack",self.im_size,self.im_size,255),
            "idle": get_frame(f"asset/monster/{self.name}/idle",self.im_size,self.im_size,255),
            "spin": get_frame(f"asset/monster/{self.name}/spin",self.im_size,self.im_size,255),
        }

    def set_target(self,target_l):
        for i in target_l:
            if i:
                self.target=i.centerx

    def move(self,dt):
        if self.condition=="idle":
            print("s")
            self.hitbox.centerx-=self.speed*dt*0.04
                


class Water_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m) 
        self.im_size = 96 


class Light_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m) 
        self.im_size = 120 

class Stone_Monster(Monster): 
    def __init__(self, pos,index,m): 
        super().__init__(pos,index, m) 
        self.im_size = 120 


class Fire_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m) 
        self.im_size = 130 


class Dark_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index,m) 
        self.im_size = 120 


class Grass_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index,m) 
        self.im_size = 144 