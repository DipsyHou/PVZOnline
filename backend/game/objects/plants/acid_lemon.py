from .base import Plant
from ..bullet import Bullet
from ...constants import CELL_W, CELL_H

class AcidLemon(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "acid_lemon")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 2.0
        self.cost = 125

    def shoot(self, game_state):
        # Check if any zombie in the same row and to the right
        has_target = False
        for z in game_state.zombies:
            if z.row == self.row and z.x > self.x:
                has_target = True
                break
        
        if has_target:
            # Spawn bullet
            bx = self.x + 40
            by = self.y + 20
            # Base damage is 25. Special damage is handled in BulletManager.
            b = Bullet(bx, by, self.row, 360, 0, 25, "acid_juice")
            # Flags for interactions
            b.can_be_attracted = True # For Trumpet
            b.can_be_reflected = True # For Jelly
            game_state.bullets.append(b)
