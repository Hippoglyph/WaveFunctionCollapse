from collections import deque
import random
import sys
import time
from canvas import Canvas
from cell import Cell
from grid import Grid
from tile_extractor import TileExtractor


class WaveFunctionCollapse:

    def __init__(self, img_path : str, width : int, height : int) -> None:
        init_start_time = time.time()
        tiles = TileExtractor.extract(img_path)
        self.grid = Grid(width, height, tiles)
        self.canvas = Canvas()
        self.entropy_queue = deque()
        self.entropy_map : dict[Cell, int] = {}
        self.entropy_list : dict[int, list[Cell]] = {}
        self.lowest_entropy = sys.maxsize
        self.unaccounted : set[Cell] = set()
        for cell in self.grid.get_cells:
            initial_entropy = cell.get_entropy()
            self.entropy_map[cell] = initial_entropy
            if initial_entropy not in self.entropy_list:
                self.entropy_list[initial_entropy] = []
            self.entropy_list[initial_entropy].append(cell)
            cell.subscribe_entropy_change(self._entropy_updated)
        for entropy, _ in self.entropy_list.items():
            if entropy < self.lowest_entropy:
                self.lowest_entropy = entropy
        self.canvas.render_color_grid(self.grid.get_color_grid())
        print(f"Init time: {time.time() - init_start_time} seconds")

    def _entropy_updated(self, cell : Cell) -> None:
        self.unaccounted.add(cell)
        self.entropy_queue.append(cell)

    def propage_entropy(self) -> None:
        while self.entropy_queue:
            cell : Cell = self.entropy_queue.popleft()
            neighbours = cell.get_neighbours()
            for neighbour in neighbours:
                neighbour.reduce(cell)
    
    def update_priorites(self):
        for cell in self.unaccounted:
            new_entropy = cell.get_entropy()
            old_entropy = self.entropy_map[cell]
            self.entropy_map.pop(cell)
            if new_entropy != old_entropy:
                old_list = self.entropy_list[old_entropy]
                old_list.remove(cell)
                if len(old_list) <= 0:
                    self.entropy_list.pop(old_entropy)
                    if self.lowest_entropy is not None and old_entropy <= self.lowest_entropy:
                        self.lowest_entropy = None
                if new_entropy > 1:
                    if new_entropy not in self.entropy_list:
                        self.entropy_list[new_entropy] = []
                    self.entropy_list[new_entropy].append(cell)
                    if self.lowest_entropy is not None and new_entropy < self.lowest_entropy:
                        self.lowest_entropy = new_entropy
                    self.entropy_map[cell] = new_entropy
        self.unaccounted.clear()

    def run(self, delay : int = 0) -> None:
        run_start_time = time.time()
        while not self.collapse():
            self.propage_entropy()
            self.update_priorites()
            self.canvas.render_color_grid(self.grid.get_color_grid())
            if delay > 0:
                self.canvas.sleep(delay)
        print(f"Run time: {time.time() - run_start_time} seconds")
        self.canvas.wait()

    def collapse(self) -> bool:
        if self.lowest_entropy is None:
            all_entropies = self.entropy_list.keys()
            if len(all_entropies) <= 0:
                return True
            self.lowest_entropy = min(self.entropy_list.keys())
        winner = random.sample(self.entropy_list[self.lowest_entropy], 1)[0]
        winner.collapse()
        return False

    def collapse_random(self) -> bool: # FAKE
        not_collapsed = []
        for cell in self.grid.get_cells:
            if not cell.collapsed:
                not_collapsed.append(cell)
        if len(not_collapsed) <= 0:
            return True
        cell : Cell = random.sample(not_collapsed, 1)[0]
        cell.collapse()
        return len(not_collapsed) <= 1