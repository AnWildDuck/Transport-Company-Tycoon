import time, pygame

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
                if rect1[1] <= rect[1] + rect[3]:

                    # They are touching!
                    return True

    # Not touching! (This will only run if return is not already called, return stops the function)
    return False
            
