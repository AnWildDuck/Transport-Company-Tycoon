import time, pygame, math

change = 0
def edit_money(c):
    global change
    change += c

def update_money(info):
    global change
    info['user_info']['money'] += change
    change = 0
    return info


fonts = {}
def show_message(info, message, pos, size, colour = (0, 0, 0), background = (255, 255, 255), margin = 0.2, alpha = 255, window_name = 'main_window', side = 'left'):
    pos = list(pos)
    
    rect = info[window_name].get_rect()
    window_size = rect.width, rect.height

    global fonts
    size = int(size * 0.8)

    # Change font if needed

    # Has the font been loaded?
    try:
        font = fonts[str(size)]
    except:

        # Load font
        font = pygame.font.SysFont('arial', int(size))
        fonts[str(size)] = font

    message = font.render(message, 0, colour)

    margin = margin * size
    mes_rect = message.get_rect()

    new_rect = pos[0], pos[1], mes_rect.width + 2 * margin, mes_rect.height + 2 * margin

    # Background rectangles
    if background:
        window = pygame.Surface((new_rect[2], new_rect[3]))
        window.fill(background)
        pygame.draw.rect(window, colour, (0, 0, new_rect[2], new_rect[3]), int(max(1, size / 7)))

        # Message
        window.blit(message, (margin, margin))
        window.set_alpha(alpha)

    else:
        window = message

    # Make sure the message is on the window
    window_size = info['window']['in_use_size']
    pos[0] = max(pos[0], 0)
    pos[1] = max(pos[1], 0)

    pos[0] = min(pos[0], window_size[0] - new_rect[2])
    pos[1] = min(pos[1], window_size[1] - new_rect[3])

    if side == 'right': pos[0] = window_size[0] - margin - mes_rect.width

    info[window_name].blit(window, pos)


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

def on_screen(info, rect):

    if not info['fullscreen']: window_rect = (0, 0, info['window']['size'][0], info['window']['size'][1])
    else: window_rect = (0, 0, info['monitor_size'][0], info['monitor_size'][1])

    new_rect = rect[0] + info['window']['pos'][0], rect[1] + info['window']['pos'][1], rect[2], rect[3]

    if touching(new_rect, window_rect):
        return True
    return False

show_things = []
def show_everthing(info):
    global show_things
    max_things = len(show_things)

    shown_things = 0

    # Show all the things
    for thing in show_things:

        filter = True

        # Is it an image?
        if thing[0] == 'blit':

            if len(thing) == 4: name, img, rect, rotation = thing; alpha = False
            else: name, img, rect, rotation, alpha = thing

            pos = int(rect[0]), int(rect[1])
            size = math.ceil(rect[2]), math.ceil(rect[3])

            rect = pos[0], pos[1], size[0], size[1]

            # Is the rect on the screen
            if on_screen(info, rect):

                img = pygame.transform.rotate(img, -rotation)
                img = pygame.transform.scale(img, size)

                # Draw
                if alpha:
                    blit_alpha(info['game_window'], img, pos, alpha)
                    shown_things += 1

                else:
                    info['game_window'].blit(img, pos)
                    shown_things += 1


        # Is it a line?
        elif thing[0] == 'line':

            # Is it visible to the player?
            rect = thing[2][0], thing[2][1], thing[2][0] - thing[3][0], thing[2][1] - thing[3][1]
            if on_screen(info, rect):

                # Draw it
                pygame.draw.line(info['game_window'], thing[1], thing[2], thing[3])
                shown_things += 1

        # Is it a rect
        elif thing[0] == 'rect':

            # Is it visible to the player
            rect = thing[1]
            if on_screen(info, rect):

                # Show it

                # Alpha
                if len(thing[2]) == 4:
                    surf = pygame.Surface(rect[2:])
                    surf.fill(thing[2])
                    surf.set_alpha(thing[2][3])
                    info['game_window'].blit(surf, rect[:2])

                # Outline
                elif len(thing) >= 4:
                    pygame.draw.rect(info['game_window'], thing[2], rect, thing[3])

                # No outline
                else:
                    pygame.draw.rect(info['game_window'], thing[2], rect)


    show_things = []
    add_info('Showing ' + str(shown_things) + '/' + str(max_things) + ' items')



