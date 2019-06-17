from solid.utils import *
from maze import *
import os


def render_path(p):
    path = None
    for i, t in enumerate(p):
        c = _render_tile(t, len(p) - i)
        if not path:
            path = c
        else:
            path += c
    scad_render_to_file(path, 'tmp.scad')
    os.system('/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD tmp.scad --autocenter --viewall')


def _render_tile(t, step):
    d = Config.square_size
    x, y= to_coordinate(t)[0] - d / 2, to_coordinate(t)[1] - d / 2
    return translate([x, y, 0])(
        scale([1, 1, step*Config.step_height/d])(
            cube(d)
        )
    )
