import pygame
from util import *
from button import *
from spirit import *

pygame.init()
spirit_type=["water","fire","grass","stone","light","dark"]
screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

spirit_dict={
    "water": Water_Spirit,
    "fire":Fire_Spirit,
    "grass":Grass_Spirit,
    "stone":Stone_Spirit,
    "light": Light_Spirit,
    "dark":Dark_Spirit
}

pygame.display.set_caption("forest witch")

spirit_l=[]


WHITE = (255, 255, 255)
spirit_pos_l = []
for i in range(6):
    for j in range(4):
        x = i * 70 + j * 30 + 70
        y = screen_height - (j + 1) * 60 - 70
        rect = pygame.Rect(x, y, 10, 10)
        spirit_pos_l.append(rect)
store_button_l=[]
for i in  range(6):
    store_button_l.append(Store_Button(screen_width-100*i-100,50,pygame.rect.Rect(screen_width-100*i-100,50,50,50),spirit_type[i]))
fps = pygame.time.Clock()

playing = True
while playing:
    dt = fps.tick(60)
    mouse_pos_x,mouse_pos_y=pygame.mouse.get_pos()
    mouse_condition=pygame.mouse.get_pressed()
    screen.fill(WHITE)
    for i in  spirit_pos_l:
        pygame.draw.rect(screen,(0,0,0),i)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    for i in store_button_l:
        i.set_hitbox()
        data= i.drag((mouse_pos_x,mouse_pos_y), mouse_condition, spirit_pos_l)
        if data:
            spirit_l.append(spirit_dict[data[1]](data[0]))
            spirit_l[-1].set_frame()
        i.draw(screen)

    for i in spirit_l:
        i.change_frame(dt)
        i.draw(screen)


    pygame.display.flip()
pygame.quit()
