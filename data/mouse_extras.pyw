from pygame import *

grid_pos = (0, 0)

def update(window_scale, game_scale, offset):
    update_pos(window_scale, game_scale, offset)

def update_pos(window_scale, game_scale, offset):
    pos = list(mouse.get_pos())
    offset = list(offset)

    pos[0] -= offset[0]
    pos[1] -= offset[1]

    pos[0] /= window_scale
    pos[1] /= window_scale

    pos[0] /= game_scale
    pos[1] /= game_scale

    pos[0] = int(pos[0])
    pos[1] = int(pos[1])

    global grid_pos
    grid_pos = list(pos)

def get_pos():
    global grid_pos
    return list(grid_pos)
