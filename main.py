import os
import random
import time
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
    while not grid.collapse_random():
        canvas.render_color_grid(grid.get_color_grid())
        canvas.window.after(1000)
    # for _ in range(3 * 3):
    #     for i in range(9):
    #         row = random.randrange(0, 3)
    #         col = random.randrange(0, 3)
    #         if not grid.board[row][col].collapsed:
    #             grid.board[row][col].collapse()
    #             break
    #     time.sleep(1000)
    #     canvas.render_color_grid(grid.get_color_grid())
    canvas.window.mainloop()
    #index = random.randrange(0, len(tiles))
    #canvas.render_neighbour(tiles[index])
