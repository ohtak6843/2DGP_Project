from pico2d import *


class Score:
    images = None
    width = 40
    height = 60

    init_double = 1

    def __init__(self, point = 0):
        self.point = point
        self.doubleS = Score.init_double
        self.plusScore = 100

        if Score.images == None:
            Score.images = [load_image('./score/score-' + '%d' % i + '@2x.png') for i in range(0, 10)]

    def draw(self):
        temp_s = self.point
        div = 0
        while True:
            if temp_s == 0 and div > 3: break
            temp_r = temp_s % 10
            temp_s = temp_s // 10
            Score.images[temp_r].draw(1500 - Score.width * div, 765, Score.width, Score.height)
            div += 1

    def update(self):
        pass
