from pygame import *
import math, mouse_extras, roads, functions
from win32api import GetSystemMetrics

def run(window_size, full_screen = False):

    colours = {
        'main_window_background': (0, 0, 0),
        'game_window_background': (100, 200, 100)
    }

    grid_width = 50
    grid_lines = 0
    money = 100000

    def event_loop():
        events = event.get()
        for e in events:
            if e.type == QUIT: quit()
        return events

    # SETUP
    monitor_size = GetSystemMetrics(0), GetSystemMetrics(1)
    if full_screen: main_window = display.set_mode(monitor_size, FULLSCREEN)
    else: main_window = display.set_mode(window_size, RESIZABLE)

    old_size = window_size

    clock = time.Clock()

    # Separate game window
    game_window_height = min(window_size)
    game_window = Surface((int(game_window_height), int(game_window_height)))

    zoom = 0.7
    zoom_speed = 5
    offset = [0, 0] # Offset from the center

    # Load images
    images = {
    }

    # Initiate Modules
    road_handler = roads.Road_Handler(grid_width)
    button_handler = functions.Popups()

    # button_handler.add_button()

    # Game loop
    while True:

        dt = clock.tick() / 1000
        events = event_loop()
        
        # Resize Things
        for loop in events:
            resize = False

            # Keypresses

            # Reset map positiion
            if loop.type == KEYDOWN:
                if loop.key == K_r:
                    offset = [0,0]
                    zoom = 0.7

                # Show cool things
                if loop.key == K_ESCAPE:
                    grid_lines = abs(grid_lines - 1)

                # Go into/quit fullscreen
                if loop.key == K_F2:
                    full_screen = abs(int(full_screen) - 1)

                    monitor_size = GetSystemMetrics(0), GetSystemMetrics(1)
                    if full_screen: main_window = display.set_mode(monitor_size, FULLSCREEN)
                    else: main_window = display.set_mode(old_size, RESIZABLE)

            if loop.type == VIDEORESIZE:
                # Fix offset
                scale = min(window_size) / min(loop.w, loop.h)
                offset[0] /= scale
                offset[1] /= scale
                # Resize window
                old_size = list(window_size)
                window_size = loop.w, loop.h
                if full_screen: main_window = display.set_mode(window_size, FULLSCREEN)
                else: main_window = display.set_mode(window_size, RESIZABLE)
                # Resize game window
                game_window_height = min(window_size)


            if loop.type == MOUSEBUTTONDOWN:
                # Scrolling
                if loop.button == 4: zoom += dt * zoom_speed * 0.5 # / ((zoom + 1) * 5)
                if loop.button == 5: zoom -= dt * zoom_speed * 0.5 # / ((zoom + 1) * 5)
                zoom = min(5, max(zoom, 0.2))

        # Move map around (adjust offset)
        rel = mouse.get_rel()
        if mouse.get_pressed()[0] and key.get_pressed()[K_LCTRL]:
            offset[0] += rel[0]
            offset[1] += rel[1] 

        # Set backgrounds
        game_window = Surface((game_window_height, game_window_height))

        main_window.fill(colours['main_window_background'])
        game_window.fill(colours['game_window_background'])

        # Set handy things
        scaled_game_size = zoom * game_window_height
        game_scale = game_window_height / grid_width
        window_scale = scaled_game_size / game_window_height

        window_offset = (window_size[0] - scaled_game_size) / 2 + offset[0], (window_size[1] - scaled_game_size) / 2 + offset[1]
        mouse_extras.update(window_scale, game_scale, window_offset)

        # Base pixel size
        pixel_size = game_window_height / scaled_game_size
        game_scale = game_window_height / grid_width

        # Show the items here
        road_handler.place_roads()
        road_handler.show_roads(game_window, game_scale)


        # Grid lines
        if grid_lines:
            for x in range(grid_width):
                x *= game_scale
                draw.line(game_window, (0, 0, 100), (x, 0), (x, game_window_height), int(pixel_size * 2 + 0.5))
            for y in range(grid_width):
                y *= game_scale
                draw.line(game_window, (0, 0, 100), (0, y), (game_window_height, y), int(pixel_size * 2 + 0.5))

        # Update screen
        game_window = transform.scale(game_window, (int(scaled_game_size), int(scaled_game_size)))

        x = (window_size[0] - scaled_game_size) / 2 + offset[0]
        y = (window_size[1] - scaled_game_size) / 2 + offset[1]

        main_window.blit(game_window, (x, y))
        display.update()


init()
run((500, 500))
 