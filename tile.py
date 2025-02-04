import math


class Tile:

    SIZE = 3

    def __init__(self, pixels : list[list[tuple[int]]]):
        self.pixels = pixels
        self.east = set()
        self.south = set()
        self.west = set()
        self.north = set()

    def __hash__(self):
        return hash(tuple(tuple(tuple(row) for row in cube) for cube in self.pixels))
    
    def __eq__(self, other):
        return isinstance(other, Tile) and self.pixels == other.pixels
    
    def create_neighbours(self, others : list["Tile"]) -> None:
        for other_tile in others:
            if self._is_neighbour(other_tile, 1, 0, 0, 0):
                print("WHat?")
            self._create_neighbour(other_tile)
    
    def _create_neighbour(self, other : "Tile") -> None:
        if self._is_neighbour(other, 1, 0, 0, 0):
            self.east.add(other)
        if self._is_neighbour(other, 0, 1, 0, 0):
            self.south.add(other)
        if self._is_neighbour(other, 0, 0, 1, 0):
            self.west.add(other)
        if self._is_neighbour(other, 0, 0, 0, 1):
            self.north.add(other)
                
    def _is_neighbour(self, other : "Tile", x_off_self : int, y_off_self : int, x_off_other : int, y_off_other : int) -> None:
        i_range = math.ceil(Tile.SIZE / 2) if y_off_self == 0 and y_off_other == 0 else Tile.SIZE # WTF?
        j_range = math.ceil(Tile.SIZE / 2) if x_off_self == 0 and x_off_other == 0 else Tile.SIZE # WTIF?
        for i in range(i_range):
            for j in range(j_range):
                pixels = self.pixels[y_off_self + i][x_off_self + j]
                r = pixels[0]
                b = pixels[1]
                g = pixels[2]
                other_pixels = other.pixels[y_off_other+i][x_off_other+j]
                r_o = other_pixels[0]
                b_o = other_pixels[1]
                g_o = other_pixels[2]
                if r is not r_o or b is not b_o or g is not g_o:
                    return False
        return True
