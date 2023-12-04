from pico2d import *
from define import *

import game_framework
import game_world

import stage1
import stage2
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
    global image, bgm
    global wait_time

    if image == None:
        image = load_image('section/section-fail.png')
    if bgm == None:
        bgm = load_wav('section/sectionfail.mp3')
        bgm.set_volume(4)

    wait_time = get_time()
    bgm.play()

def finish():
    server.section = False

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