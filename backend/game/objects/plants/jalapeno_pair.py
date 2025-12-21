from .base import Plant
from ...constants import CELL_W, CELL_H, ROWS, COLS

class JalapenoPair(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "jalapeno_pair")
        self.hp = 10000
        self.max_hp = 10000
        self.shoot_interval = 0
        self.cost = 225
        self.explode_timer = 1.0

    def update(self, dt, game_state):
        self.explode_timer -= dt
        if self.explode_timer <= 0:
            self.explode(game_state)
            self.active = False

    def explode(self, game_state):
        damage = 1800
        cx = self.col
        cy = self.row
        
        # Event
        game_state.events.append({
            "type": "particle",
            "x": self.x + self.w/2,
            "y": self.y + self.h/2,
            "kind": "jalapeno_explosion"
        })
        
        for z in game_state.zombies:
            z_col = int((z.x + z.w/2) / CELL_W)
            
            # Row OR Column
            if z.row == cy or z_col == cx:
                z.take_damage(damage)
