from util import *

class Spirit():
    def __init__(self,pos):
        self.name=""
        self.frame={}
        self.condition="idle"
        self.img=None
        self.hitbox=pygame.rect.Rect(0,0,50,50)
        self.hitbox.center=pos.center

        self.max_health=0
        self.health=0
        self.length=0

        self.speed=1
        self.cooltime=0
        self.ct=0
        self.frame_index=0
        self.im_size=0

    def draw(self,screen):
        screen.blit(self.img,(self.hitbox.centerx-self.img.get_width()//2,self.hitbox.centery-self.img.get_height()//2))

    def set_frame(self):
        self.frame={
            "attack": get_frame(f"asset/spirit/{self.name}/attack",self.im_size,self.im_size,200,True),
            "idle": get_frame(f"asset/spirit/{self.name}/idle",self.im_size,self.im_size,200,True),
            "spin": get_frame(f"asset/spirit/{self.name}/spin",self.im_size,self.im_size,200,True)
        }

    def change_frame(self,dt):
        self.img=self.frame[self.condition][int(self.frame_index)]
        if len(self.frame[self.condition]) <= int(self.frame_index+0.01*dt) :
            self.frame_index=0
        else:
            self.frame_index+=0.01*dt
    def if_change_condition(self):
        self.frame_index=0

class Water_Spirit(Spirit):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "water"
        self.im_size=96

class Light_Spirit(Spirit):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "light"
        self.im_size=120

class Stone_Spirit(Spirit):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "stone"
        self.im_size=120

class Fire_Spirit(Spirit):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "fire"
        self.im_size=130

class Dark_Spirit(Spirit):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "dark"
        self.im_size=120

class Grass_Spirit(Spirit):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "grass"
        self.im_size=144
