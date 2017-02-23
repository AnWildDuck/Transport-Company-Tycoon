from pygame import *
import mouse_extras

class Road_Handler:

    def __init__(self, grid_width):
        self.roads = []
        self.grid_width = grid_width

        self.images = {
            'straight': image.load('images//roads//straight.png'),
            'turn': image.load('images//roads//corner.png'),
            't': image.load('images//roads//t_intersection.png'),
            'cross': image.load('images//roads//cross_intersection.png'),
        }

    def place_roads(self):

        # Is the mouse in a valid position?
        pos = mouse_extras.get_pos()
        if pos[0] >= 0 and pos[0] < self.grid_width and pos[1] >= 0 and pos[1] < self.grid_width:

            # Is the map beign moved?
            if not key.get_pressed()[K_LCTRL]:

                # Is the right mouse button pressed
                if mouse.get_pressed()[2]:

                    # What road is it over?
                    for road_pos in self.roads:
                        if pos == road_pos:
                            self.roads.pop(self.roads.index(road_pos))


                # Is the mouse pressed?
                elif mouse.get_pressed()[0]:

                    okay = True
                    for road in self.roads:
                        if tuple(road) == tuple(pos):
                            okay = False
                            break

                    if okay:                            
                        # Place road
                        self.roads.append(pos)


    def show_roads(self, window, window_scale):
        directions = (0, 1), (0, -1), (1, 0), (-1, 0)

        for x, y in self.roads:

            up = False
            down = False
            left = False
            right = False

            for index in range(len(directions)):
                
                direction = list(directions[index])
                new_pos = direction[0] + x, direction[1] + y

                # Is there a road in the new pos?
                in_way = False
                for road in self.roads:
                    if tuple(road) == tuple(new_pos):
                        in_way = True
                        break

                if in_way:
                    if index == 0: up = True
                    if index == 1: down = True
                    if index == 2: right = True
                    if index == 3: left = True

            # What image should be used?
            outs = int(up) + int(down) + int(left) + int(right)

            # Cross intersection
            if outs == 4:
                img = self.images['cross']

            # Corner
            elif outs == 2 and not ((up and down) or (left and right)):
                img = self.images['turn']
                if down and left: img = transform.flip(img, 1, 1)
                if down and right: img = transform.flip(img, 0, 1)
                if up and left: img = transform.flip(img, 1, 0)

            # Straight
            elif outs <= 2:
                img = self.images['straight']

                # Does it need to be rotated?
                if left or right: img = transform.rotate(img, 90)

            elif outs == 3:
                img = self.images['t']

                # What rotation
                if not up: img = transform.flip(img, 0, 1)
                if not left: img = transform.rotate(img, 90)
                if not right: img = transform.rotate(img, 270)

            img = transform.scale(img, (int(window_scale + 0.5), int(window_scale + 0.5)))
            window.blit(img, (x * window_scale, y * window_scale))

            # draw.rect(window, (200, 200, 200), (x * window_scale, y * window_scale, window_scale, window_scale))
