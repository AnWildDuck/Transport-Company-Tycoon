import time, pygame


show_things = []
def show_everthing(info):
    global show_things

    shown_things = 0
    max_things = len(show_things)

    window_rect = (0, 0, info['window']['size'][0], info['window']['size'][1])

    # Show all the things
    for thing in show_things:

        # Is it an image?
        if thing[0] == 'blit':

            name, img, rect, rotation = thing

            pos = int(rect[0]), int(rect[1])
            size = int(rect[2]), int(rect[3])

            img = pygame.transform.scale(img, size)
            img = pygame.transform.rotate(img, -rotation)

            # Is the rect on the screen
            new_rect = img.get_rect()
            new_rect = rect[0], rect[1], new_rect.width, new_rect.height

            if touching(new_rect, window_rect):

                # Draw
                info['game_window'].blit(img, pos)

        # Is it a line?
        elif thing[0] == 'line':

            # Is it visible to the player?
            top_left = min(thing[2][0], thing[3][0]) + info['window']['pos'][0], min(thing[2][1], thing[3][1]) + info['window']['pos'][1]
            size = (abs(thing[2][0] - thing[3][0]), abs(thing[2][1] - thing[3][1]))

            thing_rect = (top_left[0], top_left[1], size[0], size[1])
            if touching(window_rect, thing_rect):

                # Draw it
                pygame.draw.line(info['game_window'], thing[1], thing[2], thing[3])
                shown_things += 1

    # Set the window name
    info['window']['name'] = 'Showing ' + str(shown_things) + ' / ' + str(max_things) + ' items'
    show_things = []



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
            
