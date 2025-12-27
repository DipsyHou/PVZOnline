from .base import Plant
from ..bullet import Bullet
from ...constants import CELL_W, CELL_H

class Jelly(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "jelly")
        self.hp = 500
        self.max_hp = 500
        self.shoot_interval = float('inf')
        self.cost = 125

    def update(self, dt, game_state):
        # Reflect bullets
        left = self.x + 10
        right = self.x + CELL_W - 10
        top = self.y + 10
        bottom = self.y + CELL_H - 10
        
        for b in game_state.bullets:
            # Check if already reflected by this instance
            if hasattr(b, 'reflected_by') and b.reflected_by == self:
                continue
            
            # Ignore certain types
            if b.kind in ["watermelon", "bomb", "citron_plasma", "grape"]:
                continue
                
            # Check collision
            if left <= b.x <= right and top <= b.y <= bottom:
                b.vx = -b.vx
                b.vy = -b.vy
                b.reflected_by = self
                
                if b.homing:
                    b.homing = False
                    b.target = None
