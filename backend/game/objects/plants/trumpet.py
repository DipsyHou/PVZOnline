from .base import Plant
from ...constants import CELL_H, ROWS, COLS

class Trumpet(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "trumpet")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0 # Does not shoot
        self.cost = 50
        
        self.trumpet_cooldown = 1.0
        self.trumpet_active = False
        self.trumpet_active_time = 0

    def update(self, dt, game_state):
        if not self.trumpet_active:
            self.trumpet_cooldown -= dt
            if self.trumpet_cooldown <= 0:
                self.trumpet_active = True
                self.trumpet_active_time = 0
        
        if self.trumpet_active:
            self.trumpet_active_time += dt
            if self.trumpet_active_time > 3.0: # 3s active window
                self.trumpet_active = False
                self.trumpet_cooldown = 1.0
                return

            # Attraction logic
            min_col = max(0, self.col - 1)
            max_col = min(COLS - 1, self.col + 1)
            min_row = max(0, self.row - 1)
            max_row = min(ROWS - 1, self.row + 1)
            target_y = self.row * CELL_H + CELL_H / 2 - 10 # Center of row (approx)

            for b in game_state.bullets:
                if b.kind in ["watermelon", "bomb", "citron_plasma", "arrow"]: continue
                
                b_col = int(b.x / 100) # Assuming CELL_W=100
                b_row = int(b.y / 100)
                
                if min_col <= b_col <= max_col and min_row <= b_row <= max_row:
                    # Attract to this row
                    lerp_factor = 5.0 * dt # Stronger pull
                    b.y += (target_y - b.y) * lerp_factor
                    # Also ensure it moves straight
                    b.vy = 0
                    # Update row property so it hits zombies in this row
                    b.row = self.row
