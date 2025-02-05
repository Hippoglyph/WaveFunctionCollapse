import math
from PIL import Image

from tile import Direction, Tile

class TileExtractor:

    @staticmethod
    def extract(img_path : str) -> list[Tile]:
        tiles = TileExtractor._create_base_tiles(img_path)
        tiles = TileExtractor._extract_neighbours(tiles)
        return tiles

    @staticmethod 
    def _create_base_tiles(img_path : str) -> list[Tile]:
        tile_set = set()
        with Image.open(img_path) as img:
            img = img.convert('RGB')
            width, height = img.size
            for x in range(width):
                for y in range(height):
                    tile_pixels = [[(-1,-1,-1) for _ in range(Tile.SIZE)] for _ in range(Tile.SIZE)]

                    for i in range(0, Tile.SIZE):
                        for j in range(0, Tile.SIZE):
                            yi = (y - Tile.SIZE // 2 + i) % height
                            xj = (x - Tile.SIZE // 2 + j) % width
                            #if xj >= 0 and xj < width and yi >= 0 and yi < height:
                            tile_pixels[i][j] = img.getpixel((xj, yi))
                    tile_set.add(Tile(tile_pixels))
        return list(tile_set)
    
    @staticmethod 
    def _extract_neighbours(tiles : list[Tile]) -> list[Tile]:
        for tile in tiles:
            for other_tile in tiles:
                TileExtractor._create_neighbour(tile, other_tile)
        return tiles
    
    @staticmethod 
    def _create_neighbour(tile : Tile, other_tile : Tile) -> None:
        upper_bound = math.ceil(Tile.SIZE / 2)
        lower_bound = Tile.SIZE // 2
        self_east = [row[lower_bound:] for row in tile.get_pixels]
        self_south = tile.get_pixels[lower_bound:]
        self_west = [row[:upper_bound] for row in tile.get_pixels]
        self_north = tile.get_pixels[:upper_bound]
        other_east = [row[lower_bound:] for row in other_tile.get_pixels]
        other_south = other_tile.get_pixels[lower_bound:]
        other_west = [row[:upper_bound] for row in other_tile.get_pixels]
        other_north = other_tile.get_pixels[:upper_bound]

        if not tile.contains_tile(Direction.EAST, other_tile):
            if TileExtractor._all_the_same(self_east, other_west):
                tile.add_tile(Direction.EAST, other_tile)
                other_tile.add_tile(Direction.WEST, tile)

        if not tile.contains_tile(Direction.SOUTH, other_tile):
            if TileExtractor._all_the_same(self_south, other_north):
                tile.add_tile(Direction.SOUTH, other_tile)
                other_tile.add_tile(Direction.NORTH, tile)

        if not tile.contains_tile(Direction.WEST, other_tile):
            if TileExtractor._all_the_same(self_west, other_east):
                tile.add_tile(Direction.WEST, other_tile)
                other_tile.add_tile(Direction.EAST, tile)

        if not tile.contains_tile(Direction.NORTH, other_tile):
            if TileExtractor._all_the_same(self_north, other_south):
                tile.add_tile(Direction.NORTH, other_tile)
                other_tile.add_tile(Direction.SOUTH, tile)
    
    @staticmethod 
    def _all_the_same(tile_a : list[list[tuple[int]]], tile_b : list[list[tuple[int]]]) -> bool:
        for i in range(len(tile_a)):
            for j in range(len(tile_a[0])):
                pixels = tile_a[i][j]
                r = pixels[0]
                b = pixels[1]
                g = pixels[2]
                other_pixels = tile_b[i][j]
                r_o = other_pixels[0]
                b_o = other_pixels[1]
                g_o = other_pixels[2]
                if r is not r_o or b is not b_o or g is not g_o:
                    return False
        return True
