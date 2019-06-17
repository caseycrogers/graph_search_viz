import queue
from geometery_utils import distance
import numpy as np
from maze import *


def _search(maze, func):
    q = queue.PriorityQueue()
    q.put((func(0, maze.start), maze.start))
    search_path = []
    t_to_step = dict()
    while not q.empty():
        p, t = q.get()
        step = len(search_path)
        search_path.append(t)
        t_to_step[t] = step
        if maze.is_finish(t):
            return search_path

        for n in maze.filtered_neighbors(t, maze.is_freespace):
            if n not in search_path:
                q.put((func(step + 1, t), n))
    print("NO SOLUTION FOUND!!!!")


def bfs(maze):
    return _search(maze, lambda s, t: s)


def dfs(maze):
    return _search(maze, lambda s, t: -s)


def a_star(maze):
    return _search(maze, lambda s, t: -s - _dist_to_finish(maze, t))


def _dist_to_finish(maze, t):
    return distance(np.array(to_coordinate(t)), np.array(to_coordinate(maze.finish)))

