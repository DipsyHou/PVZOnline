from .base import Plant
from ..bullet import Bullet

class PineShooter(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "pine_shooter")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 1.0
        self.cost = 150

    def shoot(self, game_state):
        has_target = False
        for z in game_state.zombies:
            if z.row == self.row and z.x > self.x:
                has_target = True
                break
        
        if has_target:
            bx = self.x + 40
            by = self.y + 20
            b = Bullet(bx, by, self.row, 720, 0, 20, "needle")
            b.pierce = 999
            b.w = 8 # Needle is thin
            b.h = 8
            game_state.bullets.append(b)
