import random
from typing import Callable
from direction_enum import Direction
from tile import Tile


class Cell:

    def __init__(self, initial_options : list[Tile]):
        self.options = initial_options.copy()
        self.collapsed = False
        self.entropy_change_callback = []
        self.neighbours : dict[Cell, Direction] = {}
        self.color = None

    def add_neighbour(self, neighbour : "Cell", dir : Direction) -> None:
        self.neighbours[neighbour] = dir
        neighbour.subscribe_entropy_change(self.reduce)

    def reduce(self, other_cell : "Cell") -> None:
        dir = self.neighbours[other_cell]
        removed_options = []
        for option in self.options:
            if not option.has_any(dir, other_cell.get_options):
                removed_options.append(option)
        if len(removed_options) > 0:
            for removed_option in removed_options:
                self.options.remove(removed_option)
            if len(self.options) <= 0:
                raise RuntimeError("Cell has no options")
            if len(self.options) == 1:
                self.collapse()
            self._entropy_changed()
    
    @property
    def get_options(self) -> list[Tile]:
        return self.options

    def collapse(self) -> None:
        if self.collapsed:
            return
        if len(self.options) <= 0:
            raise RuntimeError("Cell has no options")
        option = random.sample(self.options, 1)[0]
        if len(self.options) > 1:
            self.options = [option]
            self._entropy_changed()
        else:
            self.options = [option]
        self.collapsed = True

    def _entropy_changed(self) -> None:
        self.color = None
        self.report_entropy_change()

    def report_entropy_change(self) -> None:
        for callback in self.entropy_change_callback:
            callback(self)

    def subscribe_entropy_change(self, callback : Callable[["Cell"], None]) -> None:
        self.entropy_change_callback.append(callback)

    def get_color(self) -> tuple[int]:
        if self.color is not None:
            return self.color
        r = 0
        b = 0
        g = 0
        for option in self.options:
            color = option.get_color()
            r += color[0]
            b += color[1]
            g += color[2]
        r //= len(self.options)
        b //= len(self.options)
        g //= len(self.options)
        self.color = (r, b, g)
        return self.color

