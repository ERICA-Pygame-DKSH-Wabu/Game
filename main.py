import pygame
from util import *

pygame.init()

screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("forest witch")

WHITE = (255, 255, 255)
spirit_pos_l = []
for i in range(6):
    for j in range(4):
        x = i * 70 + j * 30 + 70
        y = screen_height - (j + 1) * 60 - 70
        rect = pygame.Rect(x, y, 10, 10)
        spirit_pos_l.append(rect)



playing = True
while playing:
    mouse_pos_x,mouse_pos_y=pygame.mouse.get_pos()
    mouse_condition=pygame.mouse.get_pressed()
    screen.fill(WHITE)
    for i in  spirit_pos_l:
        pygame.draw.rect(screen,(0,0,0),i)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    pygame.display.flip()
pygame.quit()
