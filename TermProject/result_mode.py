from pico2d import *
from define import *

import game_framework
import stage1

import server


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F5:
            game_framework.change_mode(stage1)

def init():
    global image
    global font

    image = load_image('result.jpg')
    font = load_font('ENCR10B.TTF', 60)

def finish():
    pass

def update():
    pass

def draw():
    global image

    clear_canvas()
    image.draw_to_origin(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    font.draw(50, 200, f'Score', (0, 0, 0))
    font.draw(50, 100, f'{server.score.point}', (0, 0, 0))
    font.draw(1000, 200, f'F5 : REPLAY', (0, 0, 0))
    font.draw(1000, 100, f'ESC : QUIT', (0, 0, 0))

    update_canvas()

def pause():
    pass


def resume():
    pass