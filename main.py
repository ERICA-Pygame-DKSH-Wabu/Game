import json
import pygame
import itertools
from pos import *
from util import *
from button import *
from spirit import *
from effect import *
from monster import *
from background import *

with open("story_wave.json", "r", encoding="utf-8") as f:
    wave_data = json.load(f)

wave_loaded = False

pygame.init()
spirit_type=["water","fire","grass","light","stone","dark"]
screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
smoke_effect_l=get_frame("asset/ui/effect",120,120,150)

pygame.display.set_caption("forest witch")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

spirit_list=[[False for i in range(6)] for j in range(4)]
monster_list= [[] for i in range(4)]
effect_list=[]
spirit_pos_list = []
monster_pos_list = []
store_btn_list=[]
located_rect = [[False for i in range(6)] for j in range(4)]

wave_start_time = 0
wave_spawn_delay = 500  
monsters_spawned = 0
all_monsters_arrived = False
 
for i in range(6):
    for j in range(4):
        x = i * 80 + j * 25 + 270
        y = screen_height - (j + 1) * 60 - 40
        rect = pygame.Rect(x, y, 24, 24)
        spirit_pos_list.append(Pos(rect,(i,3-j)))

for i in range(4):
    monster_pos_list_temp = []
    for j in range(4):
        x = i * 80 + j * 30 + 880
        y = screen_height - (j + 1) * 80 - 20
        rect = pygame.Rect(x, y, 30, 30)
        monster_pos_list_temp.append(rect)
    monster_pos_list.append(monster_pos_list_temp)

for i in range(6):
    store_btn_list.append(Store_Button(screen_width-100*i-100,50,pygame.rect.Rect(screen_width-100*i-100,60,70,80),spirit_type[i]))

background_im=get_im("asset/ui/background_1.jpg")
background_im=set_im(background_im, 1280, 640,256,True)

wave = 1  
fps = pygame.time.Clock()
playing = True
def spawn_monsters_gradually(wave_data_current, current_time):
    global monsters_spawned, wave_start_time, all_monsters_arrived
    
    if monsters_spawned >= sum(len(wave_data_current.get(f"index_{i}", [])) for i in range(1, 5)):
        all_monsters_arrived = all(monster.has_arrived for monster in monster_list)
        return
    
    if current_time - wave_start_time < monsters_spawned * wave_spawn_delay:
        return
    
    monster_count = 0
    for row in range(1, 5):
        key = f"index_{row}"
        if key in wave_data_current:
            for col, m_type in enumerate(wave_data_current[key]):
                if monster_count == monsters_spawned:
                    if col < len(monster_pos_list):
                        print(row,spirit_list, monster_list)
                        if m_type=="dark":
                            monster_list[row-1].append(Dark_Monster(row-1,m_type))
                        if m_type=="light":
                            monster_list[row-1].append(Light_Monster(row-1,m_type))
                        if m_type=="water":
                            monster_list[row-1].append(Water_Monster(row-1,m_type))
                        if m_type=="fire":
                            monster_list[row-1].append(Fire_Monster(row-1,m_type))
                        if m_type=="grass":
                            monster_list[row-1].append(Grass_Monster(row-1,m_type))
                        if m_type=="stone":
                            monster_list[row-1].append(Stone_Monster(row-1,m_type))
                        monster_list[row-1][col].set_frame()

                        # new_monster = monster_dict[m_type](monster_pos_list[col][row-1])
                        # new_monster.set_target_rect(col, row-1)
                        # new_monster.set_frame()
                        # monster_list.append(new_monster)
                        monsters_spawned += 1
                        return
                monster_count += 1
