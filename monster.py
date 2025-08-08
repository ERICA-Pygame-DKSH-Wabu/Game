import pygame
import math
from spirit import *

class Monster(Spirit):

    def __init__(self, pos, m_type):
        super().__init__(pos)
        self.name = m_type
        self.im_size = 150
        self.target_rect = [0,0]
        
        self.target_pos = pos  
        self.start_pos = pygame.Vector2(1400, pos.centery) 
        self.current_pos = pygame.Vector2(self.start_pos)  
        self.move_speed = 100  
        self.is_moving = True
        self.has_arrived = False
        
        self.hitbox.center = self.start_pos
        
    def set_frame(self):
        self.frame={
            "attack": get_frame(f"asset/monster/{self.name}/attack",self.im_size,self.im_size,255),
            "idle": get_frame(f"asset/monster/{self.name}/idle",self.im_size,self.im_size,255),
            "spin": get_frame(f"asset/monster/{self.name}/spin",self.im_size,self.im_size,255),
            "move": get_frame(f"asset/monster/{self.name}/idle",self.im_size,self.im_size,255)  
        }

    def set_target_rect(self, row, col):
        self.target_rect = [col, row]

    def update_movement(self, dt):
        if not self.is_moving or self.has_arrived:
            return
            
        target_vector = pygame.Vector2(self.target_pos.center) - self.current_pos
        distance = target_vector.length()

        if distance <= 5:
            self.current_pos = pygame.Vector2(self.target_pos.center)
            self.is_moving = False
            self.has_arrived = True
            self.condition = "idle"  
        else:
            move_distance = self.move_speed * dt * 0.001 
            if move_distance > distance:
                move_distance = distance
                
            direction = target_vector.normalize()
            self.current_pos += direction * move_distance
            self.condition = "move"  
            
        self.hitbox.center = self.current_pos

    def change_frame(self, dt):
        self.update_movement(dt)
        
        if self.condition in self.frame:
            self.img = self.frame[self.condition][int(self.frame_index)]
            if len(self.frame[self.condition]) <= int(self.frame_index + 0.01 * dt * self.frame_speed):
                self.frame_index = 0
            else:
                self.frame_index += 0.01 * dt * self.frame_speed

    def reset_position(self):

        self.current_pos = pygame.Vector2(self.start_pos)
        self.hitbox.center = self.start_pos
        self.is_moving = True
        self.has_arrived = False
        self.condition = "move"
        self.frame_index = 0

class Water_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "water")
        self.im_size = 96

class Light_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "light")
        self.im_size = 120

class Stone_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "stone")
        self.im_size = 120

class Fire_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "fire")
        self.im_size = 90
        self.y_gap = -12
        self.frame_speed = 1.0

class Dark_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "dark")
        self.im_size = 120

class Grass_Monster(Monster):
    def __init__(self, pos):
        super().__init__(pos, "grass")
        self.im_size = 110
        self.y_gap = -5