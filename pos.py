import pygame
class Pos():
    def __init__(self,rect,pos):
        self.rect=rect
        self.pos=pos
    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.rect)

    def get_rect(self):
        return(self.rect)