from table import Table
from stick import Stick
from ball import *
from heart import Heart
from wall import Wall
from hole import Hole
from score import Score

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


def is_balls_stop():
    for b in balls:
        if b.velo != 0:
            return False

    return True


def check_balls_stop():
    if is_balls_stop() and white_ball.velo == 0 and section is True:
        stick.state_machine.handle_event(('ALL_STOP', 0))


def check_balls_void():
    if len(balls) == 0:
        return True
