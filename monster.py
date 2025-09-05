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
        self.x=pos.centerx
        self.name = m_type 
        self.im_size = 150 
        self.target = 180
        self.max_health=100
        self.health=self.max_health
        self.move_speed = 10
        self.is_moving = True 
        self.has_arrived = False  
        self.index = index 
        self.target_col = 0 
        self.condition = "spin"
    def set_hitbox(self):
        self.hitbox.centerx=self.x
    def draw(self,screen):
        screen.blit(self.enemy_circle_surface, (self.x-(self.hitbox.width+10)//2,self.hitbox.bottom-30))

        screen.blit(self.img,(self.hitbox.centerx-self.img.get_width()//2-self.x_gap,self.hitbox.centery-self.img.get_height()//2-20-self.y_gap))
        if self.max_health > 0:
            bar_width = 45
            bar_height = 4
            full_rect = pygame.Rect(0, 0, bar_width, bar_height)
            full_rect.midbottom = (self.hitbox.centerx, self.hitbox.bottom)
            ratio = max(0, min(self.health / self.max_health, 1.0))
            curr_rect = full_rect.copy()
            curr_rect.width = int(bar_width * ratio)
            pygame.draw.rect(screen, (255, 0, 0), full_rect)
            if curr_rect.width > 0:
                pygame.draw.rect(screen, (0, 255, 0), curr_rect)
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
            self.x-=self.speed*dt*0.006
                


class Water_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m)
        self.max_health=125
        self.health=self.max_health
        self.im_size = 110 
        self.y_gap = 10
        self.distance=60
        self.speed=5
        self.attack_time=3
        self.damage=65
class Light_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m)
        self.max_health=100
        self.health=self.max_health
        self.im_size = 100 
        self.x_gap = -3
        self.y_gap = 10
        self.distance=95
        self.speed=3
        self.attack_time=4
        self.damage=60
class Stone_Monster(Monster): 
    def __init__(self, pos,index,m): 
        super().__init__(pos,index, m)
        self.max_health=200
        self.health=self.max_health
        self.im_size = 120 
        self.y_gap = 8
        self.x_gap = -1
        self.distance=60
        self.speed=2
        self.attack_time=3
        self.damage=40

class Fire_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index, m)
        self.max_health=65
        self.health=self.max_health
        self.y_gap = -5
        self.im_size = 80
        self.distance=500
        self.speed=1.8
        self.damage=60

class Dark_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index,m)
        self.max_health=110
        self.health=self.max_health
        self.im_size = 100 
        self.x_gap = -3
        self.y_gap = 20
        self.distance=85
        self.speed=3
        self.damage=70

class Grass_Monster(Monster): 
    def __init__(self,pos, index,m): 
        super().__init__(pos,index,m)
        self.max_health=110
        self.health=self.max_health
        self.im_size = 60
        self.x_gap = -3
        self.y_gap = 15
        self.distance=300
        self.speed=3.5
        self.attack_time=5
        self.damage=60