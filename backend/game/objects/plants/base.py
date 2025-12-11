import time
from ..base import GameObject
from ...constants import CELL_W, CELL_H, PLANT_W, PLANT_H

class Plant(GameObject):
    def __init__(self, col, row, type_name):
        # Center the plant in the cell
        x = col * CELL_W + (CELL_W - PLANT_W) / 2
        y = row * CELL_H + (CELL_H - PLANT_H) / 2
        super().__init__(x, y, PLANT_W, PLANT_H, type_name)
        self.col = col
        self.row = row
        self.last_action = time.time()
        self.action_interval = 0
        self.cost = 0

    def update(self, now, game_state):
        pass