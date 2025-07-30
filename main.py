import pygame
from util import *
from button import *
from spirit import *

pygame.init()
spirit_type=["water","fire","grass","light","stone","dark"]
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

spirit_list=[]


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

spirit_pos_list = []

for i in range(6):
    for j in range(4):
        x = i * 80 + j * 30 + 120
        y = screen_height - (j + 1) * 80 - 20
        rect = pygame.Rect(x, y, 30, 30)
        spirit_pos_list.append(rect)
        
store_btn_list=[]

for i in  range(6):
    store_btn_list.append(Store_Button(screen_width-100*i-100,50,pygame.rect.Rect(screen_width-100*i-100,50,50,50),spirit_type[i]))

fps = pygame.time.Clock()
playing = True

while playing:
    dt = fps.tick(60)
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_condition = pygame.mouse.get_pressed()
    screen.fill(WHITE)

    for i in spirit_pos_list:
        pygame.draw.rect(screen, (0, 0, 0), i)

    # 드래그 중인 버튼 찾기
    dragging_btn = None
    for btn in store_btn_list:
        if btn.dragging:
            dragging_btn = btn
            break

    for i in store_btn_list:
        i.set_hitbox()
        if dragging_btn is None:
            data = i.drag((mouse_pos_x, mouse_pos_y), mouse_condition, spirit_pos_list)
            if data:
                spirit_list.append(spirit_dict[data[1]](data[0]))
                spirit_list[-1].set_frame()
        elif i is dragging_btn:
            data = i.drag((mouse_pos_x, mouse_pos_y), mouse_condition, spirit_pos_list)
            if data:
                spirit_list.append(spirit_dict[data[1]](data[0]))
                spirit_list[-1].set_frame()
        i.change_frame(dt)
        i.draw(screen)

    for i in spirit_list:
        i.change_frame(dt)
        i.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    pygame.display.flip()

pygame.quit()
