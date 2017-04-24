from pygame import *
import time, random, extras

class Handler:

        def __init__(self):
            self.houses = []
            self.images = []
            self.valid_positions = []
            self.house_imgs = [
                    image.load('images//buildings//houses//house_1x1-1.png'),
                    image.load('images//buildings//houses//house_1x1-2.png'),
                    image.load('images//buildings//houses//house_1x1-3.png'),
                    ]
        
        def update(self, info):
            self.update_trigger(info)
            self.make_houses(info)
            self.show(info)

        last_state = 0
        def update_trigger(self, info):

            # Is road editing off?
            if not info['popups']['road_edit'].clicked:
                # Was it on before?
                if self.last_state:
                    self.update_valid_pos(info)
                    
            self.last_state = info['popups']['road_edit'].clicked

        def update_valid_pos(self, info):
            used_pos = list(info['used_pos'])

            valid_pos = []

            # Get all positions around all roads
            for pos, id in used_pos:
                if id == 'road':

                    # Add all neighbours
                    for xc, yc in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                        new_pos = pos[0] + xc, pos[1] + yc

                        # Is it already in the list?
                        if not new_pos in valid_pos:

                            # Add it
                            valid_pos.append(new_pos)

            # Remove all invalid positions
            for pos, id in used_pos:

                # Is the invalid pos in valid_pos?
                if pos in valid_pos:

                    # Remove it
                    index = valid_pos.index(pos)
                    valid_pos.pop(index)

            # Update list
            self.valid_positions = list(valid_pos)

                                   
        last_make = 0
        def make_houses(self, info):

            pop = info['user_info']['pop']
            people_per_house = 2
            construction_rate = 0.2 / (len(self.valid_positions) + 1)

            # Are there any valid positions
            if len(self.valid_positions) > 0:

                # Do we need more houses?
                if pop > len(self.houses) * people_per_house:

                    # Is it time to make a new house?
                    self.last_make += info['dt']
                    if self.last_make >= construction_rate:

                        # Make a house
                        index = random.randint(0, len(self.valid_positions) - 1)
                        pos = self.valid_positions[index]

                        self.houses.append(pos)
                        self.images.append(random.choice(self.house_imgs))
                        self.valid_positions.pop(index)

                        self.last_make = 0
                        

        def show(self, info):

            # name, img, rect, rotation            
            for index in range(len(self.houses)):
                pos = self.houses[index]
                img = self.images[index]

                # Scale img
                scaled_img = transform.scale(img, (int(info['window']['game_scale']), int(info['window']['game_scale'])))

                # Make value
                rect = pos[0] * info['window']['game_scale'], pos[1] * info['window']['game_scale'], info['window']['game_scale'], info['window']['game_scale']
                value = 'blit', scaled_img, rect, 0

                # Add value to show things
                extras.show_things.append(value)

    

