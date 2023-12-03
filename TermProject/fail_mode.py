from pico2d import *
from define import *

import game_framework
import stage_1
import stage_2
import server

image = None
bgm = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def init():
    global image
    global wait_time

    if image == None:
        image = load_image('section/section-fail.png')
    if bgm == None:
        pass
    wait_time = get_time()

def finish():
    global image


    server.section = False
    del image

def update():
    if get_time() - wait_time >= 2:
        game_framework.pop_mode()
    pass

def draw():
    global image

    clear_canvas()
    game_world.render()
    image.draw(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    update_canvas()

def pause():
    pass


def resume():
    pass