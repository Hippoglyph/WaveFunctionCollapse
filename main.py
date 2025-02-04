import os
from canvas import Canvas
from tile_extractor import TileExtractor

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

if __name__ == "__main__":
    tiles = TileExtractor.extract(os.path.join(script_dir, "samples", "Water.png"))
    canvas = Canvas()
    canvas.render_neighbour(tiles[0])
