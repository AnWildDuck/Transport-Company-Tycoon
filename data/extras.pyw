import time, pygame, math


def show_message(info, message, pos, size, colour = (0, 0, 0), backround = (255, 255, 255), margin = 0.2, alpha = 255):

    font = pygame.font.SysFont('arial', int(size))
    message = font.render(message, 0, colour)

    margin = margin * size
    mes_rect = message.get_rect()

    new_rect = pos[0], pos[1], mes_rect.width + 2 * margin, mes_rect.height + 2 * margin
    window = pygame.Surface((new_rect[2], new_rect[3]))

    # Background rectangles
    window.fill(backround)
    pygame.draw.rect(window, colour, (0, 0, new_rect[2], new_rect[3]), int(max(1, size / 7)))

    # Message
    window.blit(message, (margin, margin))

    window.set_alpha(alpha)
    info['main_window'].blit(window, pos)




show_things = []
def show_everthing(info):
    global show_things
    max_things = len(show_things)

    shown_things = 0

    if not info['fullscreen']:
        window_rect = (0, 0, info['window']['size'][0], info['window']['size'][1])
    else:
        window_rect = (0, 0, info['monitor_size'][0], info['monitor_size'][1])

    # Show all the things
    for thing in show_things:

        filter = True

        # Is it an image?
        if thing[0] == 'blit':

            name, img, rect, rotation = thing

            pos = int(rect[0]), int(rect[1])
            size = math.ceil(rect[2]), math.ceil(rect[3])

            img = pygame.transform.rotate(img, -rotation)
            img = pygame.transform.scale(img, size)

            # Is the rect on the screen
            new_rect = img.get_rect()
            new_rect = rect[0] + info['window']['pos'][0], rect[1] + info['window']['pos'][1], new_rect.width, new_rect.height

            if touching(new_rect, window_rect) or not filter:

                # Draw
                info['game_window'].blit(img, pos)
                shown_things += 1


        # Is it a line?
        elif thing[0] == 'line':

            # Is it visible to the player?
            top_left = min(thing[2][0], thing[3][0]) + info['window']['pos'][0], min(thing[2][1], thing[3][1]) + info['window']['pos'][1]
            size = (abs(thing[2][0] - thing[3][0]), abs(thing[2][1] - thing[3][1]))

            thing_rect = (top_left[0], top_left[1], size[0], size[1])

            if touching(window_rect, thing_rect) or not filter:

                # Draw it
                pygame.draw.line(info['game_window'], thing[1], thing[2], thing[3])
                shown_things += 1

    show_things = []
    add_info('Showing ' + str(shown_things) + '/' + str(max_things) + ' items')



last_time = 0
pygame.font.init()
base_font = pygame.font.SysFont(None, 30)

def fps_counter(window):
    global last_time, base_font

    this_time = time.time()
    time_dif = this_time - last_time
    fps = 1 / time_dif

    # Message surface
    message = base_font.render(str(int(fps)), 0, (255, 255, 50))

    #Info about the display window (position, size etc)
    window_rect = window.get_rect()
    margin = min(window_rect.width, window_rect.height) / 100

    # Show it
    window.blit(message, (margin, margin))

    # Update time
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
            
