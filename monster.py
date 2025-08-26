import pygame
from spirit import *
monster_frame_dict={}
l=["water","light","stone","fire","dark","grass"]
monster_size=[120,120,120,96,144,144]
for i in l:
    monster_frame_dict[i]={
            "attack": get_frame(f"asset/monster/{i}/attack",monster_size[l.index(i)],monster_size[l.index(i)],255),
            "idle": get_frame(f"asset/monster/{i}/idle",monster_size[l.index(i)],monster_size[l.index(i)],255),
            "spin": get_frame(f"asset/monster/{i}/spin",monster_size[l.index(i)],monster_size[l.index(i)],255),
        }
class Monster(Spirit):

    def __init__(self,pos, index, m_type):
        super().__init__(pos,index, m_type)
        self.name = m_type 
        self.im_size = 150 
        self.target = 180
        self.move_speed = 10
        self.is_moving = True 
        self.has_arrived = False  
        self.index = index 
        self.target_col = 0 
        self.condition = "spin"
    def set_frame(self):
        self.frame=monster_frame_dict[self.name]
    def set_condition(self):
        if int(self.hitbox.centerx)-self.distance  <= int(self.target)  and self.target:
            if self.reroad:
                self.condition="attack"
            else:
                self.condition="spin"
        else:
            self.condition="idle"
            self.reroad=True
    def set_target(self, target_l):
        candidates = [obj for obj in target_l if obj and obj.centerx <= self.hitbox.centerx]
        if candidates:
            self.target = max(candidates, key=lambda obj: obj.centerx).centerx
        else:
            self.target = 210+25*(4-self.line)

    def move(self,dt):
        if self.condition=="idle":
            self.hitbox.centerx-=self.speed*dt*0.04
                


class Water_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m) 
        self.im_size = 110 
        self.y_gap = 10
        self.distance=60
        self.move_speed=15 

class Light_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m) 
        self.im_size = 100 
        self.x_gap = -3
        self.y_gap = 10
        self.distance=200
        self.move_speed=12

class Stone_Monster(Monster): 
    def __init__(self, pos,index,m): 
        super().__init__(pos,index, m) 
        self.im_size = 120 
        self.y_gap = 8
        self.x_gap = -1
        self.distance=60
        self.move_speed=5


class Fire_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m) 
        self.y_gap = -5
        self.im_size = 80
        self.distance=700
        self.move_speed=7.5


class Dark_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index,m) 
        self.im_size = 100 
        self.x_gap = -3
        self.y_gap = 20
        self.distance=150
        self.move_speed=10


class Grass_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index,m) 
        self.im_size = 60
        self.x_gap = -3
        self.y_gap = 15
        self.distance=300
        self.move_speed=15
