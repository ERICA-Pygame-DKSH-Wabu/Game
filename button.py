from util import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

class Button:
    def __init__(self,x,y,hitbox):
        self.x=x
        self.y=y
        self.im=None
        self.coli=None
        self.hitbox=hitbox

    def draw(self,screen):
        pygame.draw.rect(screen,BLACK,self.hitbox)

class Store_Button(Button):
    def __init__(self, x, y, hitbox, s_type):
        super().__init__(x, y, hitbox)
        self.s_type = s_type
        self.original_pos = (x, y)
        self.sprit = None
        self.dragging = False
        self.img = get_im(f"asset/ui/store_btn/{self.s_type}.png")
        self.img = pygame.transform.smoothscale(self.img, (80, 80))
        self.offset_x = -15  
        self.offset_y = -15

    def set_hitbox(self):
        self.hitbox.center = (self.x, self.y)

    def drag(self, m_pos, m_condition, spirit_pos_l):
        if not self.dragging and self.hitbox.collidepoint(m_pos[0], m_pos[1]) and m_condition[0]:
            self.dragging = True

        if self.dragging:
            if m_condition[0]:
                self.x, self.y = m_pos[0], m_pos[1]
                self.hitbox.center = (self.x, self.y)
            else:
                self.dragging = False
                self.x, self.y = self.original_pos
                for rect in spirit_pos_l:
                    if self.hitbox.colliderect(rect):
                        self.set_hitbox()
                        return (rect, self.s_type)
                self.set_hitbox()
                return False

    def draw(self, screen):
        screen.blit(self.img, (self.hitbox.left + self.offset_x, self.hitbox.top + self.offset_y))
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

