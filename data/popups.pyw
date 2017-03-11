from pygame import *
import extras
all = {}

def update(info):
    global all

    # Show all popups
    y_val = 0
    for key, value in all.items():

        value.show(info, y_val)
        y_val += 1

    # Update all popups


class New:

    def __init__(self, id, img, name, options):

        self.id = id
        self.img = img
        self.options = options
        self.name = name


    def show(self, info, y):

        # Show image
        width = min(info['window']['in_use_size']) / 15
        margin = width

        pos = (margin, (y + 1) * margin)

        new_img = transform.scale(self.img, (int(width), int(width)))
        info['main_window'].blit(new_img, pos)

        # Does the name need to be shown?
        mouse_pos = mouse.get_pos()
        mouse_rect = mouse_pos[0], mouse_pos[1], 0, 0

        icon_rect = (pos[0], pos[1], width, width)

        if extras.touching(icon_rect, mouse_rect):
            info['mouse_over_popup'] = True

            # Show name
            extras.show_message(info, self.name, mouse_pos, width / 2, alpha = 150)

        else:
            info['mouse_over_popup'] = False


