from cell import Cell
from direction_enum import Direction
from tile import Tile


class Grid:

    def __init__(self, width : int, height : int, initial_options : list[Tile]):
        self.board = [[Cell(initial_options) for _ in range(height)] for _ in range(width)]
        self.cells : list[Cell] = []
        self._add_neighbours()

    def get_color_grid(self) -> list[list[tuple[int]]]:
        color_grid = [[(0,0,0) for _ in range(len(self.board[0]))] for _ in range(len(self.board))]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                color_grid[i][j] = self.board[i][j].get_color()
        return color_grid
    
    def _add_neighbours(self) -> None:
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                source_cell = self.board[i][j]
                self.cells.append(source_cell)
                if j + 1 < len(self.board[i]):
                    source_cell.add_neighbour(self.board[i][j + 1], Direction.EAST)
                if i + 1 < len(self.board):
                    source_cell.add_neighbour(self.board[i + 1][j], Direction.SOUTH)
                if j - 1 >= 0:
                    source_cell.add_neighbour(self.board[i][j - 1], Direction.WEST)
                if i - 1 >= 0:
                    source_cell.add_neighbour(self.board[i - 1][j], Direction.NORTH)

    @property
    def get_cells(self) -> list[Cell]:
        return self.cells