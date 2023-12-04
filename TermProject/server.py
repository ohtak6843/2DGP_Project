import random

from table import Table
from stick import Stick
from ball import *
from heart import Heart
from wall import Wall
from hole import Hole
from score import Score

import stage1
import stage2

import pass_mode
import fail_mode

section = False

HPstatus = 'nothing_in'

table = None

walls = []

holes = []

white_ball = None

stick = None

balls = []

heart = None

score = None

background_music = None


def load_saved_world():
    global table, walls, holes, white_ball, stick, balls, heart, score

    table, walls, holes, white_ball, stick, balls, heart, score = None, [], [], None, None, [], None, None
    game_world.load()
    for o in game_world.all_objects():
        if isinstance(o, Table):
            table = o
        elif isinstance(o, Wall):
            walls.append(o)
        elif isinstance(o, Hole):
            holes.append(o)
        elif isinstance(o, Ball) and white_ball == None:
            white_ball = o
        elif isinstance(o, Stick):
            stick = o
            # stick.white_ball = white_ball
        elif isinstance(o, Ball) and white_ball != None:
            balls.append(o)
        elif isinstance(o, Heart):
            heart = o
        elif isinstance(o, Score):
            score = o


def remove_ball(b):
    for i in range(len(balls)):
        if b == balls[i]:
            del balls[i]
            break


def check_balls_void():
    if len(balls) == 0:
        return True


def is_balls_stop():
    for b in balls:
        if b.velo != 0:
            return False

    return True


def check_balls_stop():
    if server.is_balls_stop() and server.white_ball.velo == 0 and server.section == True:
        server.stick.state_machine.handle_event(('ALL_STOP', 0))
        if server.HPstatus == 'ball_in':
            # 공 개수가 0이 되면 다음 스테이지로 넘어가기
            if check_balls_void():
                game_framework.change_mode(stage2)
            else:
                game_framework.push_mode(pass_mode)
                server.heart.HPup(1)
        elif server.HPstatus == 'ball_in_red':
            game_framework.push_mode(fail_mode)
            server.load_saved_world()
            server.heart.HPdown(1)
            server.score.doubleS = Score.init_double
        elif server.HPstatus == 'nothing_in':
            game_framework.push_mode(fail_mode)
            server.heart.HPdown(1)
            server.score.doubleS = Score.init_double
        elif server.HPstatus == 'white_ball_in':
            game_framework.push_mode(fail_mode)
            server.load_saved_world()
            server.heart.HPdown(2)
            server.score.doubleS = Score.init_double

        game_world.save()
        server.HPstatus = 'nothing_in'
        server.stick.lineT = max(0, server.stick.lineT - 1)
        set_hole_state(random.randrange(0, 6), random.randrange(0, 6))


# HP가 0이 되면 게임 종료
def check_HP_is_zero():
    if server.heart.HP <= 0:
        game_framework.change_mode(result_mode)


def set_hole_state(a, b):
    for h in server.holes:
        h.state = 'Hole'
    server.holes[a].state = 'Plus'
    server.holes[b].state = 'Minus'
