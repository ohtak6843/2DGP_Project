from pico2d import *
import game_framework
import game_world

from table import Table
from stick import Stick
from ball import Ball
from heart import Heart

WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            stick.mouse_x, stick.mouse_y = event.x, WINDOW_HEIGHT - 1 - event.y
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

    white_ball = Ball(1000, 450, 3, 0)
    game_world.add_object(white_ball, 1)

    stick = Stick(white_ball.x, white_ball.y)
    game_world.add_object(stick, 1)

    Balls = Ball(400, 450, 0, 0)
    game_world.add_object(Balls, 1)

    heart = Heart()
    game_world.add_object(heart, 2)

    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # delay(0.1)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

