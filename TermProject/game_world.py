from ball import Ball
from stick import Stick

objects = [[] for _ in range(4)]


# fill here

def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


# fill here


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()


# fill here
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


# 충돌의 세계
collision_pairs = {}  # { 'boy:ball' : [ [boy], [ball1, ball2, ball3, ... ] ]


def add_collision_pair(group, a=None, b=None):  # a와 b 사이에 충돌 검사가 필요하다는 점을 등록
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
    return None


def is_balls_stop():
    for layers in objects:
        for o in layers:
            if isinstance(o, Ball) and o.velo != 0:
                return False

    return True

def check_balls_stop():
    if is_balls_stop():
        for layers in objects:
            for o in layers:
                if isinstance(o, Stick):
                    o.state_machine.handle_event(('ALL_STOP', 0))