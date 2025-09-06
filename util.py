import pygame
import os
import pygame

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

def get_font(path, size):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, path)
    return pygame.font.Font(full_path, size)


def draw_text(screen,x,y,text,font,text_index,color=(255,255,255)):
    clipped_text = text[:int(text_index)]
    text_surface = font.render(clipped_text, True, color)
    text_rect = text_surface.get_rect(center=(x,y)) 
    screen.blit(text_surface, text_rect)
def get_im(path):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, path)
    image = pygame.image.load(full_path)
    return image

def set_im(image, width, height,alpha,flip):
    imag=image.convert_alpha()
    im=pygame.transform.smoothscale(imag, (width, height))
    im.set_alpha(alpha)
    if not flip:
        im=pygame.transform.flip(im, True, False)
    return im

def get_frame(folder_path, width, height, alpha,flip=True):
    base_path = os.path.dirname(__file__)
    full_folder_path = os.path.join(base_path, folder_path)

    filenames = sorted(
        [f for f in os.listdir(full_folder_path) if f.endswith(".png")],
        key=lambda x: int(os.path.splitext(x)[0])
    )

    frame_list = []
    for filename in filenames:
        full_image_path = os.path.join(folder_path, filename)
        image = get_im(full_image_path)
        resized_image = set_im(image, width, height, alpha,flip)
        frame_list.append(resized_image)

    return frame_list