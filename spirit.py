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
        self.fade=255
        self.dead=False
        self.if_attack=True
        self.attack_time=0
        self.damage=20
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
        self.max_health=100
        self.hitbox.center=pos.center
        self.health=100
        self.length=0
        self.speed=1
        self.cooltime=0
        self.ct=0
        self.frame_index=0
        self.im_size=0
        self.x_gap=0 #어둠, 빛 몬스터 전용
        self.y_gap=0 #어둠, 빛 정령 기준
        self.enemy_circle_surface = pygame.Surface((self.hitbox.width+10,25), pygame.SRCALPHA)
        pygame.draw.ellipse(self.enemy_circle_surface, (0,0,0,96), (0,0,self.hitbox.width+10,25))
    def if_dead(self,dt):
        if self.health<=0:
            self.dead=True
        if self.dead:
            self.fade-=dt*0.6
        if int(self.fade)<=1:
            return True
        return False

    def set_target(self, target_l):
        if target_l:
            candidates = [obj for obj in target_l if obj.hitbox.centerx >= self.hitbox.centerx and obj.health>0]
            if candidates:
                self.target = min(candidates, key=lambda obj: obj.hitbox.centerx).hitbox.centerx
            else:
                self.target = False
    def draw(self,screen):
        
        #pygame.draw.rect(screen,(0,0,0),self.hitbox)
        screen.blit(self.enemy_circle_surface, (self.hitbox.centerx-(self.hitbox.width+10)//2,self.hitbox.bottom-30))

        screen.blit(self.img,(self.hitbox.centerx-self.img.get_width()//2-self.x_gap,self.hitbox.centery-self.img.get_height()//2-20-self.y_gap))
        if self.max_health > 0:
            bar_width = 50
            bar_height = 5
            full_rect = pygame.Rect(0, 0, bar_width, bar_height)
            full_rect.midbottom = (self.hitbox.centerx, self.hitbox.bottom + 10)  # 살짝 아래 붙임
            ratio = max(0, min(self.health / self.max_health, 1.0))
            curr_rect = full_rect.copy()
            curr_rect.width = int(bar_width * ratio)
            pygame.draw.rect(screen, (255, 0, 0), full_rect)
            if curr_rect.width > 0:
                pygame.draw.rect(screen, (0, 255, 0), curr_rect)
    def set_frame(self):
        self.frame=spirit_frame_dict[self.name]
    def set_condition(self):
        if self.health<=0:
            self.condition="idle"
            return
        if int(self.hitbox.centerx)+self.distance  >= int(self.target)  and self.target and self.hitbox.centerx<self.target:
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
                self.img.set_alpha(int(self.fade))
                self.enemy_circle_surface.set_alpha(int(self.fade))
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
    def set_condition(self):
        if self.reroad:
            self.condition="attack"
        else:
            self.condition="spin"
class Light_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "light"
        self.hitbox.center=pos.center
        self.im_size=120
        self.y_gap = 5
        self.attack_time=5

class Stone_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "stone"
        self.hitbox.center=pos.center
        self.im_size=120
        self.y_gap = 15
        self.attack_time=7

class Fire_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "fire"
        self.hitbox.center=pos.center
        self.im_size=130
        self.y_gap = 10
        self.attack_time=6

class Dark_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "dark"
        self.hitbox.center=pos.center
        self.im_size=120
        self.y_gap = 5
        self.attack_time=5

class Grass_Spirit(Spirit):
    def __init__(self, pos,line):
        super().__init__(pos,line)
        self.name = "grass"
        self.hitbox.center=pos.center
        self.y_gap = 7
        self.im_size=120
        self.attack_time=6
    def set_condition(self):
        if self.reroad:
            self.condition="attack"
        else:
            self.condition="spin"
