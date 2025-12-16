import math
from .base import Plant
from ..bullet import Bullet

class Maguey(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "maguey")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 1.0
        self.cost = 300
        self.range = 400
        self.max_flight = 600
        self.damage = 28

    def shoot(self, game_state):
        # Find nearest zombie within range
        cx = self.x + 40 # Center X
        cy = self.y + 40 # Center Y
        
        target = None
        min_dist = self.range
        
        for z in game_state.zombies:
            if not z.active: continue
            zx = z.x + z.w / 2
            zy = z.y + z.h / 2
            dist = math.sqrt((zx - cx)**2 + (zy - cy)**2)
            
            if dist <= min_dist:
                min_dist = dist
                target = z
        
        if target:
            # Calculate direction
            zx = target.x + target.w / 2
            zy = target.y + target.h / 2
            dx = zx - cx
            dy = zy - cy
            mag = math.sqrt(dx*dx + dy*dy)
            
            if mag > 0:
                speed = 600
                vx = (dx / mag) * speed
                vy = (dy / mag) * speed
                
                b = Bullet(cx, cy, self.row, vx, vy, self.damage, "arrow")
                b.pierce = 999 # Infinite pierce
                b.max_distance = self.max_flight
                b.w = 40
                b.h = 10
                
                game_state.bullets.append(b)
