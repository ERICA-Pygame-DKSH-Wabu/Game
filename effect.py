class effect:
    def __init__(self,x,y,frame):
        self.x=x
        self.y=y
        self.frame=frame
        self.im=frame[0]
        self.frame_index=0
    def draw(self,screen):
        screen.blit(self.im,(self.x-self.im.get_width()//2,self.y-self.im.get_height()//2))
    def change_frame(self,dt):
        self.im=self.frame[int(self.frame_index)]
        if len(self.frame) <= int(self.frame_index+0.01*dt) :
            return True
        else:
            self.frame_index+=0.01*dt
