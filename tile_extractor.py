from PIL import Image

from tile import Tile

class TileExtractor:

    @staticmethod
    def extract(img_path : str) -> list[Tile]:
        tiles = TileExtractor._create_base_tiles(img_path)
        #tiles = [tiles[3], tiles[1]] # REMOVE
        tiles = TileExtractor._extract_neighbours(tiles) # TODO
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
                            yi = y - Tile.SIZE // 2 + i
                            xj = x - Tile.SIZE // 2 + j
                            if xj >= 0 and xj < width and yi >= 0 and yi < height:
                                tile_pixels[i][j] = img.getpixel((xj, yi))
                    #if tile_pixels is [[(0,0,0) for _ in range(Tile.SIZE)] for _ in range(Tile.SIZE)]: # REMOVE
                    tile_set.add(Tile(tile_pixels))
                    #if len(tile_set) > 4:
                    #    return list(tile_set) # REMOVE
        return list(tile_set)
    
    @staticmethod 
    def _extract_neighbours(tiles : list[Tile]) -> list[Tile]:
        for tile in tiles:
            tile.create_neighbours(tiles)
        return tiles