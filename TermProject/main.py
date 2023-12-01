from pico2d import *
import game_framework
import define

import title_mode as start_mode
import play_mode


open_canvas(define.WINDOW_WIDTH, define.WINDOW_HEIGHT, sync=True)
game_framework.run(start_mode)
close_canvas()