from util import *
class Button:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.im=None
        self.coli=None
        self.hitbox=pygame.rect.Rect()
class Store_Button(Button):
    def __init__(self,x,y):
        super.__init__(self,x,y)
    def set_hitbox(self):
        self.hitbox.center=(self.x,self.y)
    def drag(self,m_pos,m_condition,spirit_pos_l):
        if self.hitbox.collidepoint(m_pos[0],m_pos[1]) and m_condition[0]:
            self.x,self.y=m_pos[0],m_pos[1]
        if not m_condition[0]:
            self.drop(spirit_pos_l)
    def drop(self,spirit_pos_l):
        for i in spirit_pos_l:
            if i.colliderect(self.hitbox):
                self.hitbox.ceter=i.center

