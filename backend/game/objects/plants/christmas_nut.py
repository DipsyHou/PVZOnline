from .base import Plant
from ...config import CELL_W, CELL_H

class ChristmasNut(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "christmas_nut")
        self.hp = 2000
        self.max_hp = 2000
        self.shoot_interval = 0
        self.cost = 50
        
    def on_death(self, game_state):
        # Visual effect
        game_state.add_event({
            "type": "particle",
            "x": self.x + self.w/2,
            "y": self.y + self.h/2,
            "kind": "christmas_explosion"
        })
        
        # Explosion logic (3x3)
        center_col = self.col
        center_row = self.row
        
        damage = 900
        
        for z in game_state.zombies:
            # Calculate zombie column based on center position
            z_col = int((z.x + z.w/2) / CELL_W)
            z_row = z.row
            
            # Check if in 3x3 area
            if abs(z_col - center_col) <= 1 and abs(z_row - center_row) <= 1:
                z.take_damage(damage)
