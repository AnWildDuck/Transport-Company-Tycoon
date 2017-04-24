from pygame import *
import time


class Handler:

        def __init__(self):
            self.houses = []
            self.images = []
            self.valid_positions = []
            self.house_img = [image.load('images//buildings//houses_1x1-1.png'),image.load('images//buildings//houses_1x1-2.png'),image.load('images//buildings//houses_1x1-3.png')]

        last_make = 0
        def make_houses(self, info):

            pop = info['user_info']['pop']
            people_per_house = 2
            construction_rate = 1 / (len(self.valid_positions) + 1)

            if len(self.valid_positions) > 0:

                if pop > len(self.houses) * people_per_house:

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

            for pos in self.houses:

                temp_house_img = random.choice(self.house_img)

                scaled_img = transform.scale(self.temp_house_img, (int(info['window']['game_scale']), int(info['window']['game_scale'])))

                new_pos = pos[0] * info['window']['game_scale'], pos[1] * info['window']['game_scale']

                info['game_window'].blit(scaled_img, new_pos)
