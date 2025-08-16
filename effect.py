import pygame
from util import *
class effect:
    def __init__(self,x,y,frame):
        self.x=x
        self.y=y
        self.frame=frame
        self.im=frame[0]
        self.frame_index=0
        self.frame_speed=1
    def draw(self,screen):
        screen.blit(self.im,(self.x-self.im.get_width()//2,self.y-self.im.get_height()//2))
    def change_frame(self,dt):
        self.im=self.frame[int(self.frame_index)]
        if len(self.frame) <= int(self.frame_index+0.01*dt*self.frame_speed) :
            return True
        else:
            self.frame_index+=0.01*dt*self.frame_speed
class attack_effect(effect):
    def __init__(self,x,y,frame,rect_size,damage):
        super().__init__(x,y,frame)
        self.hitbox=pygame.rect.Rect(0,0,rect_size,rect_size)
        self.hitbox.center=(x,y)
        self.damage=damage
        self.frame_speed=2