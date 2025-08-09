import pygame
from spirit import *

class Monster(Spirit):

    def __init__(self, index, m_type, t):
        super().__init__(index, m_type)
        self.name = m_type 
        self.im_size = 150 
        self.target = t  
        self.move_speed = 100 
        self.is_moving = True 
        self.has_arrived = False  
        self.reroad = False 
        self.index = index 
        self.target_col = 0 
        screen_width = 1280 
        self.hitbox.centery = self.target.centery
        self.hitbox.centerx = screen_width + (self.im_size / 2)
        self.condition = "spin"

    def move(self, dt):
        """몬스터를 왼쪽으로 이동시켜 목표 지점으로 향하게 합니다."""
        if self.is_moving:
            if self.hitbox.centerx > self.target.centerx:
                self.condition = "spin"
                self.hitbox.x -= self.move_speed * (dt / 1000.0)
            else:
                self.hitbox.centerx = self.target.centerx
                self.is_moving = False
                self.has_arrived = True
                self.condition = "idle" 
                self.frame_index = 0 

    def set_frame(self): 
        self.frame={ 
            "attack": get_frame(f"asset/monster/{self.name}/attack",self.im_size,self.im_size,255), #
            "idle": get_frame(f"asset/monster/{self.name}/idle",self.im_size,self.im_size,255), #
            "spin": get_frame(f"asset/monster/{self.name}/spin",self.im_size,self.im_size,255), #
        } 

    def get_target(self,target_l): 
        try: 
            self.target_col = -1 
            a = 5 
            for i in reversed(target_l):  
                if i: 
                    self.target_col = a 
                    break 
                a -= 1 
        except: 
            self.target_col = -1 
        return (self.index, self.target_col) 

    def reset_position(self): 
        self.is_moving = True 
        self.has_arrived = False 
        self.condition = "move" 
        self.frame_index = 0 

class Water_Monster(Monster): 
    def __init__(self, index,t): 
        super().__init__(index, "water",t) 
        self.im_size = 96 

class Light_Monster(Monster): 
    def __init__(self, index,t): 
        super().__init__(index, "light",t) 
        self.im_size = 120 

class Stone_Monster(Monster): 
    def __init__(self, index,t): 
        super().__init__(index, "stone",t) 
        self.im_size = 120 

class Fire_Monster(Monster): 
    def __init__(self, index,t): 
        super().__init__(index, "fire",t) 
        self.im_size = 130 
        self.frame_speed = 1.5 

class Dark_Monster(Monster): 
    def __init__(self, index,t): 
        super().__init__(index, "dark",t) 
        self.im_size = 120 

class Grass_Monster(Monster): 
    def __init__(self, index,t): 
        super().__init__(index, "grass",t) 
        self.im_size = 144 