from ..base import GameObject
from ...constants import SCREEN_WIDTH, CELL_H, CELL_W, ZOMBIE_W, ZOMBIE_H

class Zombie(GameObject):
    def __init__(self, row, type_name):
        # Spawn at the right edge of the screen, centered vertically in the row
        x = SCREEN_WIDTH - CELL_W
        y = row * CELL_H + (CELL_H - ZOMBIE_H) / 2
        super().__init__(x, y, ZOMBIE_W, ZOMBIE_H, type_name) 
        self.row = row
        self.speed = 20 
        self.damage = 20 

    def update(self, now, dt, game_state):
        pass
