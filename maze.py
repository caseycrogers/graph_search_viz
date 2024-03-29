from config import Config

_FLOOR = 0
_WALL = 1
_START = 2
_FINISH = 3


class Maze:
    @staticmethod
    def from_file(file):
        return Maze([[int(s) for s in l.replace('\n', '').split(' ')] for l in file.readlines()])

    def __init__(self, array_2d):
        pad = [1] * (2 + len(array_2d[0]))
        self.array_2d = [pad] + [[1] + row + [1] for row in array_2d] + [pad]
        for y, row in enumerate(self.array_2d):
            for x, tile in enumerate(row):
                if tile == _START:
                    self.start = x, y
                elif tile == _FINISH:
                    self.finish = x, y
        self.width, self.height = len(self.array_2d[0]), len(self.array_2d)

    def is_wall(self, t):
        x, y = t[0], t[1]
        return self.array_2d[y][x] == _WALL

    def is_freespace(self, t):
        x, y = t[0], t[1]
        return self.array_2d[y][x] != _WALL

    def is_legal(self, t):
        x, y = t[0], t[1]
        return 0 <= x < len(self.array_2d[0]) and 0 <= y < len(self.array_2d)

    def is_finish(self, t):
        x, y = t[0], t[1]
        return self.array_2d[y][x] == _FINISH

    def filtered_neighbors(self, t, cond):
        x, y = t[0], t[1]
        neighbors = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
        return list(filter(lambda t: self.is_legal(t) and cond(t), neighbors))

    def free_neighbors(self, t):
        return self.filtered_neighbors(t, self.is_freespace)

    def __str__(self):
        string = ''
        for row in self.array_2d:
            string += ' '.join([str(i) for i in row]) + '\n'
        return string


def _to_coordinate(t, x_offset, y_offset):
    x, y = t[0], t[1]
    return Config.square_size * x + x_offset, \
           Config.bed_height - Config.square_size * y + y_offset


def to_coordinate_center(t):
    return _to_coordinate(t, Config.square_size / 2, Config.square_size / 2)


def to_coordinate_ll(t):
    return _to_coordinate(t, 0, 0)


def to_coordinate_ur(t):
    return _to_coordinate(t, 0, Config.square_size)
