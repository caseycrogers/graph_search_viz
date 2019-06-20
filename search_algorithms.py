import queue
from geometery_utils import distance
import numpy as np
from abc import ABC, abstractmethod


class _SearchNode(ABC):
    def __init__(self, cost_so_far, came_from, tile):
        self.cost = cost_so_far
        self.came_from = came_from
        self.tile = tile
        super().__init__()

    @abstractmethod
    def priority_score(self):
        pass

    def __lt__(self, other):
        return self.priority_score() < other.priority_score()


def _search(maze, node_class):
    q = queue.PriorityQueue()
    q.put(node_class(0, None, maze.start))
    visited = []
    while not q.empty():
        node = q.get()
        if node.tile in visited:
            continue
        visited.append(node.tile)
        if maze.is_finish(node.tile):
            return visited, _create_shortest_path(node)
        for t in maze.free_neighbors(node.tile):
            q.put(node_class(node.cost + 1, node, t))
    print("NO SOLUTION FOUND!!!!")


def _create_shortest_path(last_node):
    p = []
    while last_node is not None:
        p.append(last_node.tile)
        last_node = last_node.came_from
    return p[::-1]


def bfs(maze):
    class BFSNode(_SearchNode):
        def priority_score(self):
            return self.cost
    return _search(maze, BFSNode)


def dfs(maze):
    class DFSNode(_SearchNode):
        a = 0

        def priority_score(self):
            self.a += 1
            return self.a
    return _search(maze, DFSNode)


def greedy(maze):
    class GreedyNode(_SearchNode):
        def priority_score(self):
            return _dist_to_finish(maze, self.tile)
    return _search(maze, GreedyNode)


def a_star(maze):
    class AStarNode(_SearchNode):
        def priority_score(self):
            return self.cost + _dist_to_finish(maze, self.tile)
    return _search(maze, AStarNode)


def _dist_to_finish(maze, t):
    return distance(np.array(t), np.array(maze.finish))

