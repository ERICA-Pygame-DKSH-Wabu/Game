import pygame
import os
import sys

def remove_white(surface_list, threshold=80):
    new_list = []
    for surf in surface_list:
        surf = surf.convert_alpha()
        w, h = surf.get_size()
        new_surf = pygame.Surface((w, h), pygame.SRCALPHA)

        for x in range(w):
            for y in range(h):
                r, g, b, a = surf.get_at((x, y))
                if r >= threshold and g >= threshold and b >= threshold:
                    new_surf.set_at((x, y), (0, 0, 0, 0))
                else:
                    new_surf.set_at((x, y), (r, g, b, a))

        new_list.append(new_surf)
    return new_list

def invert_surface_color(surface):
    arr = pygame.surfarray.pixels3d(surface).copy()
    alpha = pygame.surfarray.pixels_alpha(surface).copy()
    arr = 255 - arr  
    new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.surfarray.blit_array(new_surface, arr)
    pygame.surfarray.pixels_alpha(new_surface)[:] = alpha
    return new_surface

def get_resource_path(relative_path):
    """PyInstaller 실행파일에서도 작동하는 리소스 경로 반환"""
    try:
        # PyInstaller가 생성한 임시 폴더
        base_path = sys._MEIPASS
    except Exception:
        # 개발 환경
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, relative_path)

def get_font(path, size):
    full_path = get_resource_path(path)
    try:
        return pygame.font.Font(full_path, size)
    except FileNotFoundError:
        print(f"Warning: Font file not found: {path}, using default font")
        return pygame.font.Font(None, size)

def draw_text(screen, x, y, text, font, text_index, color=(255, 255, 255)):
    clipped_text = text[:int(text_index)]
    text_surface = font.render(clipped_text, True, color)
    text_rect = text_surface.get_rect(center=(x, y)) 
    screen.blit(text_surface, text_rect)

def get_im(path):
    full_path = get_resource_path(path)
    try:
        image = pygame.image.load(full_path)
        return image
    except FileNotFoundError:
        print(f"Warning: Image file not found: {path}")
        # 기본 이미지 반환 (마젠타색 사각형)
        surface = pygame.Surface((32, 32))
        surface.fill((255, 0, 255))
        return surface

def set_im(image, width, height, alpha, flip):
    imag = image.convert_alpha()
    im = pygame.transform.smoothscale(imag, (width, height))
    im.set_alpha(alpha)
    if not flip:
        im = pygame.transform.flip(im, True, False)
    return im

def get_frame(folder_path, width, height, alpha, flip=True):
    full_folder_path = get_resource_path(folder_path)
    
    # 폴더가 존재하는지 확인
    if not os.path.exists(full_folder_path):
        print(f"Warning: Folder not found: {folder_path}")
        return []
    
    try:
        filenames = sorted(
            [f for f in os.listdir(full_folder_path) if f.endswith(".png")],
            key=lambda x: int(os.path.splitext(x)[0])
        )
    except (ValueError, OSError) as e:
        print(f"Warning: Error reading folder {folder_path}: {e}")
        return []

    frame_list = []
    for filename in filenames:
        full_image_path = os.path.join(folder_path, filename)
        image = get_im(full_image_path)
        resized_image = set_im(image, width, height, alpha, flip)
        frame_list.append(resized_image)

    return frame_list