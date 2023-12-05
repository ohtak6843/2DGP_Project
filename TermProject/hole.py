from pico2d import *

from define import *

class Hole:

    size = PIXEL_PER_METER * 0.1

    plus_image = None
    minus_image = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.state = 'Hole'

        if Hole.plus_image == None:
            Hole.plus_image = load_image('hole/yellow_hole.png')
            Hole.minus_image = load_image('hole/red_hole.png')


    def draw(self):
        if self.state == 'Plus':
            Hole.plus_image.draw(self.x, self.y, Hole.size, Hole.size)
        elif self.state == 'Minus':
            Hole.minus_image.draw(self.x, self.y, Hole.size, Hole.size)
        pass


    def update(self):
        pass

    def handle_collision(self, group, other):
        if group == 'Hole:Ball':
            pass


    def get_bb(self):
        return self.x - Hole.size / 2, self.y - Hole.size / 2, self.x + Hole.size / 2, self.y + Hole.size / 2


    def get_radius(self):
        return PIXEL_PER_METER * 0.11