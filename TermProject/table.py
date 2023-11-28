from pico2d import *


class Table:
    image = None

    def __init__(self, x=800, y=450, sizeX=1600, sizeY=800):
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        if self.image == None:
            self.image = load_image('Table.jpg')

    def draw(self):
        self.image.draw(self.x, self.y, self.sizeX, self.sizeY)

    def update(self):
        pass
