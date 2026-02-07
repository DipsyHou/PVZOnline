import random
from .base import Plant
from ..bullet import Bullet

class CornHoming(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "corn_homing")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 1.0
        self.cost = 375

    def shoot(self, game_state):
        # Find leftmost zombie
        target = None
        min_x = float('inf')
        
        for z in game_state.zombies:
            if z.x < min_x:
                min_x = z.x
                target = z
        
        if target:
            bx = self.x + 20
            by = self.y
            
            rand = random.random()
            if rand < 0.75:
                kind = "corn"
                damage = 20
                stun = 0
            else:
                kind = "butter"
                damage = 40
                stun = 2.0
            
            b = Bullet(bx, by, self.row, 360, 0, damage, kind)
            b.homing = True
            b.target = target
            b.stun = stun
            
            game_state.bullets.append(b)
