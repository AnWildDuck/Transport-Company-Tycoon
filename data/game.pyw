from pygame import *
def run():

    # Requires user input so a nice error message is good
    try:
        file = open('data//settings.txt', 'r')
        info = dict(eval(file.read()))
        file.close()
    except Exception as error:
        print('Error Loading settings file')
        print(error)
        return


    # Setup
    init()

    # Cool things
    zoom = 0
    offset = (0, 0)

    def resize_main(info):

        # Window size things
        info['window']['game_window_width'] = min(info['window']['size'])
        info['window']['game_scale'] = info['window']['game_window_width'] / info['grid_size']

        # The game window
        game_window = Surface((info['window']['game_window_width'],) * 2)

        # The actual window
        main_window = display.set_mode(info['window']['size'], RESIZABLE)
        return info, main_window, game_window


    # Without this pygame will stop
    def event_loop():
        events = event.get()
        for i in events:
            if i.type == QUIT: quit()
        return events

    # Set up
    info, main_window, game_window = resize_main(info)
    
    # Game Loop
    while True:

        info['events'] = event_loop()

        # Resize loop
        for e in info['events']:
            if e.type == VIDEORESIZE:
                info['window']['size'] = (e.w, e.h)
                info, main_window, game_window = resize_main(info)

        # Window Background
        main_window.fill(info['window_background'])

        # Show items
        game_window.fill(info['game_background'])

        pos = ((info['window']['size'][0] - info['window']['game_window_width']) / 2 + offset[0],
            (info['window']['size'][1] - info['window']['game_window_width']) / 2 + offset[1])

        main_window.blit(game_window, pos)

        display.update()

run()