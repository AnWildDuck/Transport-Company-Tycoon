from pygame import *
import extras
all = {}
width_factor = 15
mouse_wait = False

def update(info):
    global all

    # Show all popups
    for key, value in all.items():
        value.update(info)

    # Update all popups


def check_mouse(info):
    global all

    mouse_pos = mouse.get_pos()
    mouse_rect = mouse_pos[0], mouse_pos[1], 0, 0

    for key, value in all.items():
        for rect in value.rects:

            if extras.touching(mouse_rect, rect):
                return False
    return True


class New:

    def __init__(self, id, img, name, y, options):
        global width_factor

        self.id = id
        self.img = img
        self.options = options
        self.name = name
        self.width_factor = width_factor
        self.y = y

        self.path = []


    def update(self, info):
        self.rects = []
        self.display_option(info, 1)
        self.show(info)

    def show(self, info):

        # Show image
        width = min(info['window']['in_use_size']) / self.width_factor
        margin = width

        pos = (margin, (self.y + 1) * margin)

        new_img = transform.scale(self.img, (int(width), int(width)))
        info['main_window'].blit(new_img, pos)

        # Does the name need to be shown?
        mouse_pos = mouse.get_pos()
        mouse_rect = mouse_pos[0], mouse_pos[1], 0, 0

        icon_rect = (pos[0], pos[1], width, width)
        self.rects.append(icon_rect)

        if extras.touching(icon_rect, mouse_rect):

            # Show name
            extras.show_message(info, self.name, mouse_pos, width / 2, alpha = 150)

            if mouse.get_pressed()[0]:
                self.path = ['base']

        else:

            # Have any buttons been pressed?
            pressed = False
            for button in mouse.get_pressed():
                if button: pressed = True

            if pressed and check_mouse(info):
                self.path = []


    def display_option(self, info, layer):

        mouse_pos = mouse.get_pos()
        mouse_rect = mouse_pos[0], mouse_pos[1], 0, 0

        if len(self.path) == layer:
            width = min(info['window']['in_use_size']) / self.width_factor

            height = 0
            for name, value in self.options.items():

                height += 1

                if value['type'] == 'button':
                    if value['show_type'] == 'image':

                        img = transform.scale(value['image'], (int(width), int(width)))

                        y = (self.y + 1) * width * height + (width * 0.5) * (height - 1)
                        x = width * 2.2

                        info['main_window'].blit(img, (x, y))

                        img_rect = (x, y, width, width)
                        self.rects.append(img_rect)

                        if extras.touching(img_rect, mouse_rect):
                            extras.show_message(info, name, mouse_pos, width / 2, alpha = 150)


