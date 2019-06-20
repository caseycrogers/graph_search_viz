import argparse
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


def main(maze_file_str, algorithm, debug):
    maze_file = open(maze_file_str, "r")
    maze = Maze.from_file(maze_file)

    render_maze(maze)
    render_path(*algorithm(maze))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create visualizations for graph search algorithms')
    parser.add_argument('maze_file', help='Relative path to the input maze')
    parser.add_argument('algorithm', choices=supported_algorithms.keys())
    parser.add_argument('--debug', action='store_true', help='Only render in matplotlib.')
    args = parser.parse_args()
    main(args.maze_file,
         supported_algorithms[args.algorithm],
         args.debug)
