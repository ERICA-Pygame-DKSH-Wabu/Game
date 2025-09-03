import math
import util

frame = util.get_frame("asset/mana_frame", 20, 40, 220)
frame2=[]
for i in frame:
    frame2.append(util.invert_surface_color(i))


class Mana:
    def __init__(self, center):
        self.charge=False
        self.frame2=frame2
        self.frame = frame
        self.frame_index = 0
        self.center = center
        self.relative_angle = 0
        self.target_relative_angle = 0
        self.orbit_radius_x = 60
        self.orbit_radius_y = 25
        self.x = 0
        self.y = 0
        self.im = self.frame[0]

    def update(self, index, total, orbit_angle):
        if total == 0:
            return True
        self.target_relative_angle = index * (360 / total)
        diff = (self.target_relative_angle - self.relative_angle + 360) % 360
        if diff > 180:
            diff -= 360
        self.relative_angle = (self.relative_angle + diff * 0.05) % 360
        total_angle = (self.relative_angle + orbit_angle) % 360
        rad = math.radians(total_angle)
        self.x = self.center[0] + self.orbit_radius_x * math.cos(rad)
        self.y = self.center[1] + self.orbit_radius_y * math.sin(rad)
        if not self.charge:
            self.frame_index = (self.frame_index + 1) % len(self.frame)
            self.im = self.frame[self.frame_index]
        else:
            self.frame_index = (self.frame_index + 1) % len(self.frame2)
            self.im = self.frame2[self.frame_index]
    def draw(self, screen):
        screen.blit(self.im, (int(self.x), int(self.y)))
