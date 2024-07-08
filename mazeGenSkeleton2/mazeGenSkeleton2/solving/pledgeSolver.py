# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Pledge maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"
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
        self.turns = 0  # Track total angle

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        """
        Solves the maze using the Pledge algorithm starting from the entrance.
        """
        self.m_solved = False
        self.visited = set()
        self.m_cellsExplored = 0
        self.turns = 0
        self.m_entranceUsed = entrance  # Use the inherited attribute
        self.m_exitUsed = None

        self.solve(maze, entrance)

    def solve(self, maze: Maze3D, entrance: Coordinates3D):
        """
        Core logic for solving the maze using the Pledge algorithm.
        """
        current_cell = entrance
        self.visited.add(current_cell)
        self.m_cellsExplored += 1  # Increment explored cells
        path = [current_cell]

        while current_cell not in maze.getExits():
            print(f"Current cell: {current_cell}")
            next_cell = self.getNextCell(maze, current_cell, self.directions[self.preferred_direction_index])
            if next_cell:
                current_cell = next_cell
                self.visited.add(current_cell)
                self.m_cellsExplored += 1  # Increment explored cells
                path.append(current_cell)
                self.solverPathAppend(current_cell, False)
                # Check for exit at each step
                if current_cell in maze.getExits():
                    self.m_exitUsed = current_cell  # Set the exit point
                    self.solved(entrance, current_cell)
                    print("Maze solved.")
                    print(f"Path: {path}")
                    return
            else:
                next_cell = self.wallFollow(maze, current_cell)
                if next_cell:
                    current_cell = next_cell
                    self.visited.add(current_cell)
                    self.m_cellsExplored += 1  # Increment explored cells
                    path.append(current_cell)
                    self.solverPathAppend(current_cell, False)
                    # Check for exit at each step
                    if current_cell in maze.getExits():
                        self.m_exitUsed = current_cell  # Set the exit point
                        self.solved(entrance, current_cell)
                        print("Maze solved.")
                        print(f"Path: {path}")
                        return
                else:
                    print("Maze could not be solved.")
                    break  # Prevent infinite loop by breaking out if no valid moves

        if current_cell in maze.getExits():
            self.m_exitUsed = current_cell  # Set the exit point
            self.solved(entrance, current_cell)
            print("Maze solved.")
            print(f"Path: {path}")

    def getNextCell(self, maze: Maze3D, current_cell: Coordinates3D, direction: tuple):
        """
        Determine the next cell to move to based on the current direction.
        """
        level, row, col = current_cell.getLevel(), current_cell.getRow(), current_cell.getCol()
        dlevel, drow, dcol = direction
        next_cell = Coordinates3D(level + dlevel, row + drow, col + dcol)
        print(f"Trying to move from {current_cell} to {next_cell} in direction {direction}")
        if self.isValidMove(maze, current_cell, next_cell):
            return next_cell
        return None

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

    def wallFollow(self, maze: Maze3D, current_cell: Coordinates3D):
        """
        Follow the wall using the right-hand rule until the solver is free to move in the preferred direction.
        """
        # Order of checks: North, North-East, East, South, South-West, West
        directions = [
            (-1, 0, 0),  # North
            (-1, 1, 0),  # North-East (Up)
            (0, 1, 0),   # East
            (1, 0, 0),   # South
            (1, -1, 0),  # South-West (Down)
            (0, -1, 0)   # West
        ]

        for turn in range(1, len(directions) + 1):
            direction_index = (self.preferred_direction_index + turn) % len(directions)  # Right-hand rule
            dx, dy, dz = directions[direction_index]
            next_cell = Coordinates3D(
                current_cell.getLevel() + dz,
                current_cell.getRow() + dx,
                current_cell.getCol() + dy
            )

            print(f"Checking next cell: {next_cell}")

            if next_cell in self.visited:
                print(f"Cell {next_cell} is already visited.")
                self.updateAngle(directions[direction_index])
                continue

            if not self.isValidCoordinate(next_cell, maze):
                print(f"Cell {next_cell} is invalid.")
                self.updateAngle(directions[direction_index])
                continue

            if maze.hasWall(current_cell, next_cell):
                print(f"Wall exists between {current_cell} and {next_cell}.")
                self.updateAngle(directions[direction_index])
                continue

            # If all checks pass, move to the next cell
            self.preferred_direction_index = direction_index

            print(f"Moved to: {next_cell} with angle difference: {self.turns}")

            if self.turns == 0:
                print("Turn count balanced, resuming preferred direction.")
                # Continue in the initial direction
                self.preferred_direction_index = 0  # Reset to initial direction (East)

            return next_cell

        print("No valid moves found, returning None.")
        return None

    def updateAngle(self, direction: tuple):
        """
        Update the angle based on the direction change.
        """
        if direction in [(0, 1, 0), (0, -1, 0),(1, 0, 0),(-1, 0, 0)]:  # East or West
            self.turns += 1
        else:
            self.turns += 0.5
        print(f"Angle updated to {self.turns} due to direction change.")
