from pico2d import *


class Heart:
    image = None
    sizeX = 66
    sizeY = 60
    x = 66
    y = 700

    def __init__(self, HP = 6):
        self.HP = HP

        if Heart.image == None:
            Heart.image = load_image('Heart.png')

    def draw(self):
        for i in range(0, self.HP):
            Heart.image.draw(self.x + self.sizeX * i, self.y, self.sizeX, self.sizeY)

    def update(self):
        pass
