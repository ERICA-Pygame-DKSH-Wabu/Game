from util import *
spirit_frame_dict={}
l=["water","light","stone","fire","dark","grass"]
spirit_size=[96,120,120,150,120,120]
for i in l:
    spirit_frame_dict[i]={
            "attack": get_frame(f"asset/spirit/{i}/attack",spirit_size[l.index(i)],spirit_size[l.index(i)],255),
            "idle": get_frame(f"asset/spirit/{i}/idle",spirit_size[l.index(i)],spirit_size[l.index(i)],255),
            "spin": get_frame(f"asset/spirit/{i}/spin",spirit_size[l.index(i)],spirit_size[l.index(i)],255),
        }
for i in spirit_frame_dict["fire"]["idle"]:
    spirit_frame_dict["fire"]["idle"][ spirit_frame_dict["fire"]["idle"].index(i)]=set_im(i,138,138,255,False)
class Spirit():
    def __init__(self,pos,line, name=""):
        self.damaged=False
        self.damaged_cooltime=0
        self.if_attack=True
        self.attack_time=0
        self.damage=0
        self.max_health=100
        self.health=100
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
    def check_damaged_cool(self,dt):
        self.damaged_cooltime+=dt*0.1
        if self.damaged_cooltime>=100:
            self.damaged=True
        else:
            self.damaged=False
    def set_target(self,target_l):
        if target_l:
            self.target=min(target_l, key=lambda obj: obj.hitbox.centerx).hitbox.centerx

    def draw(self,screen):
        
        #pygame.draw.rect(screen,(0,0,0),self.hitbox)
        screen.blit(self.enemy_circle_surface, (self.hitbox.centerx-(self.hitbox.width+10)//2,self.hitbox.bottom-5))

        screen.blit(self.img,(self.hitbox.centerx-self.img.get_width()//2,self.hitbox.centery-self.img.get_height()//2))

    def set_frame(self):
        self.frame=spirit_frame_dict[self.name]
    def set_condition(self):
        if int(self.hitbox.centerx)+self.distance  >= int(self.target)  and self.target:
            if self.reroad:
                self.condition="attack"
            else:
                self.condition="spin"
        else:
            self.condition="idle"
            self.reroad=True

    def change_frame(self,dt):
        try:
            frame= 0.01 * dt *self.attack_speed
            if self.condition in self.frame:
                self.img = self.frame[self.condition][int(self.frame_index)]
                if len(self.frame[self.condition]) <= int(self.frame_index + frame):
                    self.frame_index = 0
                    if self.condition=="spin":
                        self.reroad=True
                        self.if_attack=True
                    elif self.condition=="attack":
                        self.reroad=False
                        return True
                else:
                    self.frame_index += frame
                return False
        except IndexError:
            self.frame_index=0

    def change_condition(self):
        self.frame_index=0
class Water_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "water"
        self.hitbox.center=pos.center
        self.im_size=96
        self.attack_time=9

class Light_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "light"
        self.hitbox.center=pos.center
        self.im_size=120
        self.attack_time=5

class Stone_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "stone"
        self.hitbox.center=pos.center
        self.im_size=120
        self.attack_time=7

class Fire_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "fire"
        self.hitbox.center=pos.center
        self.im_size=130
        self.attack_time=6

class Dark_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "dark"
        self.hitbox.center=pos.center
        self.im_size=120
        self.attack_time=5
class Grass_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "grass"
        self.hitbox.center=pos.center
        self.im_size=120
        self.attack_time=6
