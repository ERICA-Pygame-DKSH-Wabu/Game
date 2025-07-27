from util import *
class Button:
    def __init__(self,x,y,hitbox):
        self.x=x
        self.y=y
        self.im=None
        self.coli=None
        self.hitbox=hitbox
    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.hitbox)
class Store_Button(Button):
    def __init__(self, x, y,hitbox,s_type):
        super().__init__(x, y,hitbox)
        self.s_type=s_type
        self.original_pos = (x, y)
        self.sprit=None
        self.dragging=False

    def set_hitbox(self):
        self.hitbox.center = (self.x, self.y)

    def drag(self, m_pos, m_condition, spirit_pos_l):
        if not self.dragging and self.hitbox.collidepoint(m_pos[0], m_pos[1]) and m_condition[0]:
            self.dragging = True

        if self.dragging:
            if m_condition[0]:
                self.x, self.y = m_pos[0], m_pos[1]
                self.set_hitbox()
            else:
                self.dragging = False
                self.x, self.y = self.original_pos
                for rect in spirit_pos_l:
                    if self.hitbox.colliderect(rect):
                        self.set_hitbox()
                        return (rect, self.s_type)
                self.set_hitbox()
                return False

