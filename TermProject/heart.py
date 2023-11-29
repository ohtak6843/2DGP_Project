from pico2d import *
from define import *


class Heart:
    image = None
    sizeX = 44
    sizeY = 40
    x = 40
    y = 760

    def __init__(self, HP = 6):
        self.HP = HP

        if Heart.image == None:
            Heart.image = load_image('Heart.png')

    def draw(self):
        for i in range(0, self.HP):
            Heart.image.draw(Heart.x + (Heart.sizeX + 10) * i, Heart.y, Heart.sizeX, Heart.sizeY)

    def update(self):
        pass
