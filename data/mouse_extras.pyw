from pygame import *

grid_pos = (0, 0)

states = [0, 0, 0]
last_state = [0, 0, 0]

def update(info):
    update_pos(info)
    update_states()

def get_states():
    global states
    return list(states)

def update_states():

    global last_state, states
    new_state = mouse.get_pressed()

    if states:    
        states = []
        for index in range(len(new_state)):
            state = new_state[index] - last_state[index]
            states.append(state)
        last_state = new_state

    else:
        last_state = new_state
        states = new_state


    

    


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
