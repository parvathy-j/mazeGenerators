# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Prim's maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------
from collections import deque
from queue import PriorityQueue
from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation using A* algorithm.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "taskC"

    def solveMaze(self, maze: Maze3D):
        self.solveMazeTaskC(maze)

    def solveMazeTaskC(self, maze: Maze3D):
        """
        Solve the maze, used by Task C.
        This version of solveMaze does not provide a starting entrance, and as part of the solution, the method should
        find the entrance and exit pair (see project specs for requirements of this task).
        """
        min_cost = float('inf')
        best_pair = (None, None)

        entrances = maze.getEntrances()
        num_exits = len(maze.getExits())  # Get the number of exits, but not their locations

        for entrance in entrances:
            local_paths, local_cells_explored = self.explore_with_dfs(maze, entrance, num_exits)
            for exit_cell, path in local_paths.items():
                path_length = len(path) - 1
                cost = local_cells_explored + path_length
                if cost < min_cost and entrance != exit_cell:
                    min_cost = cost
                    best_pair = (entrance, exit_cell)

        if best_pair[0] and best_pair[1]:
            self.m_cellsExplored = min_cost
            self.m_entranceUsed = best_pair[0]
            self.m_exitUsed = best_pair[1]
            print(f"Best pair: Entrance at {best_pair[0]}, Exit at {best_pair[1]} with cost {min_cost}")
            self.trace_path(maze, best_pair[0], best_pair[1])

    def explore_with_dfs(self, maze: Maze3D, entrance: Coordinates3D, num_exits: int):
        stack = [(entrance, [entrance])]
        visited = set()
        visited.add(entrance)
        local_paths = {}
        cells_explored = 0

        while stack and len(local_paths) < num_exits:
            current_cell, path = stack.pop()
            cells_explored += 1

            if self.is_potential_exit(maze, current_cell, entrance) and current_cell not in local_paths:
                local_paths[current_cell] = path

            for neighbor in maze.neighbours(current_cell):
                if neighbor not in visited and not maze.hasWall(current_cell, neighbor):
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        return local_paths, cells_explored

    def a_star_path(self, maze: Maze3D, start: Coordinates3D, end: Coordinates3D):
        pq = PriorityQueue()
        pq.put((0, start))
        came_from = {}
        cost_so_far = {start: 0}
        came_from[start] = None

        while not pq.empty():
            _, current = pq.get()

            if current == end:
                break

            for neighbor in maze.neighbours(current):
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, end)  # Heuristic calculation
                    pq.put((priority, neighbor))
                    came_from[neighbor] = current

        return self.reconstruct_path(came_from, start, end)  # Path is reconstructed from entrance to exit utilizing the shortest distance found

    def heuristic(self, cell: Coordinates3D, entrance: Coordinates3D):
        # Manhattan distance as the heuristic:the sum of absolute differences between points across all the dimensions.
        return abs(cell.getLevel() - entrance.getLevel()) + abs(cell.getRow() - entrance.getRow()) + abs(cell.getCol() - entrance.getCol())

    def is_potential_exit(self, maze: Maze3D, cell: Coordinates3D, entrance: Coordinates3D):
        """
        Simulate checking if the cell is an exit based on heuristic rules.
        For example, assume an exit is located at the outer boundary of the maze.
        Ensure the entrance is not considered as an exit.
        """
        if cell == entrance:
            return False

        level, row, col = cell.getLevel(), cell.getRow(), cell.getCol()
        if row == -1 or col == -1 or row == maze.rowNum(level) or col == maze.colNum(level):
            print(f"Potential exit: {cell}")
            return True
        return False

    def trace_path(self, maze: Maze3D, start: Coordinates3D, end: Coordinates3D):
        path = self.a_star_path(maze, start, end)
        for cell in path:
            self.solverPathAppend(cell, False)
        return path

    def reconstruct_path(self, came_from, start, end):
        current = end
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
