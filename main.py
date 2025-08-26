
import json
import pygame
from pos import *
from cut import *
pygame.init()

with open("story_wave.json", "r", encoding="utf-8") as f:
    wave_data = json.load(f)

wave_loaded = False
alpha=175
click=False
spirit_type=["water","fire","grass","light","stone","dark"]
screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
from util import *
subt_bg=get_frame("asset/ui/subtitle_bg",1280,840,255)
boss_font = get_font("asset/witch.ttf",36)
monster_font = get_font("asset/monster.ttf", 36)
witch_font = get_font("asset/witch.ttf", 36)

smoke_effect_l=get_frame("asset/ui/appear_effect",120,120,150)
explosion_effect=get_frame("asset/ui/explosion_effect",160,160,200)
pygame.display.set_caption("witch")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0) 
from button import *
from spirit import *
from effect import *
from monster import *
from background import *


mana=10000

witch_frame_index=0
witch_frame=get_frame("asset/ui/witch",640,640,230)
start_im=get_im("asset/ui/start.png")
start_im=set_im(start_im,256,256,256,True)
start_background_im=get_im("asset/ui/start_background.png")
start_background_im=set_im(start_background_im,1280, 640,256,True)
scene="start"
fade_surface = pygame.Surface((1280, 640))
fade_surface.fill((0, 0, 0))
fade_in = True
fade_alpha = 255
fade_surface = pygame.Surface((screen_width, screen_height))
fade_surface.fill((0,0,0))


start_alpha = 0
start_dir = 1
start_pulse = False


spirit_list=[[False for i in range(6)] for j in range(4)]
monster_list=[[] for i in range(4)]
effect_list=[]
spirit_pos_list = []
monster_pos_list = []
store_btn_list=[]
located_rect = [[False for i in range(6)] for j in range(4)]
monster_effect_l=[]
spirit_effect_l=[]

if_story=False
subt_bg_frame_index=0
story_str=[["도통 익숙해질 수가 없네....이 숲은 ",witch_font],["그...ㅁ..해.. ",monster_font],["....마 녀 ",boss_font],["ㅍ.....기....해.. ",monster_font],["하여간..못말린다니깐 ",witch_font],["ㅇ...ㅙ..그..랬...어...? ",monster_font],["멈춰...! ",boss_font]]
text_index=0
waiting_game=False
story_witch=get_im("asset/ui/story_witch.png")
story_witch=set_im(story_witch,640,640,240,False)
story_boss=get_im("asset/ui/story_boss.png")
story_boss=set_im(story_boss,550,550,240,True)
change_scene="witch"

wave_start_time = 0
wave_spawn_delay = 500  
monsters_spawned = 0
monster_count = 0
all_monsters_arrived = False
 
for i in range(6):
    for spirit in range(4):
        x = i * 80 + spirit * 25 + 260
        y = screen_height - (spirit + 1) * 60 - 50
        rect = pygame.Rect(x, y, 50, 50)
        spirit_pos_list.append(Pos(rect,(i,3-spirit)))#히트박스,행렬
for i in range(4):
    x = screen_width + i * 25 + 100
    y = screen_height - (i + 1) * 60 - 40
    rect = pygame.Rect(x, y, 50, 50)
    monster_pos_list.append(Pos(rect,(i,3-spirit)))#히트박스,행렬
monster_pos_list.reverse()


for monster in range(6):
    store_btn_list.append(Store_Button(screen_width-100*monster-100,50,pygame.rect.Rect(screen_width-100*monster-100,60,70,80),spirit_type[monster]))

background_im=get_im("asset/ui/background_1.jpg")
background_im=set_im(background_im, 1280, 640,256,True)
fps = pygame.time.Clock()
playing = True
first=True

def spawn_wave(wave_num):
    if wave_num < 1 or wave_num > len(wave_data):
        return
    wave_info = wave_data[wave_num - 1]
    for row in range(1, 5):
        key = f"index_{row}"
        row_list = wave_info.get(key, [])
        if not row_list:
            continue
        row_idx = row - 1
        for col_idx, m_type in enumerate(row_list):
            try:
                base = monster_pos_list[row_idx].rect
            except Exception:
                base = monster_pos_list[row_idx].rect
            rect = base.rect if hasattr(base, "rect") else base
            spawn_rect = pygame.Rect(rect.left + 80 * col_idx, rect.top, rect.width, rect.height)
            if m_type == "dark":
                new_mon = Dark_Monster(spawn_rect, row_idx, "dark")
            elif m_type == "light":
                new_mon = Light_Monster(spawn_rect, row_idx, "light")
            elif m_type == "water":
                new_mon = Water_Monster(spawn_rect, row_idx, "water")
            elif m_type == "fire":
                new_mon = Fire_Monster(spawn_rect, row_idx, "fire")
            elif m_type == "grass":
                new_mon = Grass_Monster(spawn_rect, row_idx, "grass")
            elif m_type == "stone":
                new_mon = Stone_Monster(spawn_rect, row_idx, "stone")
            else:
                continue
            if hasattr(new_mon, "set_frame"):
                new_mon.set_frame()
            if hasattr(new_mon, "set_target_rect"):
                new_mon.set_target_rect(col_idx)
            monster_list[row_idx].append(new_mon)
