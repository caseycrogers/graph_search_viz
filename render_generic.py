from config import Config


def generate_rect(ll, width, height):
    x1, y1, x2, y2 = ll[0], ll[1], ll[0] + width, ll[1] + height
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def generate_start(center):
    x, y = center
    d = Config.square_size/3
    return [(x - d, y + d), (x - d, y - d), (x + d, y)]


def generate_finish(center):
    x, y = center
    d = Config.square_size/3
    return [(x + d, y - d), (x + d, y + d), (x - d, y + d), (x - d, y - d)]
