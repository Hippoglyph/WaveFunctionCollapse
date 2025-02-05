from direction_enum import Direction


class Tile:

    SIZE = 3

    def __init__(self, pixels : list[list[tuple[int]]]):
        self.pixels = pixels
        self.directions = {direction: set() for direction in Direction}
        self._hash = None

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(tuple(tuple(row) for row in cube) for cube in self.pixels))
        return self._hash
    
    def __eq__(self, other):
        return isinstance(other, Tile) and self.pixels == other.pixels

    # Getter for pixels
    @property
    def get_pixels(self):
        return self.pixels

    # Add tile to a direction
    def add_tile(self, direction: Direction, tile : "Tile"):
        self.directions[direction].add(tile)

    # Check if tile is in a direction
    def contains_tile(self, direction: Direction, tile : "Tile"):
        return tile in self.directions[direction]
    
    # Check if tile is in a direction
    def get_tiles(self, direction: Direction):
        return self.directions[direction]
    
    def has_any(self, direction: Direction, tiles : list["Tile"]):
        return any(tile in self.directions[direction] for tile in tiles)
    
    def get_color(self) -> tuple[int]:
        return self.pixels[Tile.SIZE // 2][Tile.SIZE // 2]