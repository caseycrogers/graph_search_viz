from maze import *
from renderer import *
from render_generic import *
from geometery_utils import distance
from collections import defaultdict
from solid.utils import offset_points
import numpy as np


def render_maze(output, maze, debug):
    _render_base(output, maze, debug)
    _render_walls(output, maze, debug)


def _render_base(output, maze, debug):
    r = DebugRenderer() if debug else DXFRenderer()
    for nail in _find_nail_points(maze):
        _render_nail_hole(r, nail)
    r.add_polygon(_find_border_points(maze))

    for nail in _find_nail_points(maze):
        _render_nail_hole(r, nail)

    r.finish(output + '_base.txt')


def _render_walls(output, maze, debug):
    r = DebugRenderer() if debug else DXFRenderer()
    free_groups = _identify_groups(maze, freespace=True)
    edge_groups = _groups_to_edge_groups(free_groups)
    polys = _edge_groups_to_polygons(edge_groups)
    for poly in polys:
        r.add_polygon(poly)

    start_coord, finish_coord = to_coordinate_center(maze.start), to_coordinate_center(maze.finish)
    triangle = generate_start(start_coord)
    r.add_polygon(triangle)
    square = generate_finish(finish_coord)
    r.add_polygon(square)

    for nail in _find_nail_points(maze):
        _render_nail_hole(r, nail)
    r.add_polygon(_find_border_points(maze))

    r.finish(output + '_walls.txt')


def _find_nail_points(maze):
    start_coord, finish_coord = to_coordinate_center(maze.start), to_coordinate_center(maze.finish)
    points = [(start_coord[0] + Config.square_size / 6, start_coord[1]),
              (start_coord[0] - Config.square_size / 6, start_coord[1]),
              (finish_coord[0] + Config.square_size / 6, finish_coord[1]),
              (finish_coord[0] - Config.square_size / 6, finish_coord[1])]
    wall_groups = _identify_groups(maze, freespace=False)
    for g in wall_groups:
        points.extend([to_coordinate_center(t) for t in _two_furthest_tiles(g)])
    return points


def _find_border_points(maze):
    return generate_rect(to_coordinate_ll((0, maze.height - 1)),
                         Config.square_size*maze.width,
                         Config.square_size*maze.height)


def _identify_groups(maze, freespace):
    cond = maze.is_freespace if freespace else maze.is_wall

    def _flood_select(t):
        g = set()
        n = [t]
        while n:
            curr = n.pop()
            if curr in g:
                continue
            g.add(curr)
            n += maze.filtered_neighbors(curr, cond)
        return g

    wall_groups = []
    visited = set()
    for y, row in enumerate(maze.array_2d):
        for x, tile in enumerate(row):
            t = (x, y)
            if t in visited:
                continue
            if cond(t):
                group = _flood_select(t)
                visited = visited.union(group)
                wall_groups.append(group)

    return wall_groups


def _groups_to_edge_groups(groups):
    def _tile_to_edges(t):
        a, b, c, d = generate_rect(to_coordinate_ll(t), Config.square_size, Config.square_size)
        return [frozenset([a, b]), frozenset([b, c]), frozenset([c, d]), frozenset([d, a])]
    edge_groups = []
    for g in groups:
        edge_group = []
        for t in g:
            edge_group.extend(_tile_to_edges(t))
        edge_groups.append(edge_group)
    return [[e for e in g if g.count(e) == 1] for g in edge_groups]


def _edge_groups_to_polygons(edge_groups):
    polys = []
    for g in edge_groups:
        point_to_edges = defaultdict(list)
        for e in g:
            a, b = e
            point_to_edges[a].append(e)
            point_to_edges[b].append(e)
        poly_group = []
        poly = []
        remaining = len(point_to_edges)
        while True:
            to_add = []
            if poly:
                to_add += [p for e in point_to_edges[poly[-1]] for p in e if p not in poly]
                poly += to_add
            if not to_add:
                if poly:
                    poly_group.append(
                        offset_points(_collapsed_poly(poly), Config.square_size/4,inside=poly_group)
                    )
                    remaining -= len(poly)
                if remaining == 0:
                    break
                curr = min(set(point_to_edges.keys()) - set(poly))
                poly = [curr, max([p for e in point_to_edges[curr] for p in e])]
        polys.extend(poly_group)
    return polys


def _collapsed_poly(poly):
    collapsed = []
    while True:
        i = 0
        while i <= len(poly) - 3:
            a, b, c = poly[i:i + 3]
            if _vert_or_horiz(a, b, c):
                i += 2
            else:
                i += 1
            collapsed.append(a)
        collapsed.extend(poly[-2:])
        if _vert_or_horiz(collapsed[-1], collapsed[0], collapsed[1]):
            collapsed = collapsed[1:]
        if _vert_or_horiz(collapsed[-2], collapsed[-1], collapsed[0]):
            collapsed = collapsed[:-1]
        if len(collapsed) == len(poly):
            return collapsed
        poly, collapsed = collapsed, []


def _vert_or_horiz(a, b, c):
    return a[0] == b[0] == c[0] or a[1] == b[1] == c[1]


def _render_nail_hole(r, center):
    r.add_circle(center, Config.nail_hole_diameter)
    return center


def _two_furthest_tiles(g):
    best_dist = -1
    best = None
    for a in g:
        for b in g:
            dist = distance(np.array(a), np.array(b))
            if dist > best_dist:
                best = a, b
                best_dist = dist
    return best
