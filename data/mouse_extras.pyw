from pygame import *

grid_pos = (0, 0)

def update(info):
    update_pos(info)

def update_pos(info):

    offset = info['window']['pos']

    pos = list(mouse.get_pos())
    offset = list(offset)

    pos[0] -= offset[0]
    pos[1] -= offset[1]

    pos[0] /= info['window']['game_scale']
    pos[1] /= info['window']['game_scale']

    pos[0] = int(pos[0])
    pos[1] = int(pos[1])

    global grid_pos
    grid_pos = list(pos)

def get_pos():
    global grid_pos
    return list(grid_pos)
