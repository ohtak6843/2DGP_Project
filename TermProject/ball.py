from pico2d import *
from define import *
from math import cos, sin, atan2, pi, sqrt

from game_world import collide, remove_object


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

            my_velo_x = other_normalVelo_x
            my_velo_y = other_normalVelo_y
            my_velo = sqrt(my_velo_x ** 2 + my_velo_y ** 2)
            other_velo_x = my_normalVelo_x
            other_velo_y = my_normalVelo_y
            other_velo = sqrt(other_velo_x ** 2 + other_velo_y ** 2)

            my_verVelo_x, my_verVelo_y = my_normalVelo_x * my_velo, my_normalVelo_y * my_velo
            other_verVelo_x, other_verVelo_y = other_normalVelo_x * other_velo, other_normalVelo_y * other_velo

            my_Fvec_x, my_Fvec_y = my_tangentVelo_x + my_verVelo_x, my_tangentVelo_y + my_verVelo_y
            other_Fvec_x, other_Fvec_y = other_tangentVelo_x + other_verVelo_x, other_tangentVelo_y + other_verVelo_y

            self.degree = atan2(my_Fvec_y, my_Fvec_x)
            other.degree = atan2(other_Fvec_y, other_Fvec_x)

            self.velo = sqrt(my_Fvec_x ** 2 + my_Fvec_y ** 2)
            other.velo = sqrt(other_Fvec_x ** 2 + other_Fvec_y ** 2)

            print(other_normalVelo_x, other_normalVelo_y)

            remove_object(self)

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
