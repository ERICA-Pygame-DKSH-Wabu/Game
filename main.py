import json
import pygame
from pos import *
from cut import *
from witch import * 
from util import *
from button import *
from spirit import *
from effect import *
from monster import *
from background import *
from mana import *
class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 640
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("witch")
        with open("story_wave.json", "r", encoding="utf-8") as f:
            self.wave_data = json.load(f)
        
        self.spirit_type = ("water","fire","grass","light","stone","dark")
        self.price = (2,4,4,5,3,5)
        self.spirit_classes = {
            "water": Water_Spirit,
            "fire": Fire_Spirit,
            "grass": Grass_Spirit,
            "light": Light_Spirit,
            "stone": Stone_Spirit,
            "dark": Dark_Spirit
        }
        self.monster_classes = {
            "dark": Dark_Monster,
            "light": Light_Monster,
            "water": Water_Monster,
            "fire": Fire_Monster,
            "grass": Grass_Monster,
            "stone": Stone_Monster,
        }
        self.fps = pygame.time.Clock()
        self.playing = True

        self.witch_frame_index = 0
        self.witch_frame = get_frame("asset/ui/witch",640,640,230)
        self.witchframe = {
            "attack": get_frame("asset/witch_frame/attack", 192*0.7, 256*0.7, 255),
            "idle": get_frame("asset/witch_frame/idle", 192*0.7, 256*0.7, 255),
            "spin": get_frame("asset/witch_frame/spin", 192*0.7, 256*0.7, 255)
}
        self.witch1 = witch([pygame.Rect(210+25*i, self.screen_height - (i + 1) * 60 - 40, 32,32) for i in range(4)],self.witchframe)
        self.subt_bg = get_frame("asset/ui/subtitle_bg",1280,840,255)
        self.subt_bg1 = get_frame("asset/ui/subtitle_bg",720,840,255)
        self.boss_font = get_font("asset/witch.ttf",36)
        self.monster_font = get_font("asset/monster.ttf",36)
        self.witch_font = get_font("asset/witch.ttf",36)

        self.spirit_attack_dict = {
            "grass": get_frame("asset/spirit_attack_effect/grass",256,192,100),
            "light": get_frame("asset/spirit_attack_effect/light",96,96,230),
            "water": get_frame("asset/spirit_attack_effect/water",160,160,140),
            "stone": get_frame("asset/spirit_attack_effect/stone",64,64,180,False),
            "fire":  get_frame("asset/spirit_attack_effect/fire",128,96,180),
            "dark":  get_frame("asset/spirit_attack_effect/dark",128,128,180),
        }
        self.monster_attack_dict = {
            "grass": get_frame("asset/monster_attack_effect/grass",128,128,220),
            "light": get_frame("asset/monster_attack_effect/light",128,128,256),
            "water": get_frame("asset/monster_attack_effect/water",128,128,220),
            "stone": get_frame("asset/monster_attack_effect/stone",128,128,180,False),
            "fire":  get_frame("asset/monster_attack_effect/fire",96,96,200,False),
            "dark":  get_frame("asset/monster_attack_effect/dark",128,128,200),
        }
        self.smoke_effect_l = get_frame("asset/ui/appear_effect",120,120,150)

        self.gameover = get_frame("asset/gameover",700,500,256)
        self.gameover = [invert_surface_color(i) for i in self.gameover]


        self.manaframe1 = util.get_frame("asset/mana_frame", 20, 40, 220)
        self.manaframe2=[]
        for i in self.manaframe1:
            self.manaframe2.append(util.invert_surface_color(i))
        self.center = (208, self.screen_height//2+20)
        self.mana_list = [Mana(self.center,self.manaframe1,self.manaframe2) for i in range(2)]
        self.orbit_angle = 0.7 % 360
        self.start_im = set_im(get_im("asset/ui/start.png"),256,256,256,True)
        self.start_background_im = set_im(get_im("asset/ui/start_background.png"),1280,640,256,True)

        self.scene = "start"
        self.fade_surface = pygame.Surface((self.screen_width, self.screen_height))
        self.fade_surface.fill((0,0,0))
        self.fade_in = True
        self.fade_alpha = 255
        self.skip = set_im(get_im("asset/ui/skip.png"),192,192,200,True)
        self.start_alpha = 0
        self.start_dir = 1
        self.start_pulse = False
        self.witch_fade_in = False

        self.spirit_list = [[False for i in range(6)] for j in range(4)]
        self.monster_list = [[] for i in range(4)]
        self.effect_list = []
        self.spirit_pos_list = []
        self.monster_pos_list = []
        self.store_btn_list = []
        self.located_rect = [[False for i in range(6)] for j in range(4)]
        self.monster_effect_l = []
        self.spirit_effect_l = []

        self.bg_switched = False
        self.appear = False
        self.if_story = False
        self.subt_bg_frame_index = 0
        self.story_l = [["대체 어디로간거니..?",self.witch_font],False,False,False,[".....",self.monster_font],False,False,False,["마녀... ",self.boss_font],False,["포...기..ㅎ..ㅐ.. ",self.monster_font],False,False,False,["하아...정말 성가시다니까 ",self.witch_font],["포기하면 편할텐데말이지...",self.witch_font],False,["ㅅ..싫..어",self.monster_font],False,["그만해..!",self.boss_font],["피곤하네...이짓도",self.witch_font],[".....",self.boss_font]]
        self.text_index = 0
        self.waiting_game = False
        self.story_witch = set_im(get_im("asset/ui/story_witch.png"),640,640,240,False)
        self.story_boss = set_im(get_im("asset/ui/story_boss.png"),550,550,240,True)
        self.change_scene = "witch"
        self.effect_frame = get_frame("asset/effect",50,50,235)
        self.full_charge = False
        self.monsters_spawned = 0
        self.monster_count = 0
        self.all_monsters_arrived = False

        self.funny = get_frame("asset/funny",1280,640,256)
        self.funny_index = 0
        for i in range(6):
            for spirit in range(4):
                x = i * 80 + spirit * 25 + 260
                y = self.screen_height - (spirit + 1) * 60 - 50
                rect = pygame.Rect(x, y, 50, 50)
                self.spirit_pos_list.append(Pos(rect,(i,3-spirit)))
        for i in range(4):
            x = self.screen_width + i*25 + 100
            y = self.screen_height - (i+1)*60 - 40
            rect = pygame.Rect(x,y,50,50)
            self.monster_pos_list.append(Pos(rect,(i,3-spirit)))
        self.monster_pos_list.reverse()
        for monster in range(6):
            self.store_btn_list.append(Store_Button(self.screen_width-100*monster-100,50,
                                                    pygame.Rect(self.screen_width-100*monster-100,60,70,80),
                                                    self.spirit_type[monster]))
        self.background_im=[set_im(get_im(f"asset/ui/background_{i}.jpg"),1280,640,256,True) for i in [1,2]]
        self.first = True
        self.power = remove_white(get_frame("asset/power",1280,720,256))
        self.tuto_index=0
        self.tuto_str_index=0
        self.tuto=True
        self.damaged=False
        self.button_=False
        self.story_index=0
        self.story_scene=0
        self.im_size=get_im("asset/story/story1/1.png").get_size()
        self.scene_l=[get_frame("asset/story/story1",1280,640,256),
                      get_frame("asset/story/story2",1280,640,256)]
        self.cut_l=[]
        self.reset=False
        self.scene_change=Cut(0,0,0,self.fade_surface)
        self.wave=1
        self.wave_time=0
        self.wave_speed=1
        self.change=False
        self.tuto_str_l=["마나는 가장 기본적인 자원입니다.","물의 정령을 소환해 마나를 충전하십시오.","마나를 사용해 정령을 소환할 수 있습니다.","웨이브가 시작될때 마다 몬스터가 몰려옵니다.","정령들로 몬스터를 물리치십시오."]

        self.monster_frame_dict={}
        l=["water","light","stone","fire","dark","grass"]
        monster_size=[120,120,120,96,144,144]
        for i in l:
            self.monster_frame_dict[i]={
                    "attack": get_frame(f"asset/monster/{i}/attack",monster_size[l.index(i)],monster_size[l.index(i)],255),
                    "idle": get_frame(f"asset/monster/{i}/idle",monster_size[l.index(i)],monster_size[l.index(i)],255),
                    "spin": get_frame(f"asset/monster/{i}/spin",monster_size[l.index(i)],monster_size[l.index(i)],255),
                }
        self.spirit_frame_dict={}
        l=["water","light","stone","fire","dark","grass"]
        spirit_size=[96,120,120,150,120,120]
        for i in l:
            self.spirit_frame_dict[i]={
                    "attack": get_frame(f"asset/spirit/{i}/attack",spirit_size[l.index(i)],spirit_size[l.index(i)],255),
                    "idle": get_frame(f"asset/spirit/{i}/idle",spirit_size[l.index(i)],spirit_size[l.index(i)],255),
                    "spin": get_frame(f"asset/spirit/{i}/spin",spirit_size[l.index(i)],spirit_size[l.index(i)],255),
                }
        for i in self.spirit_frame_dict["fire"]["idle"]:
            self.spirit_frame_dict["fire"]["idle"][self.spirit_frame_dict["fire"]["idle"].index(i)]=set_im(i,138,138,255,True)
    def reset_g(self):
        self.story_l = [["대체 어디로간거니..?",self.witch_font],False,False,False,[".....",self.monster_font],False,False,False,["마녀... ",self.boss_font],False,["포...기..ㅎ..ㅐ.. ",self.monster_font],False,False,False,["하아...정말 성가시다니까 ",self.witch_font],["포기하면 편할텐데말이지...",self.witch_font],False,["ㅅ..싫..어",self.monster_font],False,["그만해..!",self.boss_font],["피곤하네...이짓도",self.witch_font],[".....",self.boss_font]]
        self.wave = 1
        self.wave_time = 0
        self.wave_speed = 1
        self.if_story = False
        self.text_index = 0
        self.subt_bg_frame_index = 0
        self.spirit_list = [[False for _ in range(6)] for _ in range(4)]
        self.monster_list = [[] for _ in range(4)]
        self.effect_list = []
        self.spirit_effect_l = []
        self.monster_effect_l = []
        self.located_rect = [[False for _ in range(6)] for _ in range(4)]
        self.mana_list = [Mana(self.center,self.manaframe1,self.manaframe2) for _ in range(2)]
        self.store_btn_list.clear()
        for i in range(6):
            self.store_btn_list.append(Store_Button(self.screen_width - 100 * i - 100, 50,
                                                    pygame.Rect(self.screen_width - 100 * i - 100, 60, 70, 80),
                                                    self.spirit_type[i]))
        self.witch1 = witch([pygame.Rect(210 + 25 * i, self.screen_height - (i + 1) * 60 - 40, 32, 32) for i in range(4)],self.witchframe)
        self.button_ = False
        self.click = False
        self.appear = False
        self.full_charge = False
        self.fade_alpha = 255
        self.fade_in = True
        self.witch_frame_index = 0
        self.first = True
        self.cut_l = []
        self.story_index = 0
        self.story_scene = 0
        self.change = False
        self.funny_index = 0
        self.reset = False

    def check_events(self, mouse_pos, mouse_buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

            elif event.type == pygame.MOUSEBUTTONDOWN and self.scene == "start":
                self.change_scene = "story"
                self.scene_change.i = 1

            elif event.type == pygame.MOUSEBUTTONUP:
                self.click = True
                if self.scene == "story" or self.tuto or self.if_story:
                    self.button_ = True
                    if self.scene == "story" and mouse_pos[1] >= self.screen_height - 192 and mouse_pos[0] <= 192 and self.story_scene == 0:
                        self.change_scene = "game"
                        self.scene_change.i = 1
                        self.cut_l = []
                        self.story_index = 0
                        self.story_scene += 1
                        self.button_ = False
                elif self.scene in ("ending", "gameover"):
                    self.button_ = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.full_charge:
                    for line in self.monster_list:
                        for monster in line:
                            monster.health = 0
                    self.spirit_effect_l.append(attack_effect(self.screen_width // 2, self.screen_height // 2, self.power, 1280, 1000))
                    self.mana_list = []
                    self.full_charge=False


    def start_scene(self, dt):
        self.screen.blit(self.start_background_im, (0, 0))
        start_draw = self.start_im.copy()
        start_draw.set_alpha(int(self.start_alpha) * 0.7)
        self.screen.blit(start_draw, (self.screen_width // 2 - self.start_im.get_width() // 2,
                                      self.screen_height // 2 + 64))
        step = 0.15 * round(dt, 3) if self.start_pulse else 0.08 * round(dt, 3)
        if self.fade_in:
            self.fade_alpha -= step
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_in = False
                self.witch_fade_in = True
            self.fade_surface.set_alpha(int(self.fade_alpha))
            self.screen.blit(self.fade_surface, (0, 0))
        elif self.witch_fade_in:
            self.witch_frame_index += step * 0.15
            if self.witch_frame_index >= len(self.witch_frame) - 1:
                self.witch_frame_index = len(self.witch_frame) - 1
                self.witch_fade_in = False
                self.start_pulse = True
        elif self.start_pulse:
            self.start_alpha += step * self.start_dir
            if self.start_alpha >= 255:
                self.start_alpha = 255
                self.start_dir = -1
            elif self.start_alpha <= 0:
                self.start_alpha = 0
                self.start_dir = 1
        if self.witch_frame_index:
            self.screen.blit(self.witch_frame[int(self.witch_frame_index)],
                             (-self.witch_frame[int(self.witch_frame_index)].get_width() // 2 +
                              self.screen_width // 2, -20))

    def story_scene(self, dt):
        self.screen.fill((0, 0, 0))
        for cut in self.cut_l:
            cut.draw(self.screen)
        if not self.scene_change.i == 1:
            self.screen.blit(self.skip, (-32, self.screen_height - 160))
            if not self.cut_l and self.story_scene < len(self.scene_l):
                self.story_index = 0
                self.cut_l.append(Cut(0, 0, 0, self.scene_l[self.story_scene][self.story_index]))
                self.story_index += 1
            elif self.cut_l and self.cut_l[-1].fade_in(dt) and self.button_:
                if self.story_index < len(self.scene_l[self.story_scene]):
                    self.button_ = False
                    self.cut_l.append(Cut(0, 0, 0, self.scene_l[self.story_scene][self.story_index]))
                    self.story_index += 1
                elif self.story_scene == 0:
                    self.cut_l = []
                    self.story_index = 0
                    self.story_scene += 1
                    self.scene_change.i = 1
                    self.change_scene = "game"
                    self.button_ = False
                else:
                    self.scene = "ending"
                    self.button_ = False
    def spirit_attack(self,spirit):
        attack = attack_effect(spirit.target, spirit.hitbox.centery, self.spirit_attack_dict[spirit.name], 32, spirit.damage)
        for j in self.monster_list:
            for m in j:
                if m.hitbox.colliderect(attack.hitbox):
                    m.health -= attack.damage
        self.spirit_effect_l.append(attack)

    def monster_attack(self,monster):
        if monster.condition == "attack" and int(monster.frame_index) == monster.attack_time and monster.if_attack:
            attack = attack_effect(monster.target, monster.hitbox.top, self.monster_attack_dict[monster.name], 16, monster.damage)
            monster.if_attack = False
            for rect in self.witch1.hitbox:
                if rect.colliderect(attack.hitbox):
                    self.witch1.health -= attack.damage
                    self.damaged = True
            for j in self.spirit_list:
                for s in j:
                    if s and s.hitbox.colliderect(attack.hitbox):
                        s.health -= attack.damage
            self.monster_effect_l.append(attack)
    def water_mana(self):
            if not self.full_charge:
                for k in range(12):
                    if not self.mana_list[k].charge:
                        self.mana_list[k].charge = True
                        break
            self.full_charge = all(m.charge for m in self.mana_list)
    def grass_attack(self,spirit,line):
        if line[line.index(spirit)]:
            if line.index(spirit) + 1 < 6 and line[line.index(spirit) + 1]:
                line[line.index(spirit) + 1].health += 30
                self.effect_list.append(effect(spirit.hitbox.centerx + 80, spirit.hitbox.centery - 20, self.spirit_attack_dict["grass"]))
                if line[line.index(spirit) + 1].health > line[line.index(spirit) + 1].max_health:
                    line[line.index(spirit) + 1].health = line[line.index(spirit) + 1].max_health
            if line.index(spirit) - 1 > 0 and line[line.index(spirit) - 1]:
                line[line.index(spirit) - 1].health += 30
                self.effect_list.append(effect(spirit.hitbox.centerx - 80, spirit.hitbox.centery - 20, self.spirit_attack_dict["grass"]))
                if line[line.index(spirit) - 1].health > line[line.index(spirit) - 1].max_health:
                    line[line.index(spirit) - 1].health = line[line.index(spirit) - 1].max_health
            spirit.health += 30
            if spirit.health > spirit.max_health:
                spirit.health = spirit.max_health
                self.effect_list.append(effect(spirit.hitbox.centerx, spirit.hitbox.centery - 20, self.spirit_attack_dict["grass"]))
    def game_scene(self, dt, mouse_pos, mouse_condition):
        if self.witch1.health <= 0:
            self.scene_change.i = 1
            self.change_scene = "gameover"

        self.orbit_angle = (self.orbit_angle + 0.7) % 360

        if self.wave > len(self.story_l):
            self.scene_change.i = 1
            self.change_scene = "story"

        elif not self.if_story and self.wave <= len(self.story_l):
            self.text_index = 0
            self.subt_bg_frame_index = 0

            if self.story_l[self.wave - 1]:
                self.if_story = True

            if self.wave <= 10:
                self.screen.blit(self.background_im[0], (0, 0))
            else:
                if self.if_story and self.wave==11:
                    self.screen.blit(self.background_im[0], (0, 0))
                else:
                    self.screen.blit(self.background_im[1], (0, 0))
            if not self.if_story:
                self.button_ =False
            if self.first:
                self.fade_surface.set_alpha(175)
                self.screen.blit(self.fade_surface, (0, 0))

            if self.wave >= 19:
                self.wave_speed = 1000

            self.wave_time += dt * self.wave_speed * 0.005 *3
            if self.wave_time > 100:
                self.spawn_wave(self.wave)
                self.wave += 1
                self.wave_time = 0

            for line in self.spirit_list:
                for spirit in line:
                    if spirit:
                        spirit.set_target([m.hitbox for m in self.monster_list[spirit.line]])
                        spirit.set_condition()
                        spirit.change_frame(dt)
                        spirit.draw(self.screen)

                        if spirit.condition == "attack" and int(spirit.frame_index) == spirit.attack_time and spirit.if_attack:
                            if spirit.name == "grass":
                                self.grass_attack(spirit,line)
                            elif spirit.name == "water":
                                if len(self.mana_list) < 12:
                                    self.mana_list.append(Mana(self.center,self.manaframe1,self.manaframe2))
                                else:
                                    self.water_mana()
                                self.effect_list.append(effect(spirit.hitbox.centerx, spirit.hitbox.centery - 20, self.spirit_attack_dict["water"]))
                            else:
                                self.spirit_attack(spirit)
                            spirit.if_attack = False
                        if spirit.health <= 0:
                            self.located_rect[spirit.line][line.index(spirit)] = False
                        if spirit.if_dead(dt):
                            self.effect_list.append(effect(spirit.hitbox.centerx, spirit.hitbox.centery, self.smoke_effect_l))
                            line[line.index(spirit)] = False

            for line_monsters in self.monster_list:
                for monster in line_monsters:
                    monster.set_target(self.located_rect[monster.line])
                    monster.set_condition()
                    monster.change_frame(dt)
                    monster.set_hitbox()

                    self.monster_attack(monster)
                    monster.draw(self.screen)
                    if monster.if_dead(dt):
                        self.effect_list.append(effect(monster.hitbox.centerx, monster.hitbox.centery, self.smoke_effect_l))
                        self.monster_list[monster.line] = [i for i in self.monster_list[monster.line] if not monster == i]
                    else:
                        monster.move(dt)

            dragging_btn = None
            for btn in self.store_btn_list:
                if btn.dragging:
                    dragging_btn = btn
                    break

            for button in self.store_btn_list:
                button.set_hitbox()
                if dragging_btn is None:
                    button.drag(mouse_pos, mouse_condition, self.spirit_pos_list)
                elif button is dragging_btn:
                    data = button.drag(mouse_pos, mouse_condition, self.spirit_pos_list)
                    if data:
                        if self.located_rect[data[2][1]][data[2][0]]:
                            break
                        else:
                            self.appear = True
                            self.effect_list.append(effect(self.center[0] + 55, self.center[1] + 40, self.effect_frame))

                            cost = self.price[self.spirit_type.index(data[1])]
                            if len(self.mana_list) >= cost:
                                cls = self.spirit_classes[data[1]]
                                self.spirit_list[data[2][1]][data[2][0]] = cls(data[0], data[2][1],self.spirit_frame_dict)
                                self.mana_list = self.mana_list[:-cost]

                            if self.spirit_list[data[2][1]][data[2][0]]:
                                self.spirit_list[data[2][1]][data[2][0]].set_frame()
                                self.located_rect[data[2][1]][data[2][0]] = data[0]
                                self.effect_list.append(effect(data[0].centerx, data[0].centery, self.smoke_effect_l))

                if self.price[self.spirit_type.index(button.s_type)] <= len(self.mana_list):
                    button.change_frame(dt)
                else:
                    button.im = button.frame[0]
                button.draw(self.screen)

            for i, mana in enumerate(self.mana_list):
                mana.update(i, len(self.mana_list), self.orbit_angle)
                if mana.y <= mana.center[1]:
                    mana.draw(self.screen)

            self.witch1.set_condition(mouse_condition[0], self.appear)
            self.witch1.change_frame(dt)
            self.witch1.draw(self.screen)
            self.appear = False

            for i, mana in enumerate(self.mana_list):
                if mana.y > mana.center[1]:
                    mana.draw(self.screen)

            for ef in list(self.effect_list):
                ef.draw(self.screen)
                if ef.change_frame(dt):
                    self.effect_list = [e for e in self.effect_list if not e == ef]
            for ef in list(self.monster_effect_l):
                ef.draw(self.screen)
                if ef.change_frame(dt):
                    self.monster_effect_l = [e for e in self.monster_effect_l if not e == ef]
            for ef in list(self.spirit_effect_l):
                ef.draw(self.screen)
                if ef.change_frame(dt):
                    self.spirit_effect_l = [e for e in self.spirit_effect_l if not e == ef]

            progress = min(self.wave_time / 100, 1)
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 632, self.screen_width, 8))
            pygame.draw.rect(self.screen, (255, 0, 0), (0, 632, self.screen_width * progress, 8))
            self.click = False
            if self.first:
                self.if_story = True
            self.first = False

        else:
            if self.wave <= 10:
                self.screen.blit(self.background_im[0], (0, 0))
            else:
                if self.wave==11 and self.if_story:
                    self.screen.blit(self.background_im[0], (0, 0))
                else:
                    self.screen.blit(self.background_im[1], (0, 0))

            for line in self.spirit_list:
                for spirit in line:
                    if spirit:
                        spirit.draw(self.screen)
            for line_monsters in self.monster_list:
                for monster in line_monsters:
                    monster.draw(self.screen)
            for effects in self.effect_list:
                effects.draw(self.screen)
            for effects in self.monster_effect_l:
                effects.draw(self.screen)
            for effects in self.spirit_effect_l:
                effects.draw(self.screen)
            for button in self.store_btn_list:
                button.draw(self.screen)
            for i, mana in enumerate(self.mana_list):
                if mana.y <= mana.center[1]:
                    mana.draw(self.screen)
            self.witch1.draw(self.screen)
            self.appear = False
            for i, mana in enumerate(self.mana_list):
                if mana.y > mana.center[1]:
                    mana.draw(self.screen)

            if self.tuto:
                if not self.change:
                    self.subt_bg_frame_index += dt * 0.035
                    self.tuto_str_index += dt * 0.01
                if self.tuto_index >= len(self.tuto_str_l) - 1:
                    self.tuto_index = len(self.tuto_str_l) - 1
                    self.tuto_str_index = len(self.tuto_str_l[self.tuto_index])
                    if self.button_:
                        self.change = True
                        self.button_ = False
                        self.subt_bg_frame_index = 0
                        self.scene_change.i = 1

                if len(self.tuto_str_l[self.tuto_index]) <= int(self.tuto_str_index):
                    self.tuto_str_index = len(self.tuto_str_l[self.tuto_index])
                    if self.button_ and not self.change:
                        self.button_ = False
                        self.tuto_index += 1
                        self.tuto_str_index = 0

                self.fade_surface.set_alpha(175)
                self.screen.blit(self.fade_surface, (0, 0))

                frame_idx = int(self.subt_bg_frame_index)
                if self.tuto_index == 0:
                    for i, mana in enumerate(self.mana_list):
                        mana.update(i, len(self.mana_list), self.orbit_angle)
                        mana.draw(self.screen)
                elif self.tuto_index == 1:
                    self.store_btn_list[0].im = self.store_btn_list[0].frame[10]
                    self.store_btn_list[0].draw(self.screen)
                elif self.tuto_index == 2:
                    for button in self.store_btn_list:
                        button.im = button.frame[10]
                        button.draw(self.screen)
                elif self.tuto_index == 3:
                    pygame.draw.rect(self.screen, (255, 0, 0), (0, 632, self.screen_width - 420, 8))

                if frame_idx >= len(self.subt_bg1):
                    frame_idx = len(self.subt_bg1) - 1

                self.screen.blit(
                    self.subt_bg1[frame_idx],
                    (
                        self.screen_width // 2 - self.subt_bg1[frame_idx].get_width() // 2,
                        self.screen_height // 2 - self.subt_bg1[frame_idx].get_height() // 2 - 15,
                    ),
                )

                if frame_idx == 4 and self.tuto_index < len(self.tuto_str_l):
                    draw_text(
                        self.screen,
                        self.screen_width // 2,
                        self.screen_height // 2,
                        self.tuto_str_l[self.tuto_index],
                        self.witch_font,
                        int(self.tuto_str_index),
                        (255, 255, 255),
                    )
            else:
                alpha = 175
                self.fade_surface.set_alpha(alpha)
                self.screen.blit(self.fade_surface, (0, 0))
                if self.story_l[self.wave - 1][1] == self.witch_font:
                    self.screen.blit(self.story_witch, (-100, 100))
                elif self.story_l[self.wave - 1][1] == self.boss_font:
                    self.screen.blit(self.story_boss, (self.screen_width - 520, 200))
                self.screen.blit(self.subt_bg[int(self.subt_bg_frame_index)], (0, self.screen_height // 2 - 225))
                if int(self.subt_bg_frame_index) == 4:
                    self.subt_bg_frame_index = 4
                    if self.story_l[self.wave - 1]:
                        draw_text(self.screen, self.screen_width // 2, self.screen_height - 100, self.story_l[self.wave - 1][0], self.story_l[self.wave - 1][1], self.text_index)
                        if int(self.text_index) == len(self.story_l[self.wave - 1][0]):
                            self.text_index = len(self.story_l[self.wave - 1][0])
                            if mouse_condition[0]:
                                self.scene_change.i = 1
                        else:
                            self.text_index += dt * 0.01
                else:
                    self.subt_bg_frame_index += dt * 0.035

    def gameover_scene(self, dt):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.gameover[int(self.funny_index)],
                         (self.screen_width // 2 - self.gameover[int(self.funny_index)].get_width() // 2,
                          self.screen_height // 2 - self.funny[int(self.funny_index)].get_height() // 2))
        self.funny_index += dt * 0.02
        if int(self.funny_index) == 2:
            self.funny_index = 0
        if self.button_:
            self.button_ = False
            self.scene_change.i = 1
            self.change_scene = "start"
            self.reset = True

    def ending_scene(self, dt):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.funny[int(self.funny_index)],
                         (self.screen_width // 2 - self.funny[int(self.funny_index)].get_width() // 2,
                          self.screen_height // 2 - self.funny[int(self.funny_index)].get_height() // 2))
        self.funny_index += dt * 0.02
        if int(self.funny_index) == 2:
            self.funny_index = 0
        if self.button_:
            self.button_ = False
            self.scene_change.i = 1
            self.change_scene = "start"
            self.reset = True

 
    def spawn_wave(self, wave_num):
        if not (1 <= wave_num <= len(self.wave_data)):
            return

        wave_info = self.wave_data[wave_num - 1]

        for row in range(1, 5):
            key = f"index_{row}"
            row_list = wave_info.get(key, [])
            if not isinstance(row_list, list) or not row_list:
                continue

            row_idx = row - 1
            base = getattr(self.monster_pos_list[row_idx], "rect", self.monster_pos_list[row_idx])
            base_rect = base.rect if hasattr(base, "rect") else base

            for col_idx, m_type in enumerate(row_list):
                m_key = str(m_type)
                cls = self.monster_classes.get(m_key)
                if not cls:
                    continue

                spawn_rect = pygame.Rect(
                    base_rect.left - 100 + 55 * col_idx,
                    base_rect.top,
                    base_rect.width,
                    base_rect.height
                )

                mon = cls(spawn_rect, row_idx, m_key,self.monster_frame_dict)
                if hasattr(mon, "set_frame"):
                    mon.set_frame()
                if hasattr(mon, "set_target_rect"):
                    mon.set_target_rect(col_idx)

                self.monster_list[row_idx].append(mon)

    def run_game(self):
        while self.playing:
            dt = self.fps.tick(60)
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            if self.reset:
                self.reset_g()
            self.check_events(mouse_pos, mouse_buttons)
            if self.scene == "start":
                self.start_scene(dt)
            elif self.scene == "story":
                self.story_scene(dt)
            elif self.scene == "game":
                self.game_scene(dt, mouse_pos, mouse_buttons)
            elif self.scene == "gameover":
                self.gameover_scene(dt)
            elif self.scene == "ending":
                self.ending_scene(dt)
            if self.scene_change.fade_inout(dt):
                self.scene = self.change_scene
                if self.scene == "story":
                    self.story_index = 0
                elif self.scene == "game" and self.if_story:
                    if self.tuto:
                        self.tuto = False
                    else:
                        self.story_l[self.wave-1] = False
                        self.if_story = False
            self.scene_change.draw(self.screen)
            pygame.display.flip()