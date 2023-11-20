from pico2d import *
import game_framework
import game_world
import math
import define

from table import Table
from stick import Stick
from ball import Ball
from heart import Heart
from wall import Wall

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            stick.handle_event(event)

def init():
    global table
    global stick
    global white_ball
    global balls
    global heart

    table = Table()
    game_world.add_object(table, 0)

    left_wall = Wall(70, 190, 150, 700)
    game_world.add_object(left_wall, 0)
    right_wall = Wall(1463, 190, 1545, 700)
    game_world.add_object(right_wall, 0)
    game_world.add_collision_pair('LR_wall:ball', left_wall, None)
    game_world.add_collision_pair('LR_wall:ball', right_wall, None)

    top_left_wall = Wall(203, 745, 760, 818)
    game_world.add_object(top_left_wall, 0)
    top_right_wall = Wall(852, 745, 1412,818)
    game_world.add_object(top_right_wall, 0)
    bottom_left_wall = Wall(203, 70, 760, 144)
    game_world.add_object(bottom_left_wall, 0)
    bottom_right_wall = Wall(852, 70, 1412,144)
    game_world.add_object(bottom_right_wall, 0)

    white_ball = Ball(1000, 450, 3, 0)
    game_world.add_object(white_ball, 1)
    game_world.add_collision_pair('LR_wall:ball', None, white_ball)

    stick = Stick(white_ball)
    game_world.add_object(stick, 1)

    Balls = Ball(400, 450, 0, 0)
    game_world.add_object(Balls, 1)

    # heart = Heart()
    # game_world.add_object(heart, 2)

    white_ball.velo = 10

    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    # delay(0.1)
    # if stick.r <= 135:
    #     game_framework.stack[0].white_ball.degree = math.pi + stick.degree
    #     game_framework.stack[0].white_ball.velo = 10



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

