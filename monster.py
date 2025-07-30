import pygame
from spirit import *

monster_list = [] 

class Monster(Spirit):
    shared_frames = {}

    def __init__(self, pos, m_type):
        super().__init__(pos)
        self.name = m_type
        self.im_size = 150

        if m_type not in Monster.shared_frames:
            Monster.shared_frames[m_type] = self.load_frames(m_type)

        self.frame = Monster.shared_frames[m_type]
        self.img = self.frame["idle"][0]

    def load_frames(self, m_type):
        frame_dict = {
            "idle": get_frame(f"asset/spirit/{m_type}/idle", self.im_size, self.im_size, 4),
        }
        return frame_dict


def get_monsters():
    return monster_list

def update_wave(wave_data, wave_index, monster_pos_list):
    monster_list.clear()
    wave = wave_data[wave_index]
    for idx in range(1, 5):
        key = f"index_{idx}"
        if key in wave:
            for k, m_type in enumerate(wave[key]):
                pos_index = k * 4 + (idx - 1)
                if pos_index < len(monster_pos_list):
                    m = Monster(monster_pos_list[pos_index], m_type)
                    m.set_frame()
                    m.img = m.frame["idle"][0]
                    monster_list.append(m)
