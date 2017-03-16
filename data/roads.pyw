from pygame import *
import mouse_extras, popups, extras


class Handler:

    def __init__(self):
        self.roads = []

        self.images = {
            'straight': image.load('images//roads//straight.png'),
            'corner': image.load('images//roads//corner.png'),
            't_intersection': image.load('images//roads//t_intersection.png'),
            'cross_intersection': image.load('images//roads//cross_intersection.png'),
        }

    def update(self, info):
        return self.get_images(info)

    mouse_last = None
    def draw_line(self, info):

        # Get mouse position on the game grid
        mouse_grid = mouse_extras.get_pos()

        # Is the mouse being held down?        
        if mouse.get_pressed()[0]:
            
            # Is this the first click?
            if not self.mouse_last:

                # Remember this position
                self.mouse_last = mouse_grid

            # Has the mouse already been clicked?
            else:
                # Add rects to show the path
                path = extras.make_line(self.mouse_last, mouse_grid)

                if len(path) > 1:
                    if path[0][0] == path[1][0]: rot = 0
                    else: change = rot = 90
                else: change = rot = 90

                for pos in path:
                    scale = info['window']['game_scale']

                    value = 'blit', self.images['straight'], (pos[0] * scale, pos[1] * scale, scale, scale), rot, 150
                    extras.show_things.append(value)

        # Has the mouse been let go?
        else:

            # Does it matter? (Were we remembering the position?)
            if self.mouse_last:

                # Make line between mouse position and where the mouse was first clicked
                path = extras.make_line(self.mouse_last, mouse_grid)

                # Add to roads
                for pos in path:
                    self.add_road(info, pos)
            
            # Reset
            self.mouse_last = None


    def draw(self, info):

        # This will dictate whether it is okay to draw the roads
        disable_mouse = abs(int(popups.check_mouse(info)) - 1)

        if not disable_mouse:

            # Draw road
            # self.draw_single(info)
            self.draw_line(info)
            
            # Remove road
            if mouse.get_pressed()[2]:
                self.remove_road(info, mouse_extras.get_pos())


    def draw_single(self, info):

        # Is the mouse clicked
        if mouse.get_pressed():

            # Get mouse things
            buttons = mouse.get_pressed()
            pos = mouse_extras.get_pos()

            # Has any mouse button been pressed
            any_button = False
            for button in buttons:
                if button: any_button = True; break

            # Place road
            if buttons[0] and not key.get_pressed()[K_LCTRL]:
                self.add_road(info, pos)

            # Remove road
            if buttons[2]:
                self.remove_road(info, pos)


    def remove_road(self, info, pos):

        # Is the mouse even on the game surface
        if pos[0] >= 0 and pos[1] >= 0:
            if pos[0] < info['grid_size'] and pos[1] < info['grid_size']:

                # Is a road there?
                for stuff in self.roads:
                    position, outs, rot, name = stuff
                    if tuple(pos) == tuple(position):

                        # Remove it
                        index = self.roads.index(stuff)
                        self.roads.pop(index)
                        self.update_neighbours(info, pos)
                        return


    def add_road(self, info, pos):

        # Is the mouse even on the game surface
        if pos[0] >= 0 and pos[1] >= 0:
            if pos[0] < info['grid_size'] and pos[1] < info['grid_size']:

                # Is there another road in the way?
                okay = True
                for stuff in self.roads:
                    position, outs, rot, name = stuff
                    if tuple(pos) == tuple(position):

                        okay = False
                        break

                if okay:
                    # Add roads

                    # Add a blank road to the list
                    self.roads.append((pos, 0, 0, 0))

                    # Update the road
                    self.update_road(pos, info)

                    # Update the roads around it
                    self.update_neighbours(info, pos)


    def update_neighbours(self, info, pos):

        for change in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_pos = pos[0] + change[0], pos[1] + change[1]

             # Is it a valid spot
            if new_pos[0] >= 0 and new_pos[1] >= 0 and new_pos[0] < info['grid_size'] and new_pos[1] < info['grid_size']:

                # Update
                self.update_road(new_pos, info)

    def get_images(self, info):
        images = []

        width = info['window']['game_scale']

        # Format = 'blit', img, rect, rotation
        for position, outs, rotation, img_name in self.roads:

            pos = position[0] * width, position[1] * width
            rect = int(pos[0]), int(pos[1]), width, width

            images.append(['blit', self.images[img_name], rect, rotation])
        return images


    def update_road(self, pos, info):

        # Find the index of the position
        index = None
        for road in self.roads:
            if tuple(road[0]) == tuple(pos):
                index = self.roads.index(road)

        if not index == None:

            # Find the roads around it
            up = False
            down = False
            right = False
            left = False

            for change_index in range(4):
                pos_change = [(0, 1), (1, 0), (-1, 0), (0, -1)][change_index]

                new_pos = pos[0] + pos_change[0], pos[1] + pos_change[1]

                # Is this a valid spot
                if new_pos[0] >= 0 and new_pos[1] >= 0 and new_pos[0] < info['grid_size'] and new_pos[1] < info['grid_size']:

                    # Is there a road with this pos
                    for road in self.roads:
                        if tuple(road[0]) == tuple(new_pos):

                            # What direction is it?
                            if change_index == 0: up = True
                            elif change_index == 1: right = True
                            elif change_index == 2: left = True
                            else: down = True

            neighbours = int(up) + int(down) + int(left) + int(right)

            # Cross intersection
            if neighbours == 4:
                road_img = 'cross_intersection'
                rotation = 0

            # T intersection
            elif neighbours == 3:
                road_img = 't_intersection'

                if not up: rotation = 180
                if not right: rotation = 90
                if not down: rotation = 0
                if not left: rotation = 270

            # Straight line or corner
            elif neighbours == 2:

                # Straight
                if (up and down) or (left and right):
                    road_img = 'straight'

                    if left and right: rotation = 90
                    else: rotation = 0

                # Corner
                else:
                    road_img = 'corner'

                    # Corner
                    if right and down: rotation = 270
                    elif right and up: rotation = 0
                    elif left and up: rotation = 90
                    elif left and down: rotation = 180

            # Straight
            elif neighbours == 1:

                road_img = 'straight'
                if up or down:
                    rotation = 0
                else:
                    rotation = 90

            else:
                road_img = 'straight'
                rotation = 0

            self.roads[index] = pos, neighbours, rotation, road_img
