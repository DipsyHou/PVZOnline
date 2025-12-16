from .base import Plant
from ..bullet import Bullet

class LaserShroom(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "laser_shroom")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0.4
        self.cost = 300
        self.laser_active_time = 0

    def update(self, dt, game_state):
        super().update(dt, game_state)
        if self.laser_active_time > 0:
            self.laser_active_time -= dt

    def shoot(self, game_state):
        # Check if any zombie is in 5x5 range (radius 2)
        has_target = False
        for z in game_state.zombies:
            z_col = int((z.x + z.w/2) / 100) # Assuming CELL_W=100
            z_row = z.row
            if abs(z_col - self.col) <= 2 and abs(z_row - self.row) <= 2:
                has_target = True
                break

        if has_target:
            self.laser_active_time = 0.2
            
            # Define affected cells (Diamond shape? JS code: directions * 1 and * 2)
            # JS: directions = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
            # It covers 2 layers of neighbors in 8 directions.
            # Basically a 5x5 grid but maybe missing corners?
            # JS loop: for i=1 to 2.
            # It seems to cover the star pattern.
            
            affected_cells = set()
            affected_cells.add((self.col, self.row))
            directions = [
                (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)
            ]
            
            for dx, dy in directions:
                for i in range(1, 3):
                    c = self.col + dx * i
                    r = self.row + dy * i
                    affected_cells.add((c, r))
            
            # Damage zombies in affected cells
            for z in game_state.zombies:
                z_col = int((z.x + z.w/2) / 100)
                z_row = z.row
                if (z_col, z_row) in affected_cells:
                    z.take_damage(20)
