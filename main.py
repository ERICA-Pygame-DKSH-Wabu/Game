import json
import pygame
import itertools
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

wave_start_time = 0
wave_spawn_delay = 500  
monsters_spawned = 0
all_monsters_arrived = False
 
for i in range(6):
    for j in range(4):
        x = i * 80 + j * 25 + 270
        y = screen_height - (j + 1) * 60 - 40
        rect = pygame.Rect(x, y, 24, 24)
        spirit_pos_list.append(rect)

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

background_im=get_im("asset/ui/background.jpg")
background_im=set_im(background_im, 1280, 640,256,True)

wave = 1  
fps = pygame.time.Clock()
playing = True

def spawn_monsters_gradually(wave_data_current, current_time):
    """몬스터를 점진적으로 스폰하는 함수"""
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
                        new_monster = monster_dict[m_type](monster_pos_list[col][row-1])
                        new_monster.set_target_rect(col, row-1)
                        new_monster.set_frame()
                        monster_list.append(new_monster)
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
        monster_list.clear()
        wave_data_current = wave_data[wave - 1]
        monsters_spawned = 0
        wave_start_time = current_time
        all_monsters_arrived = False
        wave_loaded = True

    if wave_loaded and wave <= len(wave_data):
        spawn_monsters_gradually(wave_data[wave - 1], current_time)

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
        if key_condition[pygame.K_4]:
            i.condition="attack"
            i.change_condition()
        elif key_condition[pygame.K_5]:
            i.condition="idle" 
            i.change_condition()
        elif key_condition[pygame.K_6]:
            i.condition="spin"
            i.change_condition()
        
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
                    spirit_list = sorted(spirit_list, key=lambda obj: obj.hitbox.centery)

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
    for i, text in enumerate(info_texts):
        info_surface = info_font.render(text, True, BLACK)
        screen.blit(info_surface, (10, 50 + i * 25))
    pygame.display.flip()

pygame.quit()