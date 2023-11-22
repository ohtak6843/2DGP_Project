from pico2d import *


class Wall:

    def __init__(self, left, bottom, right, top, degree):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.degree = degree

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def update(self):
        pass

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top

    def handle_collision(self, group, other):
        pass
