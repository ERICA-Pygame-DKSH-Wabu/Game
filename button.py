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
    def __init__(self, x, y, hitbox, s_type):
        super().__init__(x, y, hitbox)
        self.s_type = s_type
        self.im_size=144
        self.original_pos = (x, y)
        self.sprit = None
        self.dragging = False
        self.frame_index=0

        self.frame=get_frame(f"asset/ui/store_btn/{self.s_type}",self.im_size,self.im_size,255)
        self.im = self.frame[10]
        

        self.string_im=[]
        self.string_im.append(get_im("asset/ui/string.png"))
        self.string_im[0]=set_im(self.string_im[0],self.im_size,self.im_size,255,True)

        self.string_im.append(get_im("asset/ui/string2.png"))
        self.string_im[1]=set_im(self.string_im[1],self.im_size,self.im_size,255,True)


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
                for j in spirit_pos_l:
                    if self.hitbox.colliderect(j.rect):
                        self.set_hitbox()
                        return (j.rect, self.s_type,j.pos)
                self.set_hitbox()
                return False

    def draw(self, screen):
        screen.blit(self.im, (self.hitbox.centerx-self.im.get_width()//2,self.hitbox.centery-self.im.get_height()//2))
        screen.blit(self.string_im[ 1 if self.dragging else 0], (self.original_pos[0]-self.string_im[ 1 if self.dragging else 0].get_width()//2,self.original_pos[1]-self.string_im[ 1 if self.dragging else 0].get_height()//5*2))
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def change_frame(self,dt):
        self.im=self.frame[int(self.frame_index)]
        if len(self.frame) <= int(self.frame_index+0.01*dt) :
            self.frame_index=0
        else:
            self.frame_index+=0.01*dt

