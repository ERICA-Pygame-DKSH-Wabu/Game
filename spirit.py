from util import *
class Spirit():
    def __init__(self,x,y,pos):
        self.x=x
        self.y=y
        self.dx=0
        self.dY=0
        self.name=""
        self.frame={}
        self.condition=""
        self.im=None

        self.max_health=0
        self.health=0
        self.length=0

        self.speed=1
        self.cooltime=0
        self.ct=0
        self.position=pos
        self.frame_index=0
    def set_frame(self):
        self.frame={
            "attack": get_frame(f"asset/spirit/{self.name}/attack",96,96,64,True),
            "idle": get_frame(f"asset/spirit/{self.name}/idle",96,96,64,True),
            "spin": get_frame(f"asset/spirit/{self.name}/spin",96,96,64,True)
        }
    def change_frame(self):
        self.im=self.frame[self.condition][self.frame_index]
        if len(self.frame[self.condition])-1==self.frame_index:
            self.frame_index=0
        else:
            self.frame_index+=0.05
    def if_change_condition(self):
        self.frame_index=0
    def move(self,dt):
        self.x+=self.dx*self.speed*dt
        self.y+=self.dy*self.speed*dt

class Water_Spirit(Spirit):
    def __init__(self,x,y,pos):
        super.__init__(self,x,y,pos)
        self.name="water"

class Light_Spirit(Spirit):
    def __init__(self,x,y,pos):
        super.__init__(self,x,y,pos)
        self.name="light"

class Stone_Spirit(Spirit):
    def __init__(self,x,y,pos):
        super.__init__(self,x,y,pos)
        self.name="stone"

class Fire_Spirit(Spirit):
    def __init__(self,x,y,pos):
        super.__init__(self,x,y,pos)
        self.name="fire"

class Dark_Spirit(Spirit):
    def __init__(self,x,y,pos):
        super.__init__(self,x,y,pos)
        self.name="dark"

class Grass_Spirit(Spirit):
    def __init__(self,x,y,pos):
        super.__init__(self,x,y,pos)
        self.name="grass"
