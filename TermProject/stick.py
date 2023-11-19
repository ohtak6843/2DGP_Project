from pico2d import *
from math import *


def m_left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT


def m_left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP and e[1].button == SDL_BUTTON_LEFT


def ball_collide(e):
    return e[0] == 'BALL_COLLIDE'


class Idle:
    @staticmethod
    def enter(stick, e):
        stick.r = 155
        pass

    @staticmethod
    def do(stick):
        pass

    @staticmethod
    def exit(stick, e):
        pass

    @staticmethod
    def draw(stick):
        dy = stick.center_y - stick.mouse_y
        dx = stick.center_x - stick.mouse_x
        stick.degree = atan2(dy, dx)
        Stick.image.composite_draw(stick.degree, '', stick.center_x + stick.r * cos(stick.degree),
                                   stick.center_y + stick.r * sin(stick.degree), 240, 240)  # 1/5 사이즈
        pass


class Pull:
    @staticmethod
    def enter(stick, e):
        stick.wait_time = get_time()
        pass

    @staticmethod
    def do(stick):
        if stick.r <= 185:
            stick.r += 1

        if get_time() - stick.wait_time >= 2:
            stick.r = 155
            stick.wait_time = get_time()
        pass

    @staticmethod
    def exit(stick, e):
        pass

    @staticmethod
    def draw(stick):
        dy = stick.center_y - stick.mouse_y
        dx = stick.center_x - stick.mouse_x
        stick.degree = atan2(dy, dx)
        Stick.image.composite_draw(stick.degree, '', stick.center_x + stick.r * cos(stick.degree),
                                   stick.center_y + stick.r * sin(stick.degree), 240, 240)  # 1/5 사이즈


class Push:
    @staticmethod
    def enter(stick, e):
        pass

    @staticmethod
    def do(stick):
        stick.r -= 1
        if stick.r < 135:
            stick.state_machine.handle_event(('BALL_COLLIDE', 0))
        pass

    @staticmethod
    def exit(stick, e):
        pass

    @staticmethod
    def draw(stick):
        dy = stick.center_y - stick.mouse_y
        dx = stick.center_x - stick.mouse_x
        stick.degree = atan2(dy, dx)
        Stick.image.composite_draw(stick.degree, '', stick.center_x + stick.r * cos(stick.degree),
                                   stick.center_y + stick.r * sin(stick.degree), 240, 240)  # 1/5 사이즈


class Hide:
    @staticmethod
    def enter(stick, e):
        pass

    @staticmethod
    def do(stick):
        pass

    @staticmethod
    def exit(stick, e):
        pass

    @staticmethod
    def draw(self):
        pass


class stateMachine:
    def __init__(self, stick):
        self.stick = stick
        self.cur_state = Idle
        self.transitions = {
            Idle: {m_left_down: Pull},
            Pull: {m_left_up: Push},
            Push: {ball_collide: Hide},
            Hide: {}
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

    def __init__(self, center_x, center_y):
        self.r = 155
        self.center_x = center_x
        self.center_y = center_y
        self.mouse_x = 0
        self.mouse_y = 0
        self.degree = 0

        self.state_machine = stateMachine(self)
        self.state_machine.start()

        if Stick.image == None:
            Stick.image = load_image('Stick.png')

    def draw(self):
        self.state_machine.draw()
        pass

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, e):
        self.state_machine.handle_event(('INPUT', e))
        if self.state_machine.cur_state == Idle:
            if e.type == SDL_MOUSEMOTION:
                self.mouse_x, self.mouse_y = e.x, 900 - 1 - e.y
        pass
