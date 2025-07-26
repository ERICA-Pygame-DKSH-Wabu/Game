import pygame
from util import *

pygame.init()

screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("forest witch")

WHITE = (255, 255, 255)

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    screen.fill(WHITE)
    pygame.display.flip()
pygame.quit()
