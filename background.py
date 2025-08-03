import pygame

class Background:
    def __init__(self):
        self.lines = []
        self.init_lines()

    def init_lines(self):
        for x in range(0, 801, 100):
            self.lines.append(((x, 0), (x, 600), (200, 200, 200), 1))

        for y in range(0, 601, 100):
            self.lines.append(((0, y), (800, y), (200, 200, 200), 1))

    def draw(self, screen):
        for start, end, color, width in self.lines:
            pygame.draw.line(screen, color, start, end, width)
