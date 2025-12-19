import random
from .base import Plant
from ..bullet import Bullet

class CornGatling(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "corn_gatling")
        self.hp = 200
        self.max_hp = 200
        self.base_interval = 2.0
        self.min_interval = 0.4
        self.shoot_interval = self.base_interval
        self.cost = 275

    def update(self, dt, game_state):
        # Check for targets
        has_target = False
        for z in game_state.zombies:
            if z.row == self.row and z.x > self.x:
                has_target = True
                break
        
        # Adjust interval
        if has_target:
            if self.shoot_interval > self.min_interval:
                self.shoot_interval -= dt * 0.2
                if self.shoot_interval < self.min_interval:
                    self.shoot_interval = self.min_interval
        else:
            if self.shoot_interval < self.base_interval:
                self.shoot_interval += dt * 0.8
                if self.shoot_interval > self.base_interval:
                    self.shoot_interval = self.base_interval
        
        super().update(dt, game_state)

    def shoot(self, game_state):
        has_target = False
        for z in game_state.zombies:
            if z.row == self.row and z.x > self.x:
                has_target = True
                break
        
        if has_target:
            bx = self.x + 40
            by = self.y + 30
            
            if random.random() < 0.1:
                b = Bullet(bx, by, self.row, 400, 0, 40, "butter")
                b.stun = 2.0
            else:
                b = Bullet(bx, by, self.row, 400, 0, 20, "corn")
                
            game_state.bullets.append(b)
