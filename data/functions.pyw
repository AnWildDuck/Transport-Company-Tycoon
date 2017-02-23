from pygame import *

class Popups:
    
    def __init__(self):
        self.left = []
        self.right = []

    def add_button(self, side, icon, id):
        if side == 'left': self.left.append(icon, id)
        elif side == 'right': self.right.append(icon, id)
        else: print('WARNING! Invalid side for button ' + id)

    def show_buttons(self, window, window_scale):

        window_rect = window.get_rect()
        window_size = window_rect.width, window_rect.height
        
        width = min(window_size) / 100
        margin = width / 2

        # Left side
        height_dif = window_scale[1] / (len(self.left) + 1)

        for index in range(len(self.left)):
            
            icon, id = self.left[index]
            y = height_dif * index - width / 2

            icon = transform.scale(icon, (int(width), int(width))) 
            window.blit(icon, (margin, y))