button_=False
story_index=0
story_scene=0
cut_l=[]
im_size=get_im("asset/story/story1/1.png")
im_size=im_size.get_size()
cut_l.append(get_frame("asset/story/story1",1280,640,256))
fade_surface.set_alpha(255)
cut_l.append(fade_surface)
cut_l.append(get_frame("asset/story/story2",1280,640,256))
cut_l.append(fade_surface)
cut__l=[Cut(0,0,254,cut_l[0][0])]
scene_change=Cut(0,0,0,fade_surface)
wave=1
wave_time=30
wave_speed=1
while playing:
    dt = fps.tick(60)
    current_time = pygame.time.get_ticks()
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_condition = pygame.mouse.get_pressed()
    key_condition = pygame.key.get_pressed()
    if scene=="story":
        screen.fill((255,255,255))
        try:
            for cut_ in cut__l:
                cut_.draw(screen)
                if (cut_.fade_in(dt) and cut_==cut__l[-1]) and button_:
                    cut__l.append(Cut(0,0,0,cut_l[story_scene][story_index]))
                    story_index+=1
                    button_=False
        except IndexError:
            if button_:
                change_scene="game"
                scene_change.i=1
    elif scene=="game":
        if not if_story:
            text_index=0
            subt_bg_frame_index
            if story_str[wave-1]:
                if_story=True
            screen.blit(background_im,(0,0))
            if first:
                fade_surface.set_alpha(175)
                screen.blit(fade_surface,(0,0))
            if wave_time>100:
                spawn_wave(wave)
                wave+=1
                wave_time=0
            wave_time+=dt*wave_speed*0.005
            for i in spirit_list:
                for spirit in i:
                    if spirit:
                        spirit.set_target(monster_list[spirit.line])
                        spirit.set_condition()
                        spirit.change_frame(dt)
                        spirit.draw(screen)
                        if spirit.condition=="attack" and int(spirit.frame_index)==spirit.attack_time and spirit.if_attack:
                            if spirit.name=="grass":
                                if spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)]:
                                    if spirit_list[spirit.line].index(spirit)+1<6 and spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1] :
                                        spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].health+=30
                                        if spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].health>spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].max_health:
                                            spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].health=spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].max_health
                                    if spirit_list[spirit.line].index(spirit)-1>0 and spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1] :
                                        spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].health+=30
                                        if spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].health>spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].max_health:
                                            spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].health=spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].max_health
                                    spirit.health+=30
                                    if spirit.health>spirit.max_health:
                                        spirit.health=spirit.max_health
                            elif spirit.name=="water":
                                mana+=50
                            else:
                                attack=attack_effect(spirit.target,spirit.hitbox.centery,explosion_effect,64,spirit.damage)
                                for j in monster_list:
                                    for i in j:
                                        if i.hitbox.colliderect(attack.hitbox):
                                            i.health-=attack.damage
                                spirit_effect_l.append(attack)
                            spirit.if_attack=False
                        if spirit.health<=0:
                            located_rect[spirit.line][spirit_list[spirit.line].index(spirit)]=False
                        if spirit.if_dead(dt):
                            effect_list.append(effect(spirit.hitbox.centerx,spirit.hitbox.centery,smoke_effect_l))
                            spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)]=False
            for line_monsters in monster_list:
                for monster in line_monsters:
                    monster.set_target(located_rect[monster.index])
                    monster.set_condition()
                    monster.change_frame(dt)
                    if monster.condition=="attack" and int(monster.frame_index)==monster.attack_time and monster.if_attack:
                        attack=attack_effect(monster.target,monster.hitbox.centery,explosion_effect,64,monster.damage)
                        monster.if_attack=False
                        for j in spirit_list:
                            for i in j:
                                if i:
                                    if i.hitbox.colliderect(attack.hitbox):
                                        i.health-=attack.damage
                        monster_effect_l.append(attack)
                    monster.draw(screen)       
                    if monster.if_dead(dt):
                        effect_list.append(effect(monster.hitbox.centerx,monster.hitbox.centery,smoke_effect_l))
                        monster_list[monster.line]=[i for i in monster_list[monster.line] if not monster==i]
                    else:
                        monster.move(dt)
            for effects in effect_list:
                effects.draw(screen)
                if effects.change_frame(dt):
                    effect_list = [i for i in effect_list if not i == effects]

            for effects in monster_effect_l:
                effects.draw(screen)
                if effects.change_frame(dt):
                    monster_effect_l = [i for i in monster_effect_l if not i == effects]

            for effects in spirit_effect_l:
                effects.draw(screen)
                if effects.change_frame(dt):
                    spirit_effect_l = [i for i in spirit_effect_l if not i == effects]
            dragging_btn = None
            for btn in store_btn_list:
                if btn.dragging:
                    dragging_btn = btn
                    break
            for monster in store_btn_list:
                monster.set_hitbox()
                if dragging_btn is None:
                    monster.drag((mouse_pos_x, mouse_pos_y), mouse_condition, spirit_pos_list)
                elif monster is dragging_btn:
                    data = monster.drag((mouse_pos_x, mouse_pos_y), mouse_condition, spirit_pos_list) 
                    if data:
                        if  located_rect[data[2][1]][data[2][0]]:#data-(pos.rect, self.s_type,j.pos)
                            break
                        else:
                            if data[1]=="dark" and mana>=200:
                                spirit_list[data[2][1]][data[2][0]]=Dark_Spirit(data[0],data[2][1])
                                mana-=200
                            if data[1]=="light" and mana>=200:
                                spirit_list[data[2][1]][data[2][0]]=Light_Spirit(data[0],data[2][1])
                                mana-=200
                            if data[1]=="water" and mana>=100:
                                spirit_list[data[2][1]][data[2][0]]=Water_Spirit(data[0],data[2][1])
                                mana-=100
                            if data[1]=="fire" and mana>=175:
                                spirit_list[data[2][1]][data[2][0]]=Fire_Spirit(data[0],data[2][1])
                                mana-=175
                            if data[1]=="grass" and mana>=175:
                                spirit_list[data[2][1]][data[2][0]]=Grass_Spirit(data[0],data[2][1])
                                mana-=175
                            if data[1]=="stone" and mana>=150:
                                spirit_list[data[2][1]][data[2][0]]=Stone_Spirit(data[0],data[2][1])
                                mana-=150
                            if spirit_list[data[2][1]][data[2][0]]:
                                spirit_list[data[2][1]][data[2][0]].set_frame()
                                located_rect[data[2][1]][data[2][0]]=data[0]
                                effect_list.append(effect(data[0].centerx,data[0].centery,smoke_effect_l))

                monster.change_frame(dt)
                monster.draw(screen)
                click=False
                if first:
                    if_story=True
                first=False
        else:
            screen.blit(background_im,(0,0))
            for i in spirit_list:
                for spirit in i:
                    if spirit:
                        spirit.draw(screen)
            for line_monsters in monster_list:
                for monster in line_monsters:
                    monster.draw(screen)       
            for effects in effect_list:
                effects.draw(screen)
            for effects in monster_effect_l:
                effects.draw(screen)
            for effects in spirit_effect_l:
                effects.draw(screen)
            for button in store_btn_list:
                button.draw(screen)
            if not click:
                alpha=175
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface,(0,0))
            if story_str[wave-1][1]==witch_font:
                screen.blit(story_witch,(-100,100))
            elif story_str[wave-1][1]==boss_font:
                screen.blit(story_boss,(screen_width-520,200))
            screen.blit(subt_bg[int(subt_bg_frame_index)],(0,screen_height//2-225))
            if int(subt_bg_frame_index)==4:
                subt_bg_frame_index=4
                if story_str[wave-1]:
                    draw_text(screen,screen_width//2,screen_height-100,story_str[wave-1][0],story_str[wave-1][1],text_index)
                    if int(text_index)==len(story_str[wave-1][0]):
                        text_index=len(story_str[wave-1][0])
                        if mouse_condition[0]:
                            scene_change.i=1
                    else:    
                        text_index+=dt*0.01
            else:
                subt_bg_frame_index+=dt*0.05


    elif scene=="start":
        screen.blit(start_background_im,(0,0))

        start_draw = start_im.copy()
        start_draw.set_alpha(int(start_alpha)*0.7)
        screen.blit(start_draw,(screen_width//2 - start_im.get_width()//2, screen_height//2+64))
        if start_pulse:
            step = 0.15 * round(dt, 3)
        else:
            step = 0.08 * round(dt, 3)
        if fade_in:
            fade_alpha -= step
            if fade_alpha <= 0:
                fade_alpha = 0
                fade_in = False
                witch_fade_in = True
            fade_surface.set_alpha(int(fade_alpha))
            screen.blit(fade_surface, (0,0))
        elif witch_fade_in:
            witch_frame_index += step*0.15
            if witch_frame_index >= len(witch_frame)-1:
                witch_frame_index = len(witch_frame)-1
                witch_fade_in = False
                start_pulse = True
        elif start_pulse:
            start_alpha += step * start_dir
            if start_alpha >= 255:
                start_alpha = 255
                start_dir = -1
            elif start_alpha <= 0:
                start_alpha = 0
                start_dir = 1
        if witch_frame_index:
            screen.blit(witch_frame[int(witch_frame_index)],(-witch_frame[int(witch_frame_index)].get_width()//2+screen_width//2,-20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.MOUSEBUTTONDOWN and scene=="start":
            change_scene="story"
            scene_change.i=1
        if event.type == pygame.MOUSEBUTTONUP:
            if scene=="story":
                button_=True
    
    if scene_change.fade_inout(dt):
        scene=change_scene
        if scene=="story":
            story_index=0
        elif scene=="game" and if_story:
            story_str[wave-1]=False
            if_story=False

    scene_change.draw(screen)
    pygame.display.flip()
pygame.quit()