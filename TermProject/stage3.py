from pico2d import *
import game_framework
import game_world
import math
import tomllib
import pickle

import server
import define

import stage3_UI
import result_mode
import pass_mode
import fail_mode

from table import Table
from stick import Stick
from ball import Ball
from heart import Heart
from wall import Wall
from hole import Hole
from score import Score


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(result_mode)
        else:
            server.stick.handle_event(event)


def init():
    game_world.clear()
    game_world.collision_pairs.clear()

    # table
    server.table = Table()
    game_world.add_object(server.table, 0)

    # walls
    server.walls = []
    with open('init_data.toml', 'rb') as f:
        walls_data_list = tomllib.load(f)['walls']
        for w in walls_data_list:
            wall = Wall(0, 0, 0, 0, 0)
            wall.__dict__.update(w)
            server.walls.append(wall)
    game_world.add_objects(server.walls, 0)
    for w in server.walls:
        game_world.add_collision_pair('Wall:Ball', w, None);

    # holes
    server.holes = []
    with open('init_data.toml', 'rb') as f:
        holes_data_list = tomllib.load(f)['holes']
        for h in holes_data_list:
            hole = Hole(0, 0)
            hole.__dict__.update(h)
            server.holes.append(hole)
    game_world.add_objects(server.holes, 0)
    for h in server.holes:
        game_world.add_collision_pair('Hole:Ball', h, None)
        game_world.add_collision_pair('Hole:White_Ball', h, None)

    # white ball
    with open('init_data.toml', 'rb') as f:
        white_ball_data = tomllib.load(f)['white_ball']
        server.white_ball = Ball(0, 0, 0, 0)
        server.white_ball.__dict__.update(white_ball_data)
    game_world.add_object(server.white_ball, 1)
    game_world.add_collision_pair('Wall:Ball', None, server.white_ball)
    game_world.add_collision_pair('Hole:White_Ball', None, server.white_ball)
    game_world.add_collision_pair('Ball:Ball', server.white_ball, server.white_ball)

    # stick
    server.stick = Stick(server.white_ball)
    game_world.add_object(server.stick, 1)
    game_world.add_collision_pair('Stick:Ball', server.stick, server.white_ball)

    # balls
    server.balls = []
    with open('init_data.toml', 'rb') as f:
        stage1_balls_list = tomllib.load(f)['stage3_balls']
        for b in stage1_balls_list:
            ball = Ball(0, 0, 0, 0)
            ball.__dict__.update(b)
            server.balls.append(ball)
    game_world.add_objects(server.balls, 1)
    for b in server.balls:
        game_world.add_collision_pair('Wall:Ball', None, b)
        game_world.add_collision_pair('Hole:Ball', None, b)
        game_world.add_collision_pair('Ball:Ball', b, b)

    # heart
    if not server.heart:
        server.heart = Heart()
    server.heart.HP = 6
    game_world.add_object(server.heart, 2)

    # score
    if not server.score:
        server.score = Score()
    game_world.add_object(server.score, 2)

    game_world.save()

    game_framework.push_mode(stage3_UI)

    pass


def finish():
    game_world.clear()
    game_world.collision_pairs.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

    server.check_balls_stop(result_mode)
    server.check_HP_is_zero()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
