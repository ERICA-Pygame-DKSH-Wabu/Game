import pygame
import math

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("타원 회전 구체 - 자연스러운 재배열")

# 색상
BLACK = (0, 0, 0)
BALL_COLOR = (100, 200, 255)

# 타원 궤도 반지름
RADIUS_X = 200
RADIUS_Y = 100

# FPS
clock = pygame.time.Clock()
FPS = 60

# 입력 문자열
input_str = ""

# 회전 속도 (전체 타원 회전)
orbit_angle = 0
orbit_speed = 0.5

# 공 클래스
class Ball:
    def __init__(self, index, total):
        self.relative_angle = index * (360 / total)  # 기준 각도
        self.target_relative_angle = self.relative_angle  # 재배열 목표

    def update(self, index, total):
        # 목표 각도 재설정
        self.target_relative_angle = index * (360 / total)

        # 부드럽게 각도 조정
        diff = (self.target_relative_angle - self.relative_angle + 360) % 360
        if diff > 180:
            diff -= 360
        self.relative_angle = (self.relative_angle + diff * 0.05) % 360

    def draw(self, surface, orbit_angle):
        total_angle = (self.relative_angle + orbit_angle) % 360
        rad = math.radians(total_angle)
        x = CENTER[0] + RADIUS_X * math.cos(rad)
        y = CENTER[1] + RADIUS_Y * math.sin(rad)

        pygame.draw.circle(surface, BALL_COLOR, (int(x), int(y)), 15)

# 공 리스트
balls = []

# 메인 루프
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_str.isdigit():
                    new_count = int(input_str)
                    current_count = len(balls)

                    # 리스트 길이 조절
                    if new_count > current_count:
                        for i in range(current_count, new_count):
                            balls.append(Ball(i, new_count))
                    elif new_count < current_count:
                        balls = balls[:new_count]

                    # 각 공에 새로운 목표 상대각도 설정
                    for i, ball in enumerate(balls):
                        ball.target_relative_angle = i * (360 / new_count)

                input_str = ""

            elif event.key == pygame.K_BACKSPACE:
                input_str = input_str[:-1]
            else:
                if event.unicode.isdigit():
                    input_str += event.unicode

    # 전체 궤도 회전
    orbit_angle = (orbit_angle + orbit_speed) % 360

    # 공 업데이트 및 그리기
    for i, ball in enumerate(balls):
        ball.update(i, len(balls))
        ball.draw(screen, orbit_angle)

    # 입력값 화면 표시
    font = pygame.font.SysFont(None, 36)
    input_surface = font.render(f"입력: {input_str}", True, (255, 255, 255))
    screen.blit(input_surface, (20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
