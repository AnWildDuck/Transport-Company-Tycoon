from pygame import *
import mouse_extras, popups, extras


class Handler:

    def __init__(self):

        self.pos = []
        self.outs = []
        self.img_names = []
        self.rots = []

        self.images = {
            'straight': image.load('images//roads//straight.png'),
            'corner': image.load('images//roads//corner.png'),
            't_intersection': image.load('images//roads//t_intersection.png'),
            'cross_intersection': image.load('images//roads//cross_intersection.png'),
        }

        self.road_cost = 5
        self.refund_value = self.road_cost

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

                # Is this valid pos?
                if mouse_grid[0] >= 0 and mouse_grid[0] < info['grid_size'] and mouse_grid[1] >= 0 and mouse_grid[1] < info['grid_size']:

                    # Remember this position
                    self.mouse_last = mouse_grid

            # Has the mouse already been clicked?
            else:

                # Correct pos
                mouse_grid[0] = max(min(mouse_grid[0], info['grid_size'] - 1), 0)
                mouse_grid[1] = max(min(mouse_grid[1], info['grid_size'] - 1), 0)

                # Add rects to show the path
                path = extras.make_line(self.mouse_last, mouse_grid)

                # Does the player have enough money?
                cost = self.road_cost * len(path)

                if cost > info['user_info']['money']:
                    colour = (255, 0, 0, 50)
                else:
                    colour = False


                if len(path) > 1:
                    if path[0][0] == path[1][0]: rot = 0
                    else: change = rot = 90
                else: change = rot = 90

                for pos in path:
                    scale = info['window']['game_scale']

                    value = 'blit', self.images['straight'], (pos[0] * scale, pos[1] * scale, scale, scale), rot, 150
                    extras.show_things.append(value)
                    
                if colour:
                    fpos = path[0]
                    lpos = path[len(path) - 1]

                    x = min(fpos[0], lpos[0])
                    y = min(fpos[1], lpos[1])

                    width = abs(fpos[0] - lpos[0]) + 1
                    height = abs(fpos[1] - lpos[1]) + 1

                    rect = (x * scale, y * scale, width * scale, height * scale)

                    value = 'rect', rect, colour
                    extras.show_things.append(value)

                # Show cost
                pos = list(path[int(len(path) / 2)])
                pos[0] *= info['window']['game_scale']; pos[1] *= info['window']['game_scale']
                pos[0] = int(pos[0] + info['window']['pos'][0]); pos[1] = int(pos[1] + info['window']['pos'][1])
                message = 'Cost: ' + str(self.road_cost * len(path))
                extras.show_message(info, message, pos, 20, colour = (0, 0, 0), background = (255, 255, 255), margin = 0.2, alpha = 128)

        # Has the mouse been let go?
        else:

            # Does it matter? (Were we remembering the position?)
            if self.mouse_last:

                # Make line between mouse position and where the mouse was first clicked
                path = extras.make_line(self.mouse_last, mouse_grid)

                # Does the user have enough money
                if self.road_cost * len(path) <= info['user_info']['money']:
 
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
            self.remove_section(info)


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


    last_mouse2 = None
    def remove_section(self, info):

        new_pos = mouse_extras.get_pos()

        new_pos[0] = max(min(new_pos[0], info['grid_size']), 0)
        new_pos[1] = max(min(new_pos[1], info['grid_size']), 0)

        # Is the mouse clicked?
        if mouse.get_pressed()[2]:

            # Is this the first time
            if not self.last_mouse2:

                # Set last mouse pos
                self.last_mouse2 = new_pos

            else:
                scale = info['window']['game_scale']

                # Make rect
                x = min(self.last_mouse2[0], new_pos[0])
                y = min(self.last_mouse2[1], new_pos[1])

                width = abs(self.last_mouse2[0] - new_pos[0]) + 1
                height = abs(self.last_mouse2[1] - new_pos[1]) + 1

                # Show rect
                value = 'rect', (x * scale, y * scale, width * scale, height * scale), (255, 100, 100, 100)
                extras.show_things.append(value)

                amount = 0

                # What is the refund value?
                for nx in range(width):
                    for ny in range(height):

                        tx = nx + x
                        ty = ny + y

                        if (tx, ty) in self.pos:
                            amount += 1

                # Show refund value
                value = amount * self.refund_value
                message = 'Refund: ' + str(value)
                extras.show_message(info, message, mouse.get_pos(), 20, colour = (0, 0, 0), background = (255, 255, 255), margin = 0.2, alpha = 255)


        # Has the mouse been let go
        else:
            if self.last_mouse2:

                # Make rect
                x = min(self.last_mouse2[0], new_pos[0])
                y = min(self.last_mouse2[1], new_pos[1])

                width = abs(self.last_mouse2[0] - new_pos[0]) + 1
                height = abs(self.last_mouse2[1] - new_pos[1]) + 1

                # Remove all roads in rect
                for nx in range(width):
                    for ny in range(height):

                        tx = nx + x
                        ty = ny + y

                        self.remove_road(info, (tx, ty))

            self.last_mouse2 = None


    def remove_road(self, info, pos):

        # Find index
        if tuple(pos) in self.pos:
            index = self.pos.index(tuple(pos))

            # Remove from all lists
            self.pos.pop(index)
            self.outs.pop(index)
            self.img_names.pop(index)
            self.rots.pop(index)

            self.update_neighbours(info, pos)
            extras.edit_money(self.refund_value)


    def add_road(self, info, pos):

        # Is the mouse even on the game surface
        if pos[0] >= 0 and pos[1] >= 0:
            if pos[0] < info['grid_size'] and pos[1] < info['grid_size']:

                # Is there another road in the way?
                if not tuple(pos) in self.pos:
                    # Add roads

                    # Add a blank road to the list
                    self.pos.append(tuple(pos))
                    self.rots.append(0)
                    self.outs.append(0)
                    self.img_names.append(0)

                    extras.edit_money(-self.road_cost)

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
        for index in range(len(self.pos)):

            position = self.pos[index]
            img_name = self.img_names[index]
            rotation = self.rots[index]

            pos = position[0] * width, position[1] * width
            rect = int(pos[0]), int(pos[1]), width, width

            images.append(['blit', self.images[img_name], rect, rotation])
        return images


    def update_road(self, pos, info):

        # Find the index of the position
        if tuple(pos) in self.pos: index = self.pos.index(tuple(pos))
        else: index = None

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
                    if tuple(new_pos) in self.pos:

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

            self.pos[index] = tuple(pos)
            self.img_names[index] = road_img
            self.outs[index] = neighbours
            self.rots[index] = rotation
