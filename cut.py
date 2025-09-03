class Cut:
    def __init__(self,x,y,alpha,im):
        self.x=x
        self.y=y
        self.alpha=alpha
        self.im=im
        self.i=-1
    def draw(self,screen):
        self.im.set_alpha(self.alpha)
        screen.blit(self.im,(self.x,self.y))
    def fade_in(self,dt):
        self.alpha+=dt*0.3
        if self.alpha>=255:
            self.alpha=255
            return True
        return False
    def fade_out(self,dt):
        self.alpha-=dt*0.08
        if self.alpha<=1:
            self.alpha=1
            return True
        return False
    def fade_inout(self,dt):
        self.alpha+=dt*0.4*self.i
        if self.alpha>=255:
            self.alpha=255
            self.i=-1
            return True
        if self.alpha<=0:
            self.alpha=0
        return False