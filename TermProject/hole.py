from pico2d import *

class Hole:
    def __init__(self, x, y):
        self.x, self.y = x, y


    def draw(self):
        draw_rectangle(*self.get_bb())
        pass


    def update(self):
        pass

    def handle_collision(self, group, other):
        if group == 'Hole:Ball':
            pass


    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10