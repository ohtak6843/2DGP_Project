from pico2d import *
from define import *

import game_framework

import stage1
import title_mode

import server

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_mode()
            game_framework.change_mode(stage1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            game_framework.pop_mode()

def init():
    global image
    global font

    image = load_image('help.png')
    font = load_font('ENCR10B.TTF', 20)

def finish():
    pass

def update():
    pass

def draw():
    global image
    global font

    clear_canvas()
    image.draw_to_origin(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    font.draw(1350, 70, f'SPACE BAR : START', (0, 0, 0))
    font.draw(1350, 50, f'F1 : TITLE MODE', (0, 0, 0))
    update_canvas()

def pause():
    pass


def resume():
    pass