from pico2d import *
from math import *
from define import *

import game_world
import game_framework


def m_left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT


def m_left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP and e[1].button == SDL_BUTTON_LEFT


def ball_collide(e):
    return e[0] == 'BALL_COLLIDE'


def balls_all_stop(e):
    return e[0] == 'ALL_STOP'


INIT_R = PIXEL_PER_METER * 1  # 450픽셀, 1미터
PULL_MAX_R = PIXEL_PER_METER * 1.5  # 675픽셀, 1.5미터

PULL_SPEED_MPS = 0.5
PULL_SPEED_PPS = (PULL_SPEED_MPS * PIXEL_PER_METER)

PUSH_SPEED_MPS = 3.0
PUSH_SPEED_PPS = (PUSH_SPEED_MPS * PIXEL_PER_METER)

POWER_INCREASE_SPEED = 3
MAX_POWER_SPEED = 3


class Idle:
    @staticmethod
    def enter(stick, e):
        stick.r = INIT_R
        pass

    @staticmethod
    def do(stick):
        pass

    @staticmethod
    def exit(stick, e):
        pass

    @staticmethod
    def draw(stick):
        dy = stick.white_ball.y - stick.mouse_y
        dx = stick.white_ball.x - stick.mouse_x
        stick.degree = atan2(dy, dx)
        Stick.image.composite_draw(stick.degree, '', stick.white_ball.x + stick.r * cos(stick.degree),
                                   stick.white_ball.y + stick.r * sin(stick.degree), Stick.width,
                                   Stick.height)
        pass


class Pull:
    @staticmethod
    def enter(stick, e):
        stick.wait_time = get_time()
        pass

    @staticmethod
    def do(stick):
        stick.r += game_framework.frame_time * PULL_SPEED_PPS
        stick.power += game_framework.frame_time * POWER_INCREASE_SPEED
        if stick.r > PULL_MAX_R:
            stick.r = PULL_MAX_R
            stick.power = MAX_POWER_SPEED

        if get_time() - stick.wait_time >= 2:
            stick.r = INIT_R
            stick.wait_time = get_time()
        pass

    @staticmethod
    def exit(stick, e):
        pass

    @staticmethod
    def draw(stick):
        dy = stick.white_ball.y - stick.mouse_y
        dx = stick.white_ball.x - stick.mouse_x
        stick.degree = atan2(dy, dx)
        Stick.image.composite_draw(stick.degree, '', stick.white_ball.x + stick.r * cos(stick.degree),
                                   stick.white_ball.y + stick.r * sin(stick.degree), Stick.width,
                                   Stick.height)  # 1/5 사이즈


class Push:
    @staticmethod
    def enter(stick, e):
        pass

    @staticmethod
    def do(stick):
        stick.r -= game_framework.frame_time * PUSH_SPEED_PPS
        pass

    @staticmethod
    def exit(stick, e):
        pass

    @staticmethod
    def draw(stick):
        dy = stick.white_ball.y - stick.mouse_y
        dx = stick.white_ball.x - stick.mouse_x
        stick.degree = atan2(dy, dx)
        Stick.image.composite_draw(stick.degree, '', stick.white_ball.x + stick.r * cos(stick.degree),
                                   stick.white_ball.y + stick.r * sin(stick.degree), Stick.width,
                                   Stick.height)  # 1/5 사이즈


class Hide:
    @staticmethod
    def enter(stick, e):
        stick.r = INIT_R
        pass

    @staticmethod
    def do(stick):
        pass

    @staticmethod
    def exit(stick, e):
        pass

    @staticmethod
    def draw(stick):
        pass


class stateMachine:
    def __init__(self, stick):
        self.stick = stick
        self.cur_state = Idle
        self.transitions = {
            Idle: {m_left_down: Pull},
            Pull: {m_left_up: Push},
            Push: {ball_collide: Hide},
            Hide: {balls_all_stop: Idle},
        }

    def start(self):
        self.cur_state.enter(self.stick, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.stick)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.stick, e)
                self.cur_state = next_state
                self.cur_state.enter(self.stick, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.stick)


class Stick:
    image = None

    width = PIXEL_PER_METER * 1.4
    height = PIXEL_PER_METER * 0.7

    def __init__(self, white_ball):
        self.r = INIT_R
        self.white_ball = white_ball
        self.mouse_x = 0
        self.mouse_y = 0
        self.degree = 0
        self.power = 0

        self.state_machine = stateMachine(self)
        self.state_machine.start()

        if Stick.image == None:
            Stick.image = load_image('Stick.png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def handle_event(self, e):
        self.state_machine.handle_event(('INPUT', e))
        if self.state_machine.cur_state is Idle or self.state_machine.cur_state is Pull:
            if e.type == SDL_MOUSEMOTION:
                self.mouse_x, self.mouse_y = e.x, WINDOW_HEIGHT - 1 - e.y

    def get_bb(self):
        left = self.white_ball.x + (self.r - Stick.width / 2) * cos(self.degree)
        bottom = self.white_ball.y + (self.r - Stick.width / 2) * sin(self.degree)
        right = self.white_ball.x + (self.r + Stick.width / 2) * cos(self.degree)
        top = self.white_ball.y + (self.r + Stick.width / 2) * sin(self.degree)

        if left > right:
            left, right = right, left
        if bottom > top:
            bottom, top = top, bottom

        return left, bottom, right, top

    def handle_collision(self, group, other):
        if group == 'Stick:Ball':
            self.state_machine.handle_event(('BALL_COLLIDE', 0))
            if self.state_machine == Idle:
                print(123123123)