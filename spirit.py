from util import *

class Spirit():
    def __init__(self,pos,line, name=""):
        self.reroad=True
        self.line=line
        self.distance=100
        self.target=False
        self.name=name
        self.frame={}
        self.condition="idle"
        self.img=None
        self.hitbox=pygame.rect.Rect(0,0,50,50)
        self.attack_speed=1
        self.max_health=0
        self.hitbox.center=pos.center
        self.health=0
        self.length=0
        self.speed=1
        self.cooltime=0
        self.ct=0
        self.frame_index=0
        self.im_size=0
        self.enemy_circle_surface = pygame.Surface((self.hitbox.width+10,25), pygame.SRCALPHA)
        pygame.draw.ellipse(self.enemy_circle_surface, (0,0,0,96), (0,0,self.hitbox.width+10,25))
    def set_target(self,target_l):
        if target_l:
            self.target=min(target_l, key=lambda obj: obj.hitbox.centerx).hitbox.left

    def draw(self,screen):
        
        #pygame.draw.rect(screen,(0,0,0),self.hitbox)
        screen.blit(self.enemy_circle_surface, (self.hitbox.centerx-(self.hitbox.width+10)//2,self.hitbox.bottom-5))

        screen.blit(self.img,(self.hitbox.centerx-self.img.get_width()//2,self.hitbox.centery-self.img.get_height()//2))

    def set_frame(self):
        self.frame={
            "attack": get_frame(f"asset/spirit/{self.name}/attack",self.im_size,self.im_size,255),
            "idle": get_frame(f"asset/spirit/{self.name}/idle",self.im_size,self.im_size,255),
            "spin": get_frame(f"asset/spirit/{self.name}/spin",self.im_size,self.im_size,255)
        }
    def set_condition(self):
        if abs(int(self.hitbox.left)-int(self.target)) <= self.distance and self.target:

            if self.reroad:
                self.condition="attack"
            else:
                self.condition="spin"
        else:
            self.condition="idle"
            self.reroad=False

    def change_frame(self,dt):
        frame= 0.01 * dt *self.attack_speed
        if self.condition in self.frame:
            self.img = self.frame[self.condition][int(self.frame_index)]
            if len(self.frame[self.condition]) <= int(self.frame_index + frame):
                self.frame_index = 0
                if self.condition=="spin":
                    self.reroad=True
                elif self.condition=="attack":
                    self.reroad=False
            else:
                self.frame_index += frame
    def change_condition(self):
        self.frame_index=0

class Water_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "water"
        self.hitbox.center=pos.center
        self.im_size=96

class Light_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "light"
        self.hitbox.center=pos.center
        self.im_size=120

class Stone_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "stone"
        self.hitbox.center=pos.center
        self.im_size=120

class Fire_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "fire"
        self.hitbox.center=pos.center
        self.im_size=130
        self.attack_speed=1.5
    def set_frame(self):
        self.frame={
            "attack": get_frame(f"asset/spirit/{self.name}/attack",self.im_size*1.2,self.im_size*1.2,255),
            "idle": get_frame(f"asset/spirit/{self.name}/idle",self.im_size*1.05,self.im_size*1.05,255),
            "spin": get_frame(f"asset/spirit/{self.name}/spin",self.im_size*1.2,self.im_size*1.2,255)
        }

class Dark_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "dark"
        self.hitbox.center=pos.center
        self.im_size=120

class Grass_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "grass"
        self.hitbox.center=pos.center
        self.im_size=120
