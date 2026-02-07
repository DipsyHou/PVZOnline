from .base import Plant
from ..bullet import Bullet

class Citron(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "citron")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0
        self.cost = 200
        self.charge_time = 0
        self.max_charge = 20.0

    def update(self, dt, game_state):
        self.charge_time += dt
        if self.charge_time > self.max_charge:
            self.charge_time = self.max_charge

    def activate(self, game_state):
        if self.charge_time < 1.0:
            return

        effective_charge = min(self.charge_time, 20.0)
        bullet_level = int(effective_charge / 1.0)
        pierce_count = int(effective_charge / 3.0)
        damage = 20 * bullet_level
        
        # Radius calculation (approximate visual size)
        radius = 5 + min(30, effective_charge * 2)
        knockback = False
        
        if effective_charge >= 10.0:
            knockback = True
            
        if effective_charge >= 20.0:
            pierce_count = 9999
            radius = 100
            
        bx = self.x + 40
        by = self.y + 40 - radius

        b = Bullet(bx, by, self.row, 1000, 0, damage, "citron_plasma")
        b.pierce = pierce_count
        b.w = radius * 2
        b.h = radius * 2
        
        if knockback:
            b.knockback_dist = 100
            b.knockback_duration = 0.5
            
        game_state.bullets.append(b)
        self.charge_time = 0
