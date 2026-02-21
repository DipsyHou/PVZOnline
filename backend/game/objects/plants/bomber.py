import math
from .base import Plant
from ..bullet import Bullet
from ...config import CELL_W, CELL_H, ROWS

class Bomber(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "bomber")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 3.0
        self.cost = 200

    def shoot(self, game_state):
        # Targets zombies in row-1, row, row+1
        # Only if x > self.x
        
        # Windmill boost check
        windmill_boost = 1.0
        for p in game_state.plants:
            if p.row == self.row and p.col < self.col and p.type == "windmill":
                windmill_boost = 1.5
                break

        rows_to_check = [self.row - 1, self.row, self.row + 1]
        g = 1200
        
        for r in rows_to_check:
            if r < 0 or r >= ROWS: continue
            
            candidates = [z for z in game_state.zombies if z.row == r and z.x > self.x]
            if not candidates: continue
            
            # Sort by distance
            candidates.sort(key=lambda z: z.x)
            
            # Take up to 2 targets
            targets = candidates[:2]
            
            for target in targets:
                bx = self.x + 40
                by = self.y + 20
                target_x = target.x + target.w / 2
                target_y = target.y + target.h / 2
                
                dx = target_x - bx
                dy = target_y - by
                
                t = max(0.35, min(1.0, abs(dx) / 450))
                vx = dx / t
                vy = (dy - 0.5 * g * t * t) / t
                
                b = Bullet(bx, by, r, vx, vy, 50 * windmill_boost, "bomb")
                b.total_time = t
                b.target_x = target_x
                b.target_y = target_y

                
                game_state.bullets.append(b)
