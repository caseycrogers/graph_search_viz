import argparse
import os
import re
from maze import Maze
from render_maze import render_maze
from search_algorithms import *
from render_path import render_path

supported_algorithms = {
    'BFS': bfs,
    'DFS': dfs,
    'GREEDY': greedy,
    'ASTAR': a_star,
}


def main(maze_file_str, algorithm_name, debug):
    m = re.search('([a-zA-Z\d]+)\.[a-zA-Z\d]+', maze_file_str)
    output_dir = 'output/{0}'.format(m.groups()[0])
    output = '{0}/{1}_{2}'.format(output_dir, m.groups()[0], algorithm_name)
    if not debug:
        os.mkdir(output_dir)
    maze_file = open(maze_file_str, "r")
    maze = Maze.from_file(maze_file)
    print(maze)

    render_maze(output, maze, debug)
    render_path(output, *supported_algorithms[algorithm_name](maze), debug)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create visualizations for graph search algorithms')
    parser.add_argument('maze_file', help='Relative path to the input maze')
    parser.add_argument('algorithm', choices=supported_algorithms.keys())
    parser.add_argument('--debug', action='store_true', help='Only render in matplotlib.')
    args = parser.parse_args()
    main(args.maze_file,
         args.algorithm,
         args.debug)
