from pico2d import *


class Ball:
    image = None

    def __init__(self, x, y, image_x = 0, image_y = 0):
        self.x = x
        self.y = y

        self.image_x = image_x
        self.image_y = image_y

        if Ball.image == None:
            Ball.image = load_image('balls.png')

    def draw(self):
        Ball.image.clip_draw(self.image_x * 375, self.image_y * 375, 375, 375, self.x, self.y, 40, 40)  # 1/10 사이즈
        # draw_rectangle(self.x - 10, self.y - 10, self.x + 10, self.y + 10)

    def update(self):
        pass
