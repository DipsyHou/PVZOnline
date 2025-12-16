import math
from .base import Plant
from ..bullet import Bullet
from ...constants import CELL_W, CELL_H

class Watermelon(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "watermelon")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 3.0
        self.cost = 300

    def shoot(self, game_state):
        # Find nearest zombie in same row
        target = None
        best_dist = float('inf')
        
        for z in game_state.zombies:
            if z.row == self.row and z.x > self.x:
                d = z.x - self.x
                if d < best_dist:
                    best_dist = d
                    target = z
        
        if not target:
            return

        # Windmill boost check
        windmill_boost = 1.0
        for p in game_state.plants:
            if p.row == self.row and p.col < self.col and p.type == "windmill":
                windmill_boost = 1.5
                break

        bx = self.x + 40
        by = self.y + 20
        target_x = target.x + target.w / 2
        target_y = target.y + target.h / 2
        
        dx = target_x - bx
        dy = target_y - by
        g = 1200
        
        # Time to impact
        t = max(0.4, min(1.2, abs(dx) / 400))
        vx = dx / t
        vy = (dy - 0.5 * g * t * t) / t
        
        b = Bullet(bx, by, self.row, vx, vy, 80 * windmill_boost, "watermelon")
        b.total_time = t
        b.target_x = target_x
        b.target_y = target_y
        b.splash_radius = 150 # approx 1.5 cells
        b.splash_damage = 40 * windmill_boost
        
        game_state.bullets.append(b)
