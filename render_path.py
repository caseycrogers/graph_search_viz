from render_generic import *
from solid.utils import *
from maze import *
import os


def render_path(output, search_path, shortest_path, debug):
    path = None
    for i, t in enumerate(search_path):
        if t in shortest_path:
            p_num = shortest_path.index(t)
        else:
            p_num = None
        c = _render_tile(t, len(search_path) - i, p_num)
        if not path:
            path = c
        else:
            path += c
    path -= _render_start(shortest_path[0])
    path -= _render_finish(shortest_path[-1])
    scad_render_to_file(path, 'tmp.scad')
    render_cmd = '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD tmp.scad --autocenter --viewall'
    if not debug:
        render_cmd += ' -o ' + output + '.stl'
    os.system(render_cmd)


def _render_tile(t, step, p_num):
    d = Config.square_size
    x, y = to_coordinate_center(t)[0] - d / 2, to_coordinate_center(t)[1] - d / 2
    column = scale([d, d, step*Config.step_height])(
        cube(1)
    )
    if p_num is not None:
        column -= translate([d/4, d/4, step*Config.step_height - 2])(
            scale([d/2, d/2, 2])(
                cube(1)
            )
        )
    return translate([x, y, 0])(column)


def _render_start(start_tile):
    return linear_extrude(height=Config.mat_thickness + Config.t)(
        offset(delta=Config.t)(
            polygon(generate_start(to_coordinate_center(start_tile)))
        )
    )


def _render_finish(finish_tile):
    return linear_extrude(height=Config.mat_thickness + Config.t)(
        offset(delta=Config.t)(
            polygon(generate_finish(to_coordinate_center(finish_tile)))
        )
    )
