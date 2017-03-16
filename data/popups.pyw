from pygame import *
import extras, mouse_extras

all = {}
all_rects = []
width_factor = 15
mouse_wait = False

def update(info):
    global all, all_rects
    all_rects = []    

    # Update all popups
    for key, value in all.items():
        rects = value.update(info)
        for rect in rects: all_rects.append(rect)


def check_mouse(info):
    global all, all_rects

    mouse_pos = mouse.get_pos()
    mouse_rect = (mouse_pos[0], mouse_pos[1], 0, 0)

    for rect in all_rects:
        if extras.touching(mouse_rect, rect):
            return False
    return True

class New:

    def __init__(self, id, img, name, layer, y, options, base = False):
        global width_factor

        self.id = id
        self.img = img
        self.options = options
        self.name = name
        self.width_factor = width_factor
        self.y = y
        self.layer = layer
        self.clicked = False
        self.last_click = False
        self.base = base


    def show_icon(self, info, img, pos, size):

        img = transform.scale(img, (int(size), int(size)))
        #info['main_window'].blit(img, pos)
        extras.blit_alpha(info['main_window'], img, pos, 230)

    def stop_all(self):
        for id, option in self.options:
            if id == 'popup':
                option.stop_all()
        self.clicked = False

    def turn_off(self, rects):
        if self.base:

            # Has the mouse been clicked?
            if mouse_extras.get_states()[0] == -1:

                mouse_pos = mouse.get_pos()
                mouse_rect = (mouse_pos[0], mouse_pos[1], 0, 0)

                # Is the mouse off the options
                okay = True
                for rect in rects:
                    if extras.touching(rect, mouse_rect):
                        okay = False
                        break

                if okay:
                    self.stop_all()


    def update(self, info, reset = False):
        rects = self.update_self(info, reset = reset)
        self.turn_off(rects)
        return rects


    def update_self(self, info, reset = False):

        just_clicked = int(self.clicked) - int(self.last_click)
        # if reset: self.clicked = False
        self.items = []

        width = min(info['window']['in_use_size']) / 10
        margin = width

        mouse_pos = mouse.get_pos()
        mouse_rect = (mouse_pos[0], mouse_pos[1], 0, 0)

        x = margin * (self.layer * 1.5 + 1)
        y = margin * (self.y * 1.5 + 1)

        # Show
        self.show_icon(info, self.img, (x, y), width)

        rect = (x, y, width, width)
        obj = self

        self.items.append((rect, obj))
        orects = []

        # Show options
        if self.clicked:
            for id, option in self.options:

                # Popup options
                if id == 'popup':
                    values = option.update(info, reset = (just_clicked == 1))

                    for value in values:
                        orects.append(value)

        # Show message
        for rect, obj in self.items:

            # Is the mouse over the rect
            if extras.touching(mouse_rect, rect):

                # Show message
                extras.show_message(info, obj.name, mouse_pos, width / 2, colour = (0, 0, 0), backround = (255, 255, 255), margin = 0.2, alpha = 180)

                # Is the icon clicked?
                if mouse_extras.get_states()[0] == -1:

                    # Unclick
                    if self.clicked == True:
                        self.stop_all()

                    self.clicked = True

        rects = []
        for rect, obj in self.items: rects.append(rect)
        for i in orects: rects.append(i)
        return rects
            