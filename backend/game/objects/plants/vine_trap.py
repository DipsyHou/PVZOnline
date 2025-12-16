from .base import Plant
from ...constants import CELL_W, CELL_H

class VineTrap(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "vine_trap")
        self.hp = 800
        self.max_hp = 800
        self.shoot_interval = 0
        self.cost = 225
        self.life_timer = 0

    def update(self, dt, game_state):
        self.life_timer += dt
        if self.life_timer >= 15.0:
            self.active = False
            return

        # Apply slow to zombies in 3x3 area
        cx = self.col
        cy = self.row
        
        for z in game_state.zombies:
            z_col = int((z.x + z.w/2) / CELL_W)
            z_row = z.row
            
            if abs(z_col - cx) <= 1 and abs(z_row - cy) <= 1:
                z.apply_slow(0.2, 0.5) # 0.2s duration (refreshed every frame), 50% speed
