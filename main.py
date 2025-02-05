import os
import random
from canvas import Canvas
from grid import Grid
from tile_extractor import TileExtractor

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

if __name__ == "__main__":
    tiles = TileExtractor.extract(os.path.join(script_dir, "samples", "Water.png"))
    grid = Grid(10, 10, tiles)
    canvas = Canvas()
    canvas.render_color_grid(grid.get_color_grid())
    for _ in range(10 * 10):
        for i in range(100):
            row = random.randrange(0, 10)
            col = random.randrange(0, 10)
            if not grid.board[row][col].collapsed:
                grid.board[row][col].collapse()
                break
        canvas.render_color_grid(grid.get_color_grid())
    #index = random.randrange(0, len(tiles))
    #canvas.render_neighbour(tiles[index])
