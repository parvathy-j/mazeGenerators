# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Prim's maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

import random
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator


class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator.
    """

    def generateMaze(self, maze: Maze3D):
        """
        Generates a maze using Prim's algorithm.
        """
        # Initialize all cells with walls
        maze.initCells(True)

        # Randomly select a starting point for the maze generation
        startLevel = random.randint(0, maze.levelNum() - 1)
        startRow = random.randint(0, maze.rowNum(startLevel) - 1)
        startCol = random.randint(0, maze.colNum(startLevel) - 1)
        startCell = Coordinates3D(startLevel, startRow, startCol)
        print(f"Starting at cell: {startCell}")

        # Set of visited cells
        visited = set([startCell])

        # List to hold walls that are potential passages
        walls = self.getNeighbourWalls(maze, startCell)
        print(f"Initial walls: {walls}")

        # Prim's algorithm to generate the maze
        while walls:
            # Select a random wall from the list
            wall = random.choice(walls)
            walls.remove(wall)

            # Unpack the wall tuple into two cells
            cell1, cell2 = wall

            # Check if the cell on the opposite side of the wall has not been visited
            if cell2 not in visited and self.isValid(cell2, maze):
                # Remove the wall to make a passage
                maze.removeWall(cell1, cell2)
                visited.add(cell2)
                # Add new walls from the newly visited cell to the list
                new_walls = self.getNeighbourWalls(maze, cell2)
                walls.extend([w for w in new_walls if w[1] not in visited])

        # Indicate that maze generation is complete
        self.m_mazeGenerated = True

    def getNeighbourWalls(self, maze: Maze3D, cell: Coordinates3D):
        """
        Get all the walls between the given cell and its neighbours.

        Parameters:
        maze (Maze3D): The maze being generated.
        cell (Coordinates3D): The current cell being processed.

        Returns:
        list: A list of tuples where each tuple contains a cell and its neighbour.
        """
        neighbours = maze.neighbours(cell)
        walls = [(cell, neighbour) for neighbour in neighbours if self.isValid(neighbour, maze)]
        return walls

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
