from pico2d import *
from math import *

class Stick:
    image = None

    def __init__(self, center_x, center_y):
        self.r = 135
        self.center_x = center_x
        self.center_y = center_y
        self.mouse_x = 0
        self.mouse_y = 0

        if Stick.image == None:
            Stick.image = load_image('Stick.png')

    def draw(self):
        dy = self.center_y - self.mouse_y
        dx = self.center_x - self.mouse_x
        degree = atan2(dy, dx)
        Stick.image.composite_draw(degree, '', self.center_x + self.r * cos(degree), self.center_y + self.r * sin(degree), 240, 240)  # 1/5 사이즈
        pass

    def update(self):
        pass

    def handle_event(self, e):
        pass
