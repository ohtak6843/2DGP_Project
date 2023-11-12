from pico2d import *
import game_framework

import play_mode as start_mode

WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900


open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT, sync=True)
game_framework.run(start_mode)
close_canvas()