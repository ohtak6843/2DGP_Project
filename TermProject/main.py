from pico2d import *
import game_framework

import play_mode as start_mode


open_canvas(start_mode.WINDOW_WIDTH, start_mode.WINDOW_HEIGHT, sync=True)
game_framework.run(start_mode)
close_canvas()