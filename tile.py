from functools import lru_cache
from direction_enum import Direction


class Tile:

    SIZE = 3

    def __init__(self, pixels : list[list[tuple[int]]]):
        self.pixels = pixels
        self.directions = {direction: set() for direction in Direction}
        self._hash = None
        self._has_any_cache = {direction: {} for direction in Direction}

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(tuple(tuple(row) for row in cube) for cube in self.pixels))
        return self._hash
    
    def __eq__(self, other):
        return isinstance(other, Tile) and self.pixels == other.pixels

    @property
    def get_pixels(self) -> list[list[tuple[int]]]:
        return self.pixels

    def add_tile(self, direction: Direction, tile : "Tile") -> bool:
        self.directions[direction].add(tile)

    def contains_tile(self, direction: Direction, tile : "Tile") -> bool:
        return tile in self.directions[direction]
    
    def get_tiles(self, direction: Direction) -> set["Tile"]:
        return self.directions[direction]
    
    def has_any(self, direction: Direction, tiles : set["Tile"]) -> bool:
        tiles_key = frozenset(tiles)
        if tiles_key in self._has_any_cache[direction]:
            return self._has_any_cache[direction][tiles_key]
        
        result = any(tile in self.directions[direction] for tile in tiles)
        self._has_any_cache[direction][tiles_key] = result
        return result
    
    def get_color(self) -> tuple[int]:
        return self.pixels[Tile.SIZE // 2][Tile.SIZE // 2]