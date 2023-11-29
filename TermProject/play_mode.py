from pico2d import *
import game_framework
import game_world
import math
import define

from table import Table
from stick import Stick
from ball import Ball, is_ball_stop, is_balls_stop
from heart import Heart
from wall import Wall
from hole import Hole

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

    left_wall = Wall(70, 168, 150, 623, math.pi / 2)
    game_world.add_object(left_wall, 0)
    right_wall = Wall(1463, 168, 1545, 623, math.pi / 2)
    game_world.add_object(right_wall, 0)
    game_world.add_collision_pair('Wall:Ball', left_wall, None)
    game_world.add_collision_pair('Wall:Ball', right_wall, None)

    top_left_wall = Wall(203, 663, 760, 728, 0)
    game_world.add_object(top_left_wall, 0)
    top_right_wall = Wall(852, 663, 1412,728, 0)
    game_world.add_object(top_right_wall, 0)
    bottom_left_wall = Wall(203, 63, 760, 128, 0)
    game_world.add_object(bottom_left_wall, 0)
    bottom_right_wall = Wall(852, 63, 1412,128, 0)
    game_world.add_object(bottom_right_wall, 0)
    game_world.add_collision_pair('Wall:Ball', top_left_wall, None)
    game_world.add_collision_pair('Wall:Ball', top_right_wall, None)
    game_world.add_collision_pair('Wall:Ball', bottom_left_wall, None)
    game_world.add_collision_pair('Wall:Ball', bottom_right_wall, None)

    white_ball = Ball(1000, 450, 3, 0)
    game_world.add_object(white_ball, 1)
    game_world.add_collision_pair('Wall:Ball', None, white_ball)

    stick = Stick(white_ball)
    game_world.add_object(stick, 1)
    game_world.add_collision_pair('Stick:Ball', stick, white_ball)
    game_world.add_collision_pair('Ball:Ball', white_ball, white_ball)

    ball1 = Ball(400, 450, 0, 0)
    ball2 = Ball(300, 350, 0, 1)
    balls = []
    balls.append(ball1)
    balls.append(ball2)
    game_world.add_objects(balls, 1)
    for b in balls:
        game_world.add_collision_pair('Wall:Ball', None, b)
        game_world.add_collision_pair('Ball:Ball', b, b)

    heart = Heart()
    game_world.add_object(heart, 2)

    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

    # 공 속도 0되면 스틱 다시 나오게
    if is_ball_stop(white_ball) and is_balls_stop(balls):
        stick.state_machine.handle_event(('ALL_STOP', 0))



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

