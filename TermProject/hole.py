from pico2d import *

from define import *

class Hole:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height


    def draw(self):
        draw_rectangle(*self.get_bb())
        pass


    def update(self):
        pass

    def handle_collision(self, group, other):
        if group == 'Hole:Ball':
            pass


    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2