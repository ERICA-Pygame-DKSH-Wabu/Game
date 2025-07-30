import json
import pygame
from util import *
from button import *
from spirit import *
from effect import *
from monster import *

with open("story_wave.json", "r", encoding="utf-8") as f:
    wave_data = json.load(f)

wave1 = wave_data[0] #임시

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

pygame.display.set_caption("forest witch")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

spirit_list=[]
effect_list=[]
spirit_pos_list = []
monster_pos_list = []
store_btn_list=[]
located_rect = []

for i in range(6):
    for j in range(4):
        x = i * 120 + j * 15 + 140
        y = screen_height - (j + 1) * 100 - 50
        rect = pygame.Rect(x, y, 40, 40)
        spirit_pos_list.append(rect)

# for i in range(6):
#     for j in range(4):
#         x = i * 80 + j * 30 + 120
#         y = screen_height - (j + 1) * 80 - 20
#         rect = pygame.Rect(x, y, 30, 30)
#         spirit_pos_list.append(rect)

for i in range(4):
    for j in range(4):
        x = i * 100 + j * 15 + 880
        y = screen_height - (j + 1) * 100 - 50
        rect = pygame.Rect(x, y, 40, 40)
        monster_pos_list.append(rect)

for idx in range(1, 5):  # index_1 ~ index_4
    key = f"index_{idx}"
    if key in wave1:
        for k, m_type in enumerate(wave1[key]):
            # k: y좌표(행), idx-1: x좌표(열)
            pos_index = k * 4 + (idx - 1)
            if pos_index < len(monster_pos_list):
                monster = Monster(monster_pos_list[pos_index], m_type)
                monster.set_frame()
                monster.img = monster.frame["idle"][0]  # 기본 이미지 설정
                monster_list.append(monster)
        

for i in  range(6):
    store_btn_list.append(Store_Button(screen_width-100*i-100,50,pygame.rect.Rect(screen_width-100*i-100,60,70,80),spirit_type[i]))

fps = pygame.time.Clock()
playing = True

fps = pygame.time.Clock()
playing = True

# 시작 시 wave 1 자동 배치
update_wave(wave_data, 0, monster_pos_list)

while playing:
    dt = fps.tick(60)
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_condition = pygame.mouse.get_pressed()
    screen.fill(WHITE)

    # 정령/몬스터 배치 위치 표시
    for i in spirit_pos_list:
        pygame.draw.rect(screen, BLACK, i)
    for i in monster_pos_list:
        pygame.draw.rect(screen, RED, i)
    for m in get_monsters():
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
                    effect_list.append(effect(data[0].centerx, data[0].centery, smoke_effect_l))
                    spirit_list.append(spirit_dict[data[1]](data[0]))
                    spirit_list[-1].set_frame()
        i.change_frame(dt)
        i.draw(screen)

    for i in spirit_list:
        if mouse_condition[0]:
            i.condition="attack"
            i.change_condition()
        elif mouse_condition[1]:
            i.condition="idle"
            i.change_condition()
        elif mouse_condition[2]:
            i.condition="spin"
            i.change_condition()
            
        i.change_frame(dt)
        i.draw(screen)

    for effects in effect_list:
        effects.draw(screen)
        if effects.change_frame(dt):
            effect_list = [i for i in effect_list if i != effects]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        elif event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:
                wave_num = event.key - pygame.K_0
                if 1 <= wave_num <= len(wave_data):
                    update_wave(wave_data, wave_num - 1, monster_pos_list)

    pygame.display.flip()

pygame.quit()

