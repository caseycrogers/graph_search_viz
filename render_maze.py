from maze import *
from renderer import *
from render_generic import *
from geometery_utils import distance
import numpy as np


def render_maze(maze):
    groups = _identify_groups(maze)
    edges = _groups_to_edges(groups)
    edges = _filter_edges(edges)
    print(maze)

    r = DebugRenderer()
    for e in edges:
        x, y = list(e)
        r.add_line(x, y)
    start_coord, finish_coord = to_coordinate(maze.start), to_coordinate(maze.finish)
    triangle = generate_start(start_coord)
    r.add_polygon(triangle)
    _render_nail_hole(r, (start_coord[0] + Config.square_size/6, start_coord[1]))
    _render_nail_hole(r, (start_coord[0] - Config.square_size/6, start_coord[1]))
    square = generate_finish(finish_coord)
    r.add_polygon(square)
    _render_nail_hole(r, (finish_coord[0] + Config.square_size/6, finish_coord[1]))
    _render_nail_hole(r, (finish_coord[0] - Config.square_size/6, finish_coord[1]))
    for g in groups:
        a, b = _two_furthest_points(g)
        _render_nail_hole(r, to_coordinate(a))
        _render_nail_hole(r, to_coordinate(b))
    r.finish("")


def _identify_groups(maze):
    def _flood_select(t):
        g = set()
        n = [t]
        while n:
            curr = n.pop()
            if curr in g:
                continue
            g.add(curr)
            n += maze.filtered_neighbors(curr, maze.is_wall)
        return g

    wall_groups = []
    visited = set()
    for y, row in enumerate(maze.array_2d):
        for x, tile in enumerate(row):
            t = (x, y)
            if t in visited:
                continue
            if maze.is_wall(t):
                group = _flood_select(t)
                visited = visited.union(group)
                wall_groups.append(group)

    return wall_groups


def _groups_to_edges(groups):
    def _tile_to_edges(t):
        x, y = to_coordinate(t)
        dist = Config.square_size / 2
        lr, ur, ul, ll = \
            (x + dist, y - dist), (x + dist, y + dist), (x - dist, y + dist), (x - dist, y - dist)
        return [frozenset([lr, ur]), frozenset([ur, ul]), frozenset([ul, ll]), frozenset([ll, lr])]
    edges = []
    for g in groups:
        for t in g:
            edges += _tile_to_edges(t)
    return edges


def _filter_edges(edges):
    return [e for e in edges if edges.count(e) == 1]


def _render_nail_hole(r, center):
    r.add_circle(center, Config.nail_hole_diameter)


def _two_furthest_points(g):
    best_dist = -1
    best = None
    for a in g:
        for b in g:
            dist = distance(np.array(a), np.array(b))
            if dist > best_dist:
                best = a, b
                best_dist = dist
    return best
