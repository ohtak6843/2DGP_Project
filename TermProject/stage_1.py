from pico2d import *
import game_framework
import game_world
import math
import tomllib
import pickle

import server
import define
import stage_2
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
            game_framework.push_mode(pass_mode)
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
            hole = Hole(0, 0, 0, 0)
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
        stage1_balls_list = tomllib.load(f)['stage1_balls']
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
    game_world.add_object(server.heart, 2)

    # score
    if not server.score:
        server.score = Score()
    game_world.add_object(server.score, 2)

    game_world.save()

    pass


def finish():
    game_world.clear()
    game_world.collision_pairs.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

    # 공 속도 0되면 스틱 다시 나오게
    if server.is_balls_stop() and server.white_ball.velo == 0 and server.section == True:
        server.stick.state_machine.handle_event(('ALL_STOP', 0))
        if server.HPstatus == 'ball_in':
            game_framework.push_mode(pass_mode)
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

    # 공 개수가 0이 되면 다음 스테이지로 넘어가기
    if len(server.balls) < 1:
        game_framework.change_mode(stage_2)
        game_framework.push_mode(pass_mode)


    # HP가 0이 되면 게임 종료
    if server.heart.HP == 0:
        game_framework.change_mode(result_mode)


def draw():
    clear_canvas()
    game_world.render()

    for w in server.walls:
        draw_rectangle(*w.get_bb())

    for h in server.holes:
        draw_rectangle(*h.get_bb())

    for o in game_world.objects[1]:
        draw_rectangle(*o.get_bb())

    update_canvas()


def pause():
    pass


def resume():
    pass