while playing:
    dt = fps.tick(60)
    current_time = pygame.time.get_ticks()
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_condition = pygame.mouse.get_pressed()
    key_condition = pygame.key.get_pressed()
    screen.fill(WHITE)

    screen.blit(background_im,(0,0))

    for j in itertools.chain.from_iterable(monster_pos_list):
        pygame.draw.rect(screen, RED, j)


    if not wave_loaded and wave <= len(wave_data):
        monster_list = [[] for i in range(4)]
        wave_data_current = wave_data[wave - 1]
        monsters_spawned = 0
        wave_start_time = current_time
        all_monsters_arrived = False
        wave_loaded = True

    if wave_loaded and wave <= len(wave_data):
        spawn_monsters_gradually(wave_data[wave - 1], current_time)

    for i in spirit_list:
        for j in i:
            if j:
                if key_condition[pygame.K_1]:
                    j.condition="attack"
                    j.change_condition()
                elif key_condition[pygame.K_2]:
                    j.condition="idle"
                    j.change_condition()
                elif key_condition[pygame.K_3]:
                    j.condition="spin"
                    j.change_condition()
                j.set_target(monster_list[j.line])
                j.set_condition()
                j.change_frame(dt)
                j.draw(screen)

    for j in monster_list:
        for i in j:
            if key_condition[pygame.K_4]:
                i.condition="attack"
                i.change_condition()
            elif key_condition[pygame.K_5]:
                i.condition="idle" 
                i.change_condition()
            elif key_condition[pygame.K_6]:
                i.condition="spin"
                i.change_condition()
            j.set_target(monster_list[j.line])
            j.set_condition()
            i.move(dt)
            i.change_frame(dt) 
            i.draw(screen)

    for effects in effect_list:
        effects.draw(screen)
        if effects.change_frame(dt):
            effect_list = [i for i in effect_list if not i == effects]

    dragging_btn = None
    for btn in store_btn_list:
        if btn.dragging:
            dragging_btn = btn
            break

    for i in store_btn_list:
        i.set_hitbox()
        if dragging_btn is None:
            i.drag((mouse_pos_x, mouse_pos_y), mouse_condition, spirit_pos_list)
        elif i is dragging_btn:
            data = i.drag((mouse_pos_x, mouse_pos_y), mouse_condition, spirit_pos_list)
            if data:
                if data[0] in located_rect:
                    break
                else:
                    located_rect[data[2][1]][data[2][0]]=data[0]
                    effect_list.append(effect(data[0].centerx,data[0].centery,smoke_effect_l))
                    if data[1]=="dark":
                        spirit_list[data[2][1]][data[2][0]]=Dark_Spirit(data[0],data[2][1])
                    if data[1]=="light":
                        spirit_list[data[2][1]][data[2][0]]=Light_Spirit(data[0],data[2][1])
                    if data[1]=="water":
                        spirit_list[data[2][1]][data[2][0]]=Water_Spirit(data[0],data[2][1])
                    if data[1]=="fire":
                        spirit_list[data[2][1]][data[2][0]]=Fire_Spirit(data[0],data[2][1])
                    if data[1]=="grass":
                        spirit_list[data[2][1]][data[2][0]]=Grass_Spirit(data[0],data[2][1])
                    if data[1]=="stone":
                        spirit_list[data[2][1]][data[2][0]]=Stone_Spirit(data[0],data[2][1])
                    spirit_list[data[2][1]][data[2][0]].set_frame()

        i.change_frame(dt)
        i.draw(screen)

    if all_monsters_arrived and key_condition[pygame.K_SPACE]:
        wave += 1
        wave_loaded = False
        if wave > len(wave_data):
            wave = 1  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    font = pygame.font.Font(None, 36)
    wave_text = font.render(f"Wave: {wave}", True, BLACK)
    screen.blit(wave_text, (10, 10))
    
    info_font = pygame.font.Font(None, 24)
    info_texts = [
        "1,2,3: Spirit states (attack, idle, spin)",
        "4,5,6: Monster states (attack, idle, spin)", 
        "SPACE: Next wave (when all monsters arrived)",
        f"Monsters arrived: {sum(1 for m in monster_list if m.has_arrived)}/{len(monster_list)}"
    ]

    if wave > 1:
        background_im=get_im("asset/ui/background_2.jpg")

    for i, text in enumerate(info_texts):
        info_surface = info_font.render(text, True, BLACK)
        screen.blit(info_surface, (10, 50 + i * 25))
    pygame.display.flip()
pygame.quit()