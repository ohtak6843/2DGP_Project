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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(stage1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            game_framework.change_mode(stage1)

def init():
    global image
    global font

    image = load_image('title.png')
    font = load_font('ENCR10B.TTF', 60)
    server.background_music = load_music('background_music.mp3')
    server.background_music.set_volume(16)
    server.background_music.repeat_play()

def finish():
    pass

def update():
    pass

def draw():
    global image

    clear_canvas()
    image.draw_to_origin(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)\

    font.draw(900, 170, f'SPACE BAR : START', (0, 0, 0))
    font.draw(900, 100, f'F1 : HELP', (0, 0, 0))
    update_canvas()

def pause():
    pass


def resume():
    pass