last_time = 0
frames = 0
last_fps = 0

pygame.font.init()
base_font = pygame.font.SysFont(None, 30)

def fps_counter(window, avg = False):
    global last_time, base_font, frames, last_fps
    this_time = time.time()

    if avg:

        if this_time - avg >= last_time:
            fps = frames * (1 / avg)
            last_time = this_time
            frames = 0
            last_fps = fps

        else:
            frames += 1
            fps = last_fps

    else:
        time_dif = this_time - last_time

        if time_dif != 0: fps = 1 / time_dif
        else: fps = 0

    # Message surface
    message = base_font.render(str(int(fps)), 0, (255, 255, 50))

    #Info about the display window (position, size etc)
    window_rect = window.get_rect()
    margin = min(window_rect.width, window_rect.height) / 100

    # Show it
    window.blit(message, (margin, margin))

    # Update time
    if not avg:
        last_time = this_time


info = []
def add_info(message):

    global info
    info.append(message)

def show_info(window):
    global base_font, info

     #Info about the display window (position, size etc)
    window_rect = window.get_rect()
    margin = min(window_rect.width, window_rect.height) / 100

    for index in range(len(info)):
        message = info[index]

        # Message surface
        message = base_font.render(message, 0, (255, 255, 50))
        message_rect = message.get_rect()

        y = (message_rect.height + margin) * index + margin

        # Show it
        window.blit(message, (window_rect.width - margin - message_rect.width, y))

    info = []



def touching(rect1, rect2):

    # Is rect1 not too far right
    if rect1[0] <= rect2[0] + rect2[2]:

        # Is rect1 not too far left
        if rect1[0] + rect1[2] >= rect2[0]:

            # Is rect1 not too high
            if rect1[1] + rect1[3] >= rect2[1]:

                # Is rect1 not too low
                if rect1[1] <= rect2[1] + rect2[3]:

                    # They are touching!
                    return True

    # Not touching! (This will only run if return is not already called, return stops the function)
    return False


def make_line(pos1, pos2):

    # Get gradient
    xc = pos1[0] - pos2[0]
    yc = pos1[1] - pos2[1]

    # Where is the corner pos?
    if abs(xc) > abs(yc):
        x = pos2[0]
        y = pos1[1]

        if xc < 0: change1 = (-1, 0)
        else: change1 = (1, 0)


    else:
        x = pos1[0]
        y = pos2[1]

        if yc < 0: change1 = (0, -1)
        else: change1 = (0, 1)

    path = [pos1]
    # Add all the points before the corner
    for val in range(max(abs(xc), abs(yc))):

        last_pos = path[len(path) - 1]
        this_pos = last_pos[0] - change1[0], last_pos[1] - change1[1]

        path.append(this_pos)
    return path



def make_line2(pos1, pos2, dist_method = 1):

    path = [pos1]
    while True:
        last_pos = path[len(path) - 1]

        # Is the end already found?
        if tuple(last_pos) == tuple(pos2): break

        # Used to find the move that gets the closest to the destination        
        moves = []
        distances = []

        # What move should be taken to get closer to the desination?
        for xc, yc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: 

            # Work out new pos
            this_pos = last_pos[0] + xc, last_pos[1] + yc
            moves.append(this_pos)

            # Find dist
            xd = abs(pos2[0] - this_pos[0])
            yd = abs(pos2[1] - this_pos[1])

            if dist_method == 0: dist = math.sqrt(xd ** 2 + yd ** 2)
            elif dist_method == 1: dist = xd + yd
            distances.append(dist)

        # Find min dist and its pos
        best_dist = min(distances)
        index = distances.index(best_dist)
        best_pos = moves[index]

        # Add to path
        path.append(best_pos)

    return path
