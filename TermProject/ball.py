from pico2d import *
from define import *
from math import cos, sin, atan2, pi, sqrt

import game_world
import game_framework
import server

FRICTION_SPEED_MPS = 0.6
FRICTION_SPEED_PPS = FRICTION_SPEED_MPS * PIXEL_PER_METER


class Ball:
    image = None
    ball_ball_sound = None

    size = PIXEL_PER_METER * 0.08

    def __init__(self, x, y, image_x=0, image_y=0):
        self.x = x
        self.y = y

        self.image_x = image_x
        self.image_y = image_y

        self.velo = 0
        self.degree = 0

        self.hide = False

        if Ball.image == None:
            Ball.image = load_image('Balls.png')
            Ball.ball_ball_sound = load_wav('sound/ball_ball_collide.wav')
            Ball.ball_ball_sound.set_volume(16)

    def draw(self):
        if self.hide == False:
            Ball.image.clip_draw(self.image_x * 276, self.image_y * 276, 276, 276, self.x, self.y, Ball.size, Ball.size)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.x += game_framework.frame_time * (self.velo * PIXEL_PER_METER) * cos(self.degree)
        self.y += game_framework.frame_time * (self.velo * PIXEL_PER_METER) * sin(self.degree)

        self.velo -= game_framework.frame_time * FRICTION_SPEED_MPS
        if self.velo < 0: self.velo = 0

    def get_bb(self):
        return self.x - Ball.size / 2, self.y - Ball.size / 2, self.x + Ball.size / 2, self.y + Ball.size / 2

    def handle_collision(self, group, other):
        if self != other: print(f'collision : {group}')
        if group == 'Ball:Ball' and self != other:
            if not game_world.collide(self, other): return

            Ball.ball_ball_sound.play()

            # 각도 및 속도 조정
            dy = other.y - self.y
            dx = other.x - self.x

            temp = normalize(dx, dy)
            self_normalize_Nx, self_normalize_Ny = temp[0], temp[1]
            other_normalize_Nx, other_normalize_Ny = -temp[0], -temp[1]

            self_degree = atan2(self_normalize_Ny, self_normalize_Nx)
            other_degree = atan2(other_normalize_Ny, other_normalize_Nx)

            # 충돌 시 충돌 위치 재조정
            while game_world.collide(self, other):
                self.x += cos(self_degree + math.pi)
                self.y += sin(self_degree + math.pi)
                other.x += cos(other_degree + math.pi)
                other.y += sin(other_degree + math.pi)

            self_N_size = self.velo * cos(self.degree) * self_normalize_Nx + self.velo * sin(
                self.degree) * self_normalize_Ny
            other_N_size = other.velo * cos(other.degree) * other_normalize_Nx + other.velo * sin(
                other.degree) * other_normalize_Ny

            self_Nx = self_N_size * self_normalize_Nx
            self_Ny = self_N_size * self_normalize_Ny
            other_Nx = other_N_size * other_normalize_Nx
            other_Ny = other_N_size * other_normalize_Ny

            self_Tx = self.velo * cos(self.degree) - self_Nx
            self_Ty = self.velo * sin(self.degree) - self_Ny
            other_Tx = other.velo * cos(other.degree) - other_Nx
            other_Ty = other.velo * sin(other.degree) - other_Ny

            self_after_N_size = sqrt(other_Nx ** 2 + other_Ny ** 2)
            other_after_N_size = sqrt(self_Nx ** 2 + self_Ny ** 2)

            self_after_Nx, self_after_Ny = other_normalize_Nx * self_after_N_size, other_normalize_Ny * self_after_N_size
            other_after_Nx, other_after_Ny = self_normalize_Nx * other_after_N_size, self_normalize_Ny * other_after_N_size

            self_Fx, self_Fy = self_Tx + self_after_Nx, self_Ty + self_after_Ny
            other_Fx, other_Fy = other_Tx + other_after_Nx, other_Ty + other_after_Ny

            self.degree = atan2(self_Fy, self_Fx)
            other.degree = atan2(other_Fy, other_Fx)

            self.velo = sqrt(self_Fx ** 2 + self_Fy ** 2)
            other.velo = sqrt(other_Fx ** 2 + other_Fy ** 2)

            print(self.velo * cos(self.degree) + other.velo * cos(self.degree))
            print(self.velo * sin(self.degree) + other.velo * sin(self.degree))

        elif group == 'Stick:Ball':
            self.degree = other.degree + math.pi
            self.velo = other.power

            other.power = 0
            server.section = True
        elif group == 'Wall:Ball':
            Ball.ball_ball_sound.play()

            # 충돌 시 충돌 위치 재조정
            while game_world.collide(self, other):
                self.x += cos(self.degree + math.pi)
                self.y += sin(self.degree + math.pi)

            # 각도 조정
            in_degree = self.degree - other.degree
            out_degree = other.degree - in_degree

            self.degree = out_degree
        elif group == 'Hole:White_Ball':
            server.HPstatus = 'white_ball_in'
            self.velo = 0
            self.hide = True
            game_world.remove_object(self)
        elif group == 'Hole:Ball':
            if server.HPstatus == 'nothing_in':
                server.HPstatus = 'ball_in'
            if other.state == 'Minus':
                server.HPstatus = 'ball_in_red'
            if other.state == 'Plus':
                server.stick.lineT += 3
            server.score.point += server.score.doubleS * server.score.plusScore
            server.score.doubleS += 1
            game_world.remove_object(self)
            server.remove_ball(self)
