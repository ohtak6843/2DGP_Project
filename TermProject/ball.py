from pico2d import *
from math import cos, sin, atan2, pi

from game_world import collide


class Ball:
    image = None

    def __init__(self, x, y, image_x = 0, image_y = 0):
        self.x = x
        self.y = y

        self.image_x = image_x
        self.image_y = image_y

        self.velo = 0
        self.degree = 0

        if Ball.image == None:
            Ball.image = load_image('balls.png')

    def draw(self):
        Ball.image.clip_draw(self.image_x * 276, self.image_y * 276, 276, 276, self.x, self.y, 40, 40)  # 1/10 사이즈
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velo * cos(self.degree)
        self.y += self.velo * sin(self.degree)
        pass


    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20
        pass


    def handle_collision(self, group, other):
        if group == 'Ball:Ball' and self != other:
            print(f'collision : {group}')
            # 충돌 시 충돌 위치 재조정

            temp_velo = self.velo + other.velo
            while collide(self, other):
                self.x += temp_velo * cos(self.degree + math.pi)
                self.y += temp_velo * sin(self.degree + math.pi)
                
            # 각도 조정
            

            # 속도 조정
            self.velo = 5
            other.velo = 5

            pass
        elif group == 'Stick:Ball':
            self.degree = other.degree + math.pi
            self.velo = 10
            pass
        elif group == 'Wall:Ball':
            # 충돌 시 충돌 위치 재조정
            while collide(self, other):
                self.x += cos(self.degree + math.pi)
                self.y += sin(self.degree + math.pi)

            # 각도 조정
            in_degree = self.degree - other.degree
            out_degree = other.degree - in_degree

            self.degree = out_degree

            pass
        pass