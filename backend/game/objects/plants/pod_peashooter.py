import math
from .base import Plant
from ..bullet import Bullet
from ...constants import CELL_W, CELL_H

class PodPeashooter(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "pod_peashooter")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 1.0
        self.cost = 225

    def shoot(self, game_state):
        # Check if any zombie is ahead (any row? No, usually same row or general direction)
        # Spread logic in JS checked `zombies.some(z => z.x > this.x)` (any row!)
        has_target = False
        for z in game_state.zombies:
            if z.x > self.x:
                has_target = True
                break
        
        if has_target:
            bx = self.x + 40
            by = self.y + 20
            count = 5
            min_deg = -45
            max_deg = 45
            speed = 360
            
            for i in range(count):
                t = 0.5 if count == 1 else i / (count - 1)
                deg = min_deg + t * (max_deg - min_deg)
                rad = math.radians(deg)
                vx = math.cos(rad) * speed
                vy = math.sin(rad) * speed
                b = Bullet(bx, by, self.row, vx, vy, 20, "pea")
                game_state.bullets.append(b)
