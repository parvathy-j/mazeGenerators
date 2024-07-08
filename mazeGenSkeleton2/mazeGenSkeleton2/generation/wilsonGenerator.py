# -------------------------------------------------------------------
# Wilson's algorithm maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

import random
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator


class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson's algorithm maze generator.
    """

    def generateMaze(self, maze: Maze3D):
        """
        Generates a maze using Wilson's algorithm.
        """
        # Initialize all cells with walls
        maze.initCells(True)

        # Set of visited cells (finalised)
        visited = set()

        # Randomly select a starting cell and mark it as finalised
        startLevel = random.randint(0, maze.levelNum() - 1)
        startRow = random.randint(0, maze.rowNum(startLevel) - 1)
        startCol = random.randint(0, maze.colNum(startLevel) - 1)
        startCell = Coordinates3D(startLevel, startRow, startCol)
        visited.add(startCell)

        # While there are unvisited cells, keep generating the maze
        while len(visited) < self.countCells(maze):
            # Pick a random unvisited cell
            while True:
                level = random.randint(0, maze.levelNum() - 1)
                row = random.randint(0, maze.rowNum(level) - 1)
                col = random.randint(0, maze.colNum(level) - 1)
                current_cell = Coordinates3D(level, row, col)
                if current_cell not in visited:
                    break

            # Perform a random walk until a finalised cell is found
            path = [current_cell]
            while current_cell not in visited:
                neighbours = maze.neighbours(current_cell)
                # Filter valid neighbours
                valid_neighbours = [n for n in neighbours if self.isValid(n, maze)]
                if not valid_neighbours:
                    print(f"No valid neighbors for {current_cell}. Breaking out of the loop.")
                    break
                next_cell = random.choice(valid_neighbours)
                if next_cell in path:
                    # Remove loop by truncating the path
                    loop_index = path.index(next_cell)
                    path = path[:loop_index + 1]
                else:
                    path.append(next_cell)
                current_cell = next_cell

            # Carve the path and mark cells as visited
            for i in range(len(path) - 1):
                maze.removeWall(path[i], path[i + 1])
                visited.add(path[i])

            visited.add(path[-1])

        # Indicate that maze generation is complete
        self.m_mazeGenerated = True

    def isValid(self, coord: Coordinates3D, maze: Maze3D):
        """
        Check if the coordinates are within the bounds of the maze.

        Parameters:
        coord (Coordinates3D): The coordinates to check.
        maze (Maze3D): The maze being generated.

        Returns:
        bool: True if the coordinates are within bounds, False otherwise.
        """
        level = coord.getLevel()
        row = coord.getRow()
        col = coord.getCol()
        return (
                0 <= level < maze.levelNum() and
                0 <= row < maze.rowNum(level) and
                0 <= col < maze.colNum(level)
        )

    def countCells(self, maze: Maze3D):
        """
        Count the total number of cells in the maze.

        Parameters:
        maze (Maze3D): The maze being generated.

        Returns:
        int: The total number of cells in the maze.
        """
        total_cells = 0
        for level in range(maze.levelNum()):
            for row in range(maze.rowNum(level)):
                for col in range(maze.colNum(level)):
                    total_cells += 1
        return total_cells
