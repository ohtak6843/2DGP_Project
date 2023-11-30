from pico2d import *
import game_framework
import game_world
import math
import server
import define

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
        else:
            server.stick.handle_event(event)


def init():
    global table
    global stick
    global white_ball
    global balls
    global heart

    # table = Table()
    # game_world.add_object(table, 0)
    #
    # left_wall = Wall(70, 168, 150, 623, math.pi / 2)
    # game_world.add_object(left_wall, 0)
    # right_wall = Wall(1463, 168, 1545, 623, math.pi / 2)
    # game_world.add_object(right_wall, 0)
    # game_world.add_collision_pair('Wall:Ball', left_wall, None)
    # game_world.add_collision_pair('Wall:Ball', right_wall, None)
    #
    # top_left_wall = Wall(203, 663, 760, 728, 0)
    # game_world.add_object(top_left_wall, 0)
    # top_right_wall = Wall(852, 663, 1412,728, 0)
    # game_world.add_object(top_right_wall, 0)
    # bottom_left_wall = Wall(203, 63, 760, 128, 0)
    # game_world.add_object(bottom_left_wall, 0)
    # bottom_right_wall = Wall(852, 63, 1412,128, 0)
    # game_world.add_object(bottom_right_wall, 0)
    # game_world.add_collision_pair('Wall:Ball', top_left_wall, None)
    # game_world.add_collision_pair('Wall:Ball', top_right_wall, None)
    # game_world.add_collision_pair('Wall:Ball', bottom_left_wall, None)
    # game_world.add_collision_pair('Wall:Ball', bottom_right_wall, None)
    #
    #
    # holes = []
    # holes.append(Hole(135, 690, 60, 80))
    # holes.append(Hole(805, 700, 60, 60))
    # holes.append(Hole(1475, 690, 60, 80))
    # holes.append(Hole(135, 100, 60, 80))
    # holes.append(Hole(805, 90, 60, 60))
    # holes.append(Hole(1475, 100, 60, 80))
    # game_world.add_objects(holes, 0)
    # for h in holes:
    #     game_world.add_collision_pair('Hole:Ball', h, None)
    #
    #
    # white_ball = Ball(1000, 450, 3, 0)
    # game_world.add_object(white_ball, 1)
    # game_world.add_collision_pair('Wall:Ball', None, white_ball)
    # game_world.add_collision_pair('Hole:Ball', None, white_ball)
    #
    # stick = Stick(white_ball)
    # game_world.add_object(stick, 1)
    # game_world.add_collision_pair('Stick:Ball', stick, white_ball)
    # game_world.add_collision_pair('Ball:Ball', white_ball, white_ball)
    #
    # ball1 = Ball(400, 450, 0, 0)
    # ball2 = Ball(300, 350, 0, 1)
    # balls = []
    # balls.append(ball1)
    # balls.append(ball2)
    # game_world.add_objects(balls, 1)
    # for b in balls:
    #     game_world.add_collision_pair('Wall:Ball', None, b)
    #     game_world.add_collision_pair('Ball:Ball', b, b)
    # for b in balls:
    #     game_world.add_collision_pair('Hole:Ball', None, b)
    #
    # heart = Heart()
    # game_world.add_object(heart, 2)

    # table
    server.table = Table()
    game_world.add_object(server.table, 0)

    # walls
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
    server.holes.append(Hole(135, 690, 60, 80))
    server.holes.append(Hole(805, 700, 60, 60))
    server.holes.append(Hole(1475, 690, 60, 80))
    server.holes.append(Hole(135, 100, 60, 80))
    server.holes.append(Hole(805, 90, 60, 60))
    server.holes.append(Hole(1475, 100, 60, 80))
    game_world.add_objects(server.holes, 0)
    for h in server.holes:
        game_world.add_collision_pair('Hole:Ball', h, None)

    # white ball
    server.white_ball = Ball(1000, 450, 3, 0)
    game_world.add_object(server.white_ball, 1)
    game_world.add_collision_pair('Wall:Ball', None, server.white_ball)
    game_world.add_collision_pair('Hole:Ball', None, server.white_ball)
    game_world.add_collision_pair('Ball:Ball', server.white_ball, server.white_ball)

    # stick
    server.stick = Stick(server.white_ball)
    game_world.add_object(server.stick, 1)
    game_world.add_collision_pair('Stick:Ball', server.stick, server.white_ball)

    server.balls.append(Ball(400, 450, 0, 0))
    server.balls.append(Ball(300, 350, 0, 1))
    game_world.add_objects(server.balls, 1)
    for b in server.balls:
        game_world.add_collision_pair('Wall:Ball', None, b)
        game_world.add_collision_pair('Hole:Ball', None, b)
        game_world.add_collision_pair('Ball:Ball', b, b)

    # heart
    server.heart = Heart()
    game_world.add_object(server.heart, 2)

    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

    # 공 속도 0되면 스틱 다시 나오게
    server.check_balls_stop()

    # 공 개수가 0이 되면 다음 스테이지로 넘어가기


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
