table = None

walls = []

holes = []

stick = None

white_ball = None

balls = []

heart = None


def remove_ball(b):
    for i in range(len(balls)):
        if b == balls[i]:
            del balls[i]
            break


def is_balls_stop():
    for b in balls:
        if b.velo != 0:
            return False

    return True


def check_balls_stop():
    if is_balls_stop() and white_ball.velo == 0 and stick != None:
        stick.state_machine.handle_event(('ALL_STOP', 0))


def check_balls_void():
    if len(balls) == 0:
        return True
