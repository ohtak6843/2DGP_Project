from math import sqrt

WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900


def normalize(vec_x, vec_y):
    size = sqrt(vec_x ** 2 + vec_y ** 2)
    normal_x, normal_y = vec_x / size, vec_y / size

    return normal_x, normal_y
    pass
