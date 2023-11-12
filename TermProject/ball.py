from pico2d import *


class Ball:
    image = None

    def __init__(self, x, y, image_x = 0, image_y = 0):
        self.x = x
        self.y = y

        self.image_x = image_x
        self.image_y = image_y

        self.velo_x = 0
        self.velo_y = 0

        if Ball.image == None:
            Ball.image = load_image('balls.png')

    def draw(self):
        Ball.image.clip_draw(self.image_x * 375, self.image_y * 375, 375, 375, self.x, self.y, 40, 40)  # 1/10 사이즈
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.x -= self.velo_x
        self.y -= self.velo_y
        pass


    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15
        pass


    def handle_collision(self, group, other):
        if group == 'ball:ball':
            pass
        elif group == 'stick:ball':
            pass
        elif group == 'LR_wall:ball':
            self.velo_x = -self.velo_x
        elif group == 'TB_wall:ball':
            self.velo_y = -self.velo_y
        pass