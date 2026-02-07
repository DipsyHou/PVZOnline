from .base import Zombie
from ...config import PLANT_W

class GargantuarZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "gargantuar")
        self.hp = 4500
        self.max_hp = 4500
        self.speed = 15
        self.damage = 50
        self.smash_timer = 0

    def update(self, now, dt, game_state):
        # Status updates
        if self.slow_timer > 0: self.slow_timer -= dt
        if self.stun_timer > 0: self.stun_timer -= dt
        if self.knockback_timer > 0: self.knockback_timer -= dt

        current_speed = self.speed
        if self.slow_timer > 0: current_speed *= self.slow_factor
        if self.stun_timer > 0: current_speed = 0
        
        if self.knockback_timer > 0:
            self.x += self.knockback_speed * dt
            return

        # Attack logic
        targets = []
        for p in game_state.plants:
            if p.row == self.row and p.active:
                if self.x < p.x + p.w and self.x + self.w > p.x:
                    if p.type in ["time_machine", "reshaper", "iced_coconut"]:
                        continue
                    targets.append(p)
        
        if targets:
            # Sort targets: Pumpkin first
            targets.sort(key=lambda p: 0 if p.type == "spiky_pumpkin" else 1)
            target = targets[0]
            
            if self.stun_timer <= 0:
                self.smash_timer += dt
                if self.smash_timer >= 1.0:
                    target.hp -= 9999
                    if target.hp <= 0: target.active = False
                    self.smash_timer = 0
                    
                    game_state.add_event({
                        "type": "particle",
                        "x": target.x + target.w/2,
                        "y": target.y + target.h/2,
                        "kind": "smash"
                    })
        else:
            self.smash_timer = 0
            self.x -= current_speed * dt
