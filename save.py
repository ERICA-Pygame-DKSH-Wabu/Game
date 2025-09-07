import json
import random
import pygame
from pos import *
from cut import *
pygame.init()

with open("story_wave.json", "r", encoding="utf-8") as f:
    wave_data = json.load(f)

wave_loaded = False
alpha=175
click=False
spirit_type=("water","fire","grass","light","stone","dark")
price=(2,4,4,5,3,5)
screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("witch")
from witch import * 
from util import *
from button import *
from spirit import *
from effect import *
from monster import *
from background import *
from mana import *
witch1=witch([pygame.Rect(210+25*i,screen_height - (i + 1) * 60 - 40, 32,32) for i in range(4)])
subt_bg=get_frame("asset/ui/subtitle_bg",1280,840,255)
subt_bg1=get_frame("asset/ui/subtitle_bg",720,840,255)
boss_font = get_font("asset/witch.ttf",36)
monster_font = get_font("asset/monster.ttf", 36)
witch_font = get_font("asset/witch.ttf", 36)
data=False
spirit_attack_dict={
    "grass":get_frame("asset/spirit_attack_effect/grass",256,192,100),
    "light":get_frame("asset/spirit_attack_effect/light",96,96,230),
    "water":get_frame("asset/spirit_attack_effect/water",160,160,140),
    "stone":get_frame("asset/spirit_attack_effect/stone",64,64,180,False),
    "fire":get_frame("asset/spirit_attack_effect/fire",128,96,180),
    "dark":get_frame("asset/spirit_attack_effect/dark",128,128,180),
}
monster_attack_dict={
    "grass":get_frame("asset/monster_attack_effect/grass",128,128,220),
    "light":get_frame("asset/monster_attack_effect/light",128,128,256),
    "water":get_frame("asset/monster_attack_effect/water",128,128,220),
    "stone":get_frame("asset/monster_attack_effect/stone",128,128,180,False),
    "fire":get_frame("asset/monster_attack_effect/fire",96,96,200,False),
    "dark":get_frame("asset/monster_attack_effect/dark",128,128,200),
}
smoke_effect_l=get_frame("asset/ui/appear_effect",120,120,150)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0) 
gameover=get_frame("asset/gameover",700,500,256)
gameover=[invert_surface_color(i)  for i in gameover]
center = ( 208, screen_height // 2+20)
mana_list = [Mana(center) for i in range(2)]
orbit_angle = 0.7 % 360
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
skip=get_im("asset/ui/skip.png")
skip=set_im(skip,192,192,200,True)
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
appear=False
if_story=False
subt_bg_frame_index=0
story_l=[["대체 어디로간거니..?",witch_font],False,False,False,[".....",monster_font],False,False,False,["마녀... ",boss_font],False,["포...기..ㅎ..ㅐ.. ",monster_font],False,False,False,["하아...정말 성가시다니까 ",witch_font],["포기하면 편할텐데말이지...",witch_font],False,["ㅅ..싫..어",monster_font],False,["그만해..!",boss_font],["피곤하네...이짓도",witch_font],[".....",boss_font]]
text_index=0
waiting_game=False
story_witch=get_im("asset/ui/story_witch.png")
story_witch=set_im(story_witch,640,640,240,False)
story_boss=get_im("asset/ui/story_boss.png")
story_boss=set_im(story_boss,550,550,240,True)
change_scene="witch"
effect_frame=get_frame("asset/effect",50,50,235)
full_charge=False
monsters_spawned = 0
monster_count = 0
all_monsters_arrived = False


funny=get_frame("asset/funny",1280,640,256)
funny_index=0
for i in range(6):
    for spirit in range(4):
        x = i * 80 + spirit * 25 + 260
        y = screen_height - (spirit + 1) * 60 - 50
        rect = pygame.Rect(x, y, 50, 50)
        spirit_pos_list.append(Pos(rect,(i,3-spirit)))
for i in range(4):
    x = screen_width + i * 25 + 100
    y = screen_height - (i + 1) * 60 - 40
    rect = pygame.Rect(x, y, 50, 50)
    monster_pos_list.append(Pos(rect,(i,3-spirit)))
monster_pos_list.reverse()
for monster in range(6):
    store_btn_list.append(Store_Button(screen_width-100*monster-100,50,pygame.Rect(screen_width-100*monster-100,60,70,80),spirit_type[monster]))
background_im=[get_im(f"asset/ui/background_{i}.jpg") for i in [1,2]]
background_im=[set_im(i, 1280, 640,256,True)for i in background_im]
fps = pygame.time.Clock()
playing = True
first=True
power=get_frame("asset/power",1280,720,256)
power=remove_white(power)
tuto_index=0
tuto_str_index=0
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
            spawn_rect = pygame.Rect(rect.left-100 + 55 * col_idx, rect.top, rect.width, rect.height)
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
tuto=True
damaged=False
button_=False
story_index=0
story_scene=0
im_size=get_im("asset/story/story1/1.png")
im_size=im_size.get_size()

scene_l = [
    get_frame("asset/story/story1", 1280, 640, 256),
    get_frame("asset/story/story2", 1280, 640, 256)]

story_scene = 0
story_index = 0
button_ = False
cut_l=[]
reset=False
scene_change=Cut(0,0,0,fade_surface)
wave=1
wave_time=0
wave_speed=1
change=False
tuto_str_l=["마나는 가장 기본적인 자원입니다.","물의 정령을 소환해 마나를 충전하십시오.","마나를 사용해 정령을 소환할 수 있습니다.","웨이브가 시작될때 마다 몬스터가 몰려옵니다.","정령들로 몬스터를 물리치십시오."]
def run_game():
    global playing, alpha, click, orbit_angle, witch_frame_index, scene, fade_in, fade_alpha, start_alpha, start_dir, start_pulse
    global appear, if_story, subt_bg_frame_index, text_index, waiting_game, change_scene, full_charge, monsters_spawned, monster_count
    global all_monsters_arrived, button_, story_index, story_scene, wave, wave_time, wave_speed, first,reset
    global mana_list, spirit_list, monster_list, effect_list, monster_effect_l, spirit_effect_l, located_rect, store_btn_list
    global witch1, story_l, background_im, subt_bg, story_witch, story_boss, effect_frame, witch_font, boss_font, monster_font,change
    global fade_surface,power, witch_frame,funny,funny_index ,start_im, start_background_im, skip, im_size, cut_l,price, scene_change,tuto,tuto_str_index,tuto_index,tuto_str_l
    fps = pygame.time.Clock()
    playing = True
    first = True
    while playing:
        dt = fps.tick(60)
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        mouse_condition = pygame.mouse.get_pressed()
        if reset:
            story_l=[["도통 익숙해질 수가 없네....이 숲은 ",witch_font],False,False,False,["그...ㅁ..해.. ",monster_font],False,False,False,["....마 녀 ",boss_font],False,["ㅍ.....기....해.. ",monster_font],False,False,["하여간..못말린다니깐 ",witch_font],False,False,False,["ㅇ...ㅙ..그..랬...어...? ",monster_font],False,["그만해..! ",boss_font],["피곤하네...이짓도",witch_font],[".....",boss_font]]
            wave = 1
            wave_time = 0
            wave_speed = 1
            if_story = False
            text_index = 0
            subt_bg_frame_index = 0

            spirit_list = [[False for _ in range(6)] for _ in range(4)]
            monster_list = [[] for _ in range(4)]
            effect_list = []
            spirit_effect_l = []
            monster_effect_l = []
            located_rect = [[False for _ in range(6)] for _ in range(4)]

            mana_list = [Mana(center) for _ in range(2)]
            store_btn_list.clear()
            for i in range(6):
                store_btn_list.append(Store_Button(
                    screen_width - 100 * i - 100, 50,
                    pygame.Rect(screen_width - 100 * i - 100, 60, 70, 80),
                    spirit_type[i]
                ))

            witch1 = witch([pygame.Rect(210 + 25 * i, screen_height - (i + 1) * 60 - 40, 32, 32) for i in range(4)])
            
            button_ = False
            click = False
            appear = False
            full_charge = False
            fade_alpha = 255
            fade_in = True
            witch_frame_index = 0
            first = True
            cut_l = []
            story_index = 0
            story_scene = 0
            change = False
            funny_index = 0
            reset=False

        if scene == "story":
            screen.fill((0, 0, 0))

            for cut in cut_l:
                cut.draw(screen)

            if not scene_change.i == 1:
                screen.blit(skip,(-32,screen_height-160))
                if not cut_l and story_scene < len(scene_l):
                    story_index = 0
                    cut_l.append(Cut(0, 0, 0, scene_l[story_scene][story_index]))
                    story_index += 1

                elif cut_l and cut_l[-1].fade_in(dt) and button_:
                    if story_index < len(scene_l[story_scene]):
                        button_ = False
                        cut_l.append(Cut(0, 0, 0, scene_l[story_scene][story_index]))
                        story_index += 1
                    elif story_scene==0:
                        cut_l = []
                        story_index = 0
                        story_scene += 1
                        scene_change.i = 1
                        change_scene = "game"
                        button_ = False
                    else:
                        scene="ending"
                        button_=False


        elif scene=="game":
            if witch1.health<=0:
                scene_change.i=1
                change_scene="gameover"
            orbit_angle = (orbit_angle + 0.7) % 360

            if wave > len(story_l):
                scene_change.i = 1
                change_scene="story"

            elif not if_story and wave <= len(story_l):
                text_index = 0
                subt_bg_frame_index=0
                if story_l[wave-1]:
                    if_story = True
                if wave<=10:
                    screen.blit(background_im[0],(0,0))
                else:
                    screen.blit(background_im[1],(0,0))
                if first:
                    fade_surface.set_alpha(175)
                    screen.blit(fade_surface,(0,0))
                if wave>=19:
                    wave_speed=1000
                wave_time += dt * wave_speed * 0.005 *15
                if wave_time > 100:
                    spawn_wave(wave)
                    wave += 1
                    wave_time = 0
                for i in spirit_list:
                    for spirit in i:
                        if spirit:
                            spirit.set_target(i.hitbox for i in monster_list[spirit.line])
                            spirit.set_condition()
                            spirit.change_frame(dt)
                            spirit.draw(screen)
                            if spirit.condition=="attack" and int(spirit.frame_index)==spirit.attack_time and spirit.if_attack:
                                if spirit.name=="grass":
                                    if spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)]:
                                        if spirit_list[spirit.line].index(spirit)+1<6 and spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1]:
                                            spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].health+=30
                                            effect_list.append(effect(spirit.hitbox.centerx+80,spirit.hitbox.centery-20,spirit_attack_dict["grass"]))
                                            if spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].health>spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].max_health:
                                                spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].health=spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)+1].max_health
                                        if spirit_list[spirit.line].index(spirit)-1>0 and spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1]:
                                            spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].health+=30
                                            effect_list.append(effect(spirit.hitbox.centerx-80,spirit.hitbox.centery-20,spirit_attack_dict["grass"]))
                                            if spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].health>spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].max_health:
                                                spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].health=spirit_list[spirit.line][spirit_list[spirit.line].index(spirit)-1].max_health
                                        spirit.health+=30
                                        if spirit.health>spirit.max_health:
                                            spirit.health=spirit.max_health
                                            effect_list.append(effect(spirit.hitbox.centerx,spirit.hitbox.centery-20,spirit_attack_dict["grass"]))
                                elif spirit.name=="water":
                                    if len(mana_list)<12:
                                        mana_list.append(Mana(center))
                                    else:
                                        if not full_charge:
                                            for k in range(12):
                                                if not mana_list[k].charge:
                                                    mana_list[k].charge=True
                                                    break
                                        full_charge=all(m.charge for m in mana_list)
                                    effect_list.append(effect(spirit.hitbox.centerx,spirit.hitbox.centery-20,spirit_attack_dict["water"]))
                                else:
                                    attack=attack_effect(spirit.target,spirit.hitbox.centery,spirit_attack_dict[spirit.name],32,spirit.damage)
                                    for j in monster_list:
                                        for m in j:
                                            if m.hitbox.colliderect(attack.hitbox):
                                                m.health-=attack.damage
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
                        monster.set_hitbox()
                        if monster.condition=="attack" and int(monster.frame_index)==monster.attack_time and monster.if_attack:
                            attack=attack_effect(monster.target,monster.hitbox.top,monster_attack_dict[monster.name],16,monster.damage)
                            monster.if_attack=False
                            for rect in witch1.hitbox:
                                if rect.colliderect(attack.hitbox):
                                    witch1.health-=attack.damage
                                    damaged=True
                            for j in spirit_list:
                                for s in j:
                                    if s and s.hitbox.colliderect(attack.hitbox):
                                        s.health-=attack.damage
                            monster_effect_l.append(attack)
                        monster.draw(screen)
                        if monster.if_dead(dt):
                            effect_list.append(effect(monster.hitbox.centerx,monster.hitbox.centery,smoke_effect_l))
                            monster_list[monster.line]=[i for i in monster_list[monster.line] if not monster==i]
                        else:
                            monster.move(dt)
                dragging_btn=None
                for btn in store_btn_list:
                    if btn.dragging:
                        dragging_btn=btn
                        break
                for button in store_btn_list:
                    button.set_hitbox()
                    if dragging_btn is None:
                        button.drag((mouse_pos_x,mouse_pos_y),mouse_condition,spirit_pos_list)
                    elif button is dragging_btn:
                        data=button.drag((mouse_pos_x,mouse_pos_y),mouse_condition,spirit_pos_list)
                        if data:
                            if located_rect[data[2][1]][data[2][0]]:
                                break
                            else:
                                appear=True
                                effect_list.append(effect(center[0]+55,center[1]+40,effect_frame))
                                if data[1]=="dark" and len(mana_list)>=5:
                                    spirit_list[data[2][1]][data[2][0]]=Dark_Spirit(data[0],data[2][1])
                                    mana_list=mana_list[:-5]
                                if data[1]=="light" and len(mana_list)>=5:
                                    spirit_list[data[2][1]][data[2][0]]=Light_Spirit(data[0],data[2][1])
                                    mana_list=mana_list[:-5]
                                if data[1]=="water" and len(mana_list)>=2:
                                    spirit_list[data[2][1]][data[2][0]]=Water_Spirit(data[0],data[2][1])
                                    mana_list=mana_list[:-2]
                                if data[1]=="fire" and len(mana_list)>=4:
                                    spirit_list[data[2][1]][data[2][0]]=Fire_Spirit(data[0],data[2][1])
                                    mana_list=mana_list[:-4]
                                if data[1]=="grass" and len(mana_list)>=4:
                                    spirit_list[data[2][1]][data[2][0]]=Grass_Spirit(data[0],data[2][1])
                                    mana_list=mana_list[:-4]
                                if data[1]=="stone" and len(mana_list)>=3:
                                    spirit_list[data[2][1]][data[2][0]]=Stone_Spirit(data[0],data[2][1])
                                    mana_list=mana_list[:-3]
                                if spirit_list[data[2][1]][data[2][0]]:
                                    spirit_list[data[2][1]][data[2][0]].set_frame()
                                    located_rect[data[2][1]][data[2][0]]=data[0]
                                    effect_list.append(effect(data[0].centerx,data[0].centery,smoke_effect_l))
                    if price[spirit_type.index(button.s_type)]<=len(mana_list):    
                        button.change_frame(dt)
                    else:
                        button.im=button.frame[0]
                    button.draw(screen)
                for i,mana in enumerate(mana_list):
                    mana.update(i,len(mana_list),orbit_angle)
                    if mana.y<=mana.center[1]:
                        mana.draw(screen)
                witch1.set_condition(mouse_condition[0],appear)
                witch1.change_frame(dt)
                witch1.draw(screen)
                appear=False
                for i,mana in enumerate(mana_list):
                    if mana.y>mana.center[1]:
                        mana.draw(screen)
                for ef in effect_list:
                    ef.draw(screen)
                    if ef.change_frame(dt):
                        effect_list=[e for e in effect_list if not e==ef]
                for ef in monster_effect_l:
                    ef.draw(screen)
                    if ef.change_frame(dt):
                        monster_effect_l=[e for e in monster_effect_l if not e==ef]
                for ef in spirit_effect_l:
                    ef.draw(screen)
                    if ef.change_frame(dt):
                        spirit_effect_l=[e for e in spirit_effect_l if not e==ef]
                progress=min(wave_time/100,1)
                pygame.draw.rect(screen,(0,0,0),(0,632,screen_width,8))
                pygame.draw.rect(screen,(255,0,0),(0,632,screen_width*progress,8))
                click=False
                if first:
                    if_story=True
                first=False

            else:
                if wave<=10:
                    screen.blit(background_im[0],(0,0))
                else:
                    screen.blit(background_im[1],(0,0))
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
                for i,mana in enumerate(mana_list):
                    if mana.y<=mana.center[1]:
                        mana.draw(screen)
                witch1.draw(screen)
                appear=False
                for i,mana in enumerate(mana_list):
                    if mana.y>mana.center[1]:
                        mana.draw(screen)
                if tuto:
                    if not change:
                        subt_bg_frame_index += dt * 0.035
                        tuto_str_index += dt * 0.01
                    if tuto_index >= len(tuto_str_l) - 1:
                        tuto_index = len(tuto_str_l) - 1
                        tuto_str_index = len(tuto_str_l[tuto_index])
                        if button_:
                            change = True
                            button_ = False
                            subt_bg_frame_index = 0
                            scene_change.i = 1

                    if len(tuto_str_l[tuto_index]) <= int(tuto_str_index):
                        tuto_str_index = len(tuto_str_l[tuto_index])
                        if button_ and not change:
                            button_ = False
                            tuto_index += 1
                            tuto_str_index = 0

                    fade_surface.set_alpha(175)
                    screen.blit(fade_surface, (0, 0))

                    frame_idx = int(subt_bg_frame_index)
                    if tuto_index==0:
                        for i,mana in enumerate(mana_list):
                            mana.update(i,len(mana_list),orbit_angle)
                            mana.draw(screen)
                    elif tuto_index==1:
                        store_btn_list[0].im=store_btn_list[0].frame[10]
                        store_btn_list[0].draw(screen)
                    elif tuto_index==2:
                        for button in store_btn_list:
                            button.im=button.frame[10]
                            button.draw(screen)
                    elif tuto_index==3:
                        pygame.draw.rect(screen,(255,0,0),(0,632,screen_width-420,8))

                    if frame_idx >= len(subt_bg1):
                        frame_idx = len(subt_bg1) - 1

                    screen.blit(
                        subt_bg1[frame_idx],
                        (
                            screen_width // 2 - subt_bg1[frame_idx].get_width() // 2,
                            screen_height // 2 - subt_bg1[frame_idx].get_height() // 2 - 15,
                        ),
                    )

                    if frame_idx == 4 and tuto_index < len(tuto_str_l):
                        draw_text(
                            screen,
                            screen_width // 2,
                            screen_height // 2,
                            tuto_str_l[tuto_index],
                            witch_font,
                            int(tuto_str_index),
                            (255, 255, 255),
                        )

                else:
                    if not click:
                        alpha=175
                    fade_surface.set_alpha(alpha)
                    screen.blit(fade_surface,(0,0))
                    if story_l[wave-1][1]==witch_font:
                        screen.blit(story_witch,(-100,100))
                    elif story_l[wave-1][1]==boss_font:
                        screen.blit(story_boss,(screen_width-520,200))
                    screen.blit(subt_bg[int(subt_bg_frame_index)],(0,screen_height//2-225))
                    if int(subt_bg_frame_index)==4:
                        subt_bg_frame_index=4
                        if story_l[wave-1]:
                            draw_text(screen,screen_width//2,screen_height-100,story_l[wave-1][0],story_l[wave-1][1],text_index)
                            if int(text_index)==len(story_l[wave-1][0]):
                                text_index=len(story_l[wave-1][0])
                                if mouse_condition[0]:
                                    scene_change.i=1
                            else:    
                                text_index+=dt*0.01
                    else:
                        subt_bg_frame_index+=dt*0.035

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
        elif scene=="gameover":
            screen.fill((0,0,0))
            screen.blit(gameover[int(funny_index)],(screen_width//2-gameover[int(funny_index)].get_width()//2,screen_height//2-funny[int(funny_index)].get_height()//2))
            funny_index+=dt*0.02
            if int(funny_index)==2:
                funny_index=0
            if button_:
                button_=False
                scene_change.i=1
                change_scene="start"
                reset=True

        else:
            screen.fill((0,0,0))
            screen.blit(funny[int(funny_index)],(screen_width//2-funny[int(funny_index)].get_width()//2,screen_height//2-funny[int(funny_index)].get_height()//2))
            funny_index+=dt*0.02
            if int(funny_index)==2:
                funny_index=0
            if button_:
                button_=False
                scene_change.i=1
                change_scene="start"
                reset=True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.MOUSEBUTTONDOWN and scene=="start":
                change_scene="story"
                scene_change.i=1
            if event.type == pygame.MOUSEBUTTONUP:
                click=True 
                if scene=="story" or tuto:
                    button_=True
                    if mouse_pos_y>=screen_height-192 and mouse_pos_x<=192 and story_scene==0:
                        change_scene="game"
                        scene_change.i=1
                        cut_l = []
                        story_index = 0
                        story_scene += 1
                        button_=False
                elif scene=="ending" or scene=="gameover":
                    button_=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if full_charge:
                        for i in monster_list:
                            for monster in i:
                                monster.health=0
                        spirit_effect_l.append(attack_effect(screen_width//2,screen_height//2,power,1280,1000))
                        mana_list=[]
        if scene_change.fade_inout(dt):
            scene=change_scene
            if scene=="story":
                story_index=0
            elif scene=="game" and if_story:
                if tuto:
                    tuto=False
                else:
                    story_l[wave-1]=False
                    if_story=False

        scene_change.draw(screen)
        pygame.display.flip()

    pygame.quit()
