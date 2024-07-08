# -------------------------------------------------------------------
# Wall following maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"
        # Define the possible directions in a cyclic order (clockwise)
        self.directions = [
            (-1, 0, 0),  # North
            (-1, 1, 0),  # North-East (Up)
            (0, 1, 0),   # East
            (1, 0, 0),   # South
            (1, -1, 0),  # South-West (Down)
            (0, -1, 0)   # West
        ]
        self.preferred_direction_index = 2  # Initially facing East

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        """
        Solves the maze using the wall-following algorithm starting from the entrance.
        """
        self.m_solved = False
        self.visited = set()
        self.m_cellsExplored = 0
        self.m_entranceUsed = entrance
        self.m_exitUsed = None
        self.solve(maze, entrance)

    def solve(self, maze: Maze3D, entrance: Coordinates3D):
        """
        Core logic for solving the maze using the wall-following algorithm.
        """
        current_cell = entrance
        self.visited.add(current_cell)
        self.m_cellsExplored += 1
        path = [current_cell]
        came_from = None

        while current_cell not in maze.getExits():
            print(f"Current cell: {current_cell}")
            next_cell, came_from = self.getNextCell(maze, current_cell, came_from)
            if next_cell:
                current_cell = next_cell
                self.visited.add(current_cell)
                self.m_cellsExplored += 1
                path.append(current_cell)
                self.solverPathAppend(current_cell, False)
                if current_cell in maze.getExits():
                    self.m_exitUsed = current_cell
                    self.solved(entrance, current_cell)
                    print("Maze solved.")
                    print(f"Path: {path}")
                    return
            else:
                print("No valid moves found, returning None.")
                break

        if current_cell in maze.getExits():
            self.m_exitUsed = current_cell
            self.solved(entrance, current_cell)
            print("Maze solved.")
            print(f"Path: {path}")

    def getNextCell(self, maze: Maze3D, current_cell: Coordinates3D, came_from: Coordinates3D):
        """
        Determine the next cell to move to based on the wall-following rule.
        """
        # Rotate the direction cycle so that the direction we came from is checked last
        came_from_direction = None
        if came_from:
            came_from_direction = (current_cell.getLevel() - came_from.getLevel(),
                                   current_cell.getRow() - came_from.getRow(),
                                   current_cell.getCol() - came_from.getCol())
        directions = self.directions[self.preferred_direction_index:] + self.directions[:self.preferred_direction_index]
        if came_from_direction in directions:
            directions.remove(came_from_direction)
            directions.append(came_from_direction)

        for direction in directions:
            next_cell = self.calculateNextCell(current_cell, direction)
            print(f"Trying to move from {current_cell} to {next_cell} in direction {direction}")
            if self.isValidMove(maze, current_cell, next_cell):
                if next_cell not in self.visited:
                    self.preferred_direction_index = self.directions.index(direction)
                    return next_cell, current_cell
        return None, came_from

    def calculateNextCell(self, current_cell: Coordinates3D, direction: tuple):
        """
        Calculate the coordinates of the next cell based on the current cell and direction.
        """
        level, row, col = current_cell.getLevel(), current_cell.getRow(), current_cell.getCol()
        dlevel, drow, dcol = direction
        return Coordinates3D(level + dlevel, row + drow, col + dcol)

    def isValidMove(self, maze: Maze3D, from_cell: Coordinates3D, to_cell: Coordinates3D):
        """
        Check if the move from one cell to another is valid.
        """
        return self.isValidCoordinate(to_cell, maze) and not maze.hasWall(from_cell, to_cell)

    def isValidCoordinate(self, cell: Coordinates3D, maze: Maze3D) -> bool:
        """
        Check if the coordinates are within the bounds of the maze.
        """
        level = cell.getLevel()
        row = cell.getRow()
        col = cell.getCol()
        valid = (
                0 <= level < maze.levelNum() and
                0 <= row < maze.rowNum(level) and
                0 <= col < maze.colNum(level)
        )
        print(f"Checking validity of {cell}: {valid}")
        return valid
