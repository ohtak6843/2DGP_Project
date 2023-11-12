from pico2d import *


class Stick:
    image = None

    def __init__(self):
        if Stick.image == None:
            Stick.image = load_image('Heart.png')

    def draw(self):
        Stick.image.draw(500, 500, 240, 240)  # 1/5 사이즈

    def update(self):
        pass
