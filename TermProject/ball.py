from pico2d import *
from define import *
from math import cos, sin, atan2, pi

from game_world import collide


class Ball:
    image = None

    def __init__(self, x, y, image_x=0, image_y=0):
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
        if self != other: print(f'collision : {group}')
        if group == 'Ball:Ball' and self != other:
            if not collide(self, other): return

            # 충돌 시 충돌 위치 재조정
            while collide(self, other):
                self.x += self.velo * cos(self.degree + math.pi)
                self.y += self.velo * sin(self.degree + math.pi)
                other.x += other.velo * cos(other.degree + math.pi)
                other.y += other.velo * sin(other.degree + math.pi)

            # 각도 및 속도 조정
            dy = other.y - self.y
            dx = other.x - self.x

            temp = normalize(dy, dx)
            my_normal_x, my_normal_y = temp[0], temp[1]
            other_normal_x, other_normal_y = -temp[0], -temp[1]

            my_normalVelo_size = self.velo * cos(self.degree) * my_normal_x + self.velo * sin(self.degree) * my_normal_y
            other_normalVelo_size = other.velo * cos(other.degree) * other_normal_x + other.velo * sin(other.degree) * other_normal_y

            my_normalVelo_x = my_normalVelo_size * my_normal_x
            my_normalVelo_y = my_normalVelo_size * my_normal_y
            other_normalVelo_x = other_normalVelo_size * other_normal_x
            other_normalVelo_y = other_normalVelo_size * other_normal_y

            my_tangentVelo_x = self.velo * cos(self.degree) - my_normalVelo_x
            my_tangentVelo_y = self.velo * sin(self.degree) - my_normalVelo_y
            other_tangentVelo_x = other.velo * cos(other.degree) - other_normalVelo_x
            other_tangentVelo_y = other.velo * sin(other.degree) - other_normalVelo_y

            

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
