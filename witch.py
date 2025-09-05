from util import *

frame = {
    "attack": get_frame("asset/witch_frame/attack", 192*0.7, 256*0.7, 255),
    "idle": get_frame("asset/witch_frame/idle", 192*0.7, 256*0.7, 255),
    "spin": get_frame("asset/witch_frame/spin", 192*0.7, 256*0.7, 255)
}

class witch:
    def __init__(self, hitbox):
        self.hitbox = hitbox
        self.max_health = 1000
        self.health = 1000
        self.frame = frame
        self.fade = 255
        self.condition = "idle"
        self.img = self.frame["idle"][0]
        self.frame_index = 0
        self.button_pressed = False   # 마우스 눌림 상태 저장
        self.reversing = False        # spin 역재생 여부
        self.appear = True            # main에서 인자로 들어오는 값

    def setting(self):
        self.health = 500
        self.fade = 255

    def draw(self, screen):
        screen.blit(self.img, (150, 320))
        if self.health > 0:
            bar_width = 70
            bar_height = 5
            full_rect = pygame.Rect(0, 0, bar_width, bar_height)
            full_rect.midbottom = (218,640 // 2+20+160)
            ratio = max(0, min(self.health / self.max_health, 1.0))
            curr_rect = full_rect.copy()
            curr_rect.width = int(bar_width * ratio)
            pygame.draw.rect(screen, (255, 0, 0), full_rect)
            if curr_rect.width > 0:
                pygame.draw.rect(screen, (0, 255, 0), curr_rect)

    def set_condition(self, if_button_pressed, appear):
        self.appear = appear  # 외부 인자 반영

        # 마우스 누르기 시작 → spin 정방향
        if if_button_pressed and not self.button_pressed:
            self.condition = "spin"
            self.frame_index = 0
            self.reversing = False

        # 마우스 뗐을 때
        elif not if_button_pressed and self.button_pressed:
            if self.condition == "spin":
                if self.appear:  # attack으로 전환
                    self.condition = "attack"
                    self.frame_index = 0
                else:  # spin 역재생 시작
                    self.reversing = True
                    self.condition = "spin"
                    self.frame_index = len(self.frame["spin"]) - 1

        self.button_pressed = if_button_pressed

    def change_frame(self, dt):
        if self.fade <= 256:
            self.fade += 0.01 * dt
        else:
            self.fade = 256

        try:
            frame_speed = 0.016 * dt
            self.img = self.frame[self.condition][int(self.frame_index)]
            self.img.set_alpha(int(self.fade))

            # 상태별 처리
            if self.condition == "spin":
                if self.reversing:  # spin 역재생
                    self.frame_index -= frame_speed
                    if self.frame_index <= 0:
                        self.condition = "idle"
                        self.frame_index = 0
                        self.reversing = False
                else:  # 정방향 재생
                    if self.frame_index + frame_speed >= len(self.frame["spin"]):
                        self.frame_index = len(self.frame["spin"]) - 1  # 끝 프레임 유지
                    else:
                        self.frame_index += frame_speed

            elif self.condition == "attack":
                if self.frame_index + frame_speed >= len(self.frame["attack"]):
                    self.condition = "idle"
                    self.frame_index = 0
                else:
                    self.frame_index += frame_speed

            elif self.condition == "idle":
                self.frame_index = (self.frame_index + frame_speed) % len(self.frame["idle"])

        except IndexError:
            self.frame_index = 0
