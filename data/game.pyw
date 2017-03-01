from pygame import *
import extras

def get_dir():
    import os
    cwd = os.getcwd()

def run():

    # Load settings from 'settings.txt'
    # Requires user input so a nice error message is good
    try:
        file = open('settings.txt', 'r')
        info = dict(eval(file.read()))
        file.close()
    except Exception as error:
        print('Error Loading settings file')
        print(error)
        return


    # Setup
    init()
    clock = time.Clock()


    # Cool grid lines and stuff
    hidden_items = True

    # game_window_width is the unscaled size, game_surf_width is scaled
    info['window']['game_window_width'] = min(info['window']['size'])
    info['window']['game_surf_width'] = info['window']['game_window_width'] * info['zoom']

    def update_pixel_size(info):
        info['window']['pixel_size'] = info['window']['game_window_width'] / info['window']['game_surf_width'] + 0.5
        return info

    def show_grid_lines(game_window, info):
        for x in range(info['grid_size']):
            x = info['window']['game_scale'] * x + info['window']['top_pos'][0]
            draw.line(game_window, (50, 0, 0), (int(x), 0), (int(x), int(info['window']['game_surf_width'])), 1)# int(info['window']['pixel_size']))
        for y in range(info['grid_size']):
            y = info['window']['game_scale'] * y + info['window']['top_pos'][1]
            draw.line(game_window, (50, 0, 0), (0, y), (int(info['window']['game_surf_width']), int(y)), 1)# int(info['window']['pixel_size']))

    def resize_main(info):

        # Window size things
        info['window']['game_surf_width'] = min(info['window']['size'])
        info['window']['game_scale'] = info['window']['game_surf_width'] / info['grid_size']

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
    info = update_pixel_size(info)


    # -----------
    #  Game Loop
    # -----------

    
    while True:

        # dt or delta time is used to make things move at the correct speed when fps changes
        info['dt'] = clock.tick() / 1000
        info['events'] = event_loop()

        for e in info['events']:
            
            # Resize
            if e.type == VIDEORESIZE:
                info['window']['size'] = (e.w, e.h)
                info, main_window, game_window = resize_main(info)

            # Zoom
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 5: info['zoom'] += .9 * info['dt'] * info['zoom'] # Zoom in
                if e.button == 4: info['zoom'] -= .9 * info['dt'] * info['zoom'] # Zoom out

                if e.button == 4 or e.button == 5:
                    info['zoom'] = max(0.6, info['zoom'])
                    info['window']['game_scale'] = info['window']['game_surf_width'] / info['grid_size']

        # Move
        mouse_buttons = mouse.get_pressed()
        info['mouse_rel'] = mouse.get_rel()
        
        # Change the offset
        if key.get_pressed()[K_LCTRL] and mouse_buttons[0] or mouse_buttons[1]:
            info['offset'][0] += info['mouse_rel'][0]
            info['offset'][1] += info['mouse_rel'][1]
        

        info = update_pixel_size(info)

        # The size of the shown window (making the surface to the full size was what made it so laggy)
        # This solution makes things a little confusing (Keeping track of more variables and a little more math) but is worth it
        info['window']['real_game_size'] = (min(info['window']['game_surf_width'], info['window']['size'][0]),
                                            min(info['window']['game_surf_width'], info['window']['size'][1]))

        # One of the extra variables needed (Keeps track of where (0, 0) would be on the fully scaled version relitave to (0, 0) on the 'real_game_size'
        info['window']['top_pos'] = ((info['window']['real_game_size'][0] - info['window']['game_surf_width']) / 2,
                                     (info['window']['real_game_size'][1] - info['window']['game_surf_width']) / 2)

        # The position and size of the 'real_game_size' window on the fully scaled one
        info['window']['max_rect'] = (-info['window']['top_pos'][0],
                                      -info['window']['top_pos'][1],
                                      info['window']['real_game_size'][0],
                                      info['window']['real_game_size'][1])
                    
        # Window Background
        main_window.fill(info['window_background'])

        # Show items
        info['window']['game_surf_width'] = info['window']['game_window_width'] * info['zoom']
        #game_window = transform.scale(game_window, (int(info['window']['game_surf_width']),) * 2)
        #game_window = Surface((min(info['window']['game_surf_width'], info['window']['size'][0]), min(info['window']['game_surf_width'], info['window']['size'][1])))
        game_window = Surface(info['window']['real_game_size'])
        game_window.fill(info['game_background'])

        # This sets the name of the window, It is just showing cool info to make sure everythin is a-okay
        display.set_caption(str(round(info['zoom'], 5)) + '   ' + str(info['window']['top_pos']))

        # Position of the 'real_game_size' window on the main window
        pos = ((info['window']['size'][0] - (info['window']['real_game_size'][0])) / 2 + info['offset'][0],
            (info['window']['size'][1] - (info['window']['real_game_size'][1])) / 2 + info['offset'][1])

        # Show grid lines
        #if hidden_items: show_grid_lines(game_window, info)

        # Add the game window to the main
        main_window.blit(game_window, pos)

        # Show fps
        extras.fps_counter(main_window)

        # Update the screen!
        display.update()

run()
