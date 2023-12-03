from pico2d import *


class Score:
    images = None

    init_double = 1

    def __init__(self, point = 0):
        self.point = point
        self.doubleS = Score.init_double
        self.plusScore = 100

        if Score.images == None:
            Score.images = [load_image('./score/score-' + '%d' % i + '@2x.png') for i in range(0, 10)]
            Score.font = load_font('ENCR10B.TTF', 30)

    def draw(self):
        Score.font.draw(1400, 760, f'{self.point}', (255, 255, 255))

    def update(self):
        pass
