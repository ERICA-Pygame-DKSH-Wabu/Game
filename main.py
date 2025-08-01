import json
import pygame
from util import *
from button import *
from spirit import *
from effect import *
from monster import *

with open("story_wave.json", "r", encoding="utf-8") as f:
    wave_data = json.load(f)

wave_loaded = False

pygame.init()
spirit_type=["water","fire","grass","light","stone","dark"]
screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
smoke_effect_l=get_frame("asset/ui/effect",120,120,150)

spirit_dict={
    "water": Water_Spirit,
    "fire":Fire_Spirit,
    "grass":Grass_Spirit,
    "stone":Stone_Spirit,
    "light": Light_Spirit,
    "dark":Dark_Spirit
}

monster_dict={
    "water": Water_Monster,
    "fire":Fire_Monster,
    "grass":Grass_Monster,
    "stone":Stone_Monster,
    "light": Light_Monster,
    "dark":Dark_Monster
}

pygame.display.set_caption("forest witch")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

spirit_list=[]
monster_list=[]
effect_list=[]
spirit_pos_list = []
monster_pos_list = []
store_btn_list=[]
located_rect = []
 
for i in range(6):
    for j in range(4):
        x = i * 80 + j * 30 + 120
        y = screen_height - (j + 1) * 80 - 20
        rect = pygame.Rect(x, y, 30, 30)
        spirit_pos_list.append(rect)

for i in range(4):
    for j in range(4):
        x = i * 80 + j * 30 + 880
        y = screen_height - (j + 1) * 80 - 20
        rect = pygame.Rect(x, y, 30, 30)
        monster_pos_list.append(rect)

for i in range(6):
    store_btn_list.append(Store_Button(screen_width-100*i-100,50,pygame.rect.Rect(screen_width-100*i-100,60,70,80),spirit_type[i]))

wave = 3
fps = pygame.time.Clock()
playing = True

while playing:
    dt = fps.tick(60)
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_condition = pygame.mouse.get_pressed()
    key_condition = pygame.key.get_pressed()
    screen.fill(WHITE)

    for i in spirit_pos_list:
        pygame.draw.rect(screen, BLACK, i)

    for i in monster_pos_list:
        pygame.draw.rect(screen, RED, i)

    for m in monster_list:
        m.draw(screen)

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
                if data[0] in located_rect:
                    break
                else:
                    located_rect.append(data[0])
                    effect_list.append(effect(data[0].centerx,data[0].centery,smoke_effect_l))
                    spirit_list.append(spirit_dict[data[1]](data[0]))
                    spirit_list[-1].set_frame()

        i.change_frame(dt)
        i.draw(screen)

    if not wave_loaded and wave <= len(wave_data):
        monster_list.clear()  
        wave_data_current = wave_data[wave - 1]  

        for idx in range(1, 5):
            key = f"index_{idx}"
            if key in wave_data_current:
                for k, m_type in enumerate(wave_data_current[key]):
                    pos_index = k * 4 + (idx - 1)
                    if pos_index < len(monster_pos_list):
                        monster_list.append(monster_dict[m_type](monster_pos_list[pos_index]))
                        monster_list[-1].set_frame()

        wave_loaded = True

    for i in spirit_list:
        if key_condition[pygame.K_1]:
            i.condition="attack"
            i.change_condition()
        elif key_condition[pygame.K_2]:
            i.condition="idle"
            i.change_condition()
        elif key_condition[pygame.K_3]:
            i.condition="spin"
            i.change_condition()
        i.change_frame(dt)
        i.draw(screen)

    for i in monster_list:
        if key_condition[pygame.K_1]:
            i.condition="attack"
            i.change_condition()
        elif key_condition[pygame.K_2]:
            i.condition="idle"
            i.change_condition()
        elif key_condition[pygame.K_3]:
            i.condition="spin"
            i.change_condition()
        i.change_frame(dt)
        i.draw(screen)

        
    for effects in effect_list:
        effects.draw(screen)
        if effects.change_frame(dt):
            effect_list=[ i for i in effect_list if not i==effects]
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    pygame.display.flip()

pygame.quit()
