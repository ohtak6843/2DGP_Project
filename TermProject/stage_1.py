from pico2d import *
import game_framework
import game_world
import math
import server
import define

import stage_2
import pass_mode

from table import Table
from stick import Stick
from ball import Ball
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.push_mode(pass_mode)
        else:
            server.stick.handle_event(event)


def init():
    global table
    global stick
    global white_ball
    global balls
    global heart

    # table
    server.table = Table()
    game_world.add_object(server.table, 0)

    # walls
    server.walls = []
    server.walls.append(Wall(70, 168, 150, 623, math.pi / 2))  # left wall
    server.walls.append(Wall(1463, 168, 1545, 623, math.pi / 2))  # right wall
    server.walls.append(Wall(203, 663, 760, 728, 0))  # top left wall
    server.walls.append(Wall(852, 663, 1412, 728, 0))  # top right wall
    server.walls.append(Wall(203, 63, 760, 128, 0))  # bottom left wall
    server.walls.append(Wall(852, 63, 1412, 128, 0))  # bottom right wall
    game_world.add_objects(server.walls, 0)
    for w in server.walls:
        game_world.add_collision_pair('Wall:Ball', w, None);

    # holes
    server.holes = []
    server.holes.append(Hole(135, 690, 60, 80))
    server.holes.append(Hole(805, 700, 60, 60))
    server.holes.append(Hole(1475, 690, 60, 80))
    server.holes.append(Hole(135, 100, 60, 80))
    server.holes.append(Hole(805, 90, 60, 60))
    server.holes.append(Hole(1475, 100, 60, 80))
    game_world.add_objects(server.holes, 0)
    for h in server.holes:
        game_world.add_collision_pair('Hole:Ball', h, None)
        game_world.add_collision_pair('Hole:White_Ball', h, None)

    # white ball
    server.white_ball = Ball(1200, 400, 3, 0)
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
    server.balls.append(Ball(500, 400, 0, 3))
    server.balls.append(Ball(460, 420, 1, 3))
    server.balls.append(Ball(460, 380, 2, 3))
    game_world.add_objects(server.balls, 1)
    for b in server.balls:
        game_world.add_collision_pair('Wall:Ball', None, b)
        game_world.add_collision_pair('Hole:Ball', None, b)
        game_world.add_collision_pair('Ball:Ball', b, b)

    # heart
    if not server.heart:
        server.heart = Heart()
    game_world.add_object(server.heart, 2)

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
        game_framework.push_mode(pass_mode)

    # 공 개수가 0이 되면 다음 스테이지로 넘어가기
    if len(server.balls) < 1:
        game_framework.push_mode(clear_mode)


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
