from pico2d import *
from define import *

import game_framework
import stage_1


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(stage_1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            game_framework.change_mode(stage_1)

def init():
    global image

    image = load_image('title.jpg')

def finish():
    global image

    del image

def update():
    pass

def draw():
    global image

    clear_canvas()
    image.draw_to_origin(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    update_canvas()

def pause():
    pass


def resume():
    pass