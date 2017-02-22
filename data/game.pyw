from pygame import *
import math

def run(window_size):

    colours = {
        'main_window_background': (0, 0, 0),
        'game_window_background': (100, 200, 100)
    }

    grid_width = 20
    grid_lines = 0

    def event_loop():
        events = event.get()
        for e in events:
            if e.type == QUIT: quit()
        return events

    # SETUP
    main_window = display.set_mode(window_size, RESIZABLE)
    clock = time.Clock()

    # Separate game window
    game_window_height = min(window_size)
    game_window = Surface((int(game_window_height), int(game_window_height)))

    zoom = 0.7
    zoom_speed = 5
    offset = [0, 0] # Offset from the center

    # Load images
    images = {
        'background': image.load('images//backgrounds//grassy.png')
    }

    # Game loop
    while True:

        dt = clock.tick() / 1000
        events = event_loop()
        
        # Resize Things
        for loop in events:
            if loop.type == VIDEORESIZE:
                # Fix offset
                scale = min(window_size) / min(loop.w, loop.h)
                offset[0] /= scale
                offset[1] /= scale
                # Resize window
                window_size = loop.w, loop.h
                main_window = display.set_mode(window_size, RESIZABLE)
                # Resize game window
                game_window_height = min(window_size)

            if loop.type == KEYDOWN:
                if loop.key == K_r:
                    offset = [0,0]
                    zoom = 0.7

                if loop.key == K_ESCAPE:
                    grid_lines = abs(grid_lines - 1)

            if loop.type == MOUSEBUTTONDOWN:
                # Scrolling
                if loop.button == 5: zoom += dt * zoom_speed * 0.5 # / ((zoom + 1) * 5)
                if loop.button == 4: zoom -= dt * zoom_speed * 0.5 # / ((zoom + 1) * 5)
                zoom = min(2, max(zoom, 0.2))

        # Move map around (adjust offset)
        rel = mouse.get_rel()
        if mouse.get_pressed()[0] and key.get_pressed()[K_LCTRL]:
            offset[0] += rel[0]
            offset[1] += rel[1] 

        # Set backgrounds
        game_window = Surface((game_window_height, game_window_height))
        game_window_scale = game_window_height / grid_width

        # Game window
        game_window.fill(colours['game_window_background'])
        # game_window.blit(transform.scale(images['background'], (game_window_height, game_window_height)), (0, 0))

        # Set handy thing
        game_scale = game_window_height / grid_width

        # Base pixel size
        game_window_size = int(zoom * game_window_height)
        pixel_size = game_window_height / game_window_size

        # Show the items here

        # Grid lines
        if grid_lines:
            for x in range(grid_width):
                x *= game_scale
                draw.line(game_window, (0, 0, 100), (x, 0), (x, game_window_height), int(pixel_size * 2 + 0.5))
            for y in range(grid_width):
                y *= game_scale
                draw.line(game_window, (0, 0, 100), (0, y), (game_window_height, y), int(pixel_size * 2 + 0.5))


        # Main window
        main_window.fill(colours['main_window_background'])

        # Update screen
        game_window_size = int(zoom * game_window_height)
        game_window = transform.scale(game_window, (game_window_size, game_window_size))

        x = (window_size[0] - game_window_size) / 2 + offset[0]
        y = (window_size[1] - game_window_size) / 2 + offset[1]

        main_window.blit(game_window, (x, y))
        display.set_caption(str(game_window_size))
        display.update()


init()
run((500, 500))
 