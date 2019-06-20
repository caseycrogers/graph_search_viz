from config import Config


def generate_start(center):
    x, y = center
    d = Config.square_size/3
    return [(x - d, y + d), (x - d, y - d), (x + d, y)]


def generate_finish(center):
    x, y = center
    d = Config.square_size/3
    return [(x + d, y - d), (x + d, y + d), (x - d, y + d), (x - d, y - d)]
