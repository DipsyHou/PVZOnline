from ..base import GameObject
from ...config import SCREEN_WIDTH, CELL_H, ZOMBIE_W, ZOMBIE_H, PLANT_W, PLANT_H, CELL_W

class Zombie(GameObject):
    def __init__(self, row, type_name):
        x = SCREEN_WIDTH - CELL_W
        y = row * CELL_H + (CELL_H - ZOMBIE_H) / 2
        super().__init__(x, y, ZOMBIE_W, ZOMBIE_H, type_name)
        self.row = row
        self.hp = 200
        self.max_hp = 200
        self.speed = 20
        self.damage = 50 # DPS
        self.armor = 0
        self.max_armor = 0
        
        # Status effects
        self.slow_timer = 0
        self.slow_factor = 1.0
        self.stun_timer = 0
        self.knockback_timer = 0
        self.knockback_speed = 0

    def take_damage(self, amount):
        # Armor logic (if any)
        if self.armor > 0:
            self.armor -= amount
            if self.armor < 0:
                self.hp += self.armor # overflow damage
                self.armor = 0
        else:
            self.hp -= amount
            
        if self.hp <= 0:
            self.active = False

    def apply_slow(self, duration, factor):
        self.slow_timer = duration
        self.slow_factor = factor

    def apply_stun(self, duration):
        self.stun_timer = duration

    def apply_knockback(self, dist, duration):
        self.knockback_timer = duration
        self.knockback_speed = dist / duration

    def update(self, now, dt, game_state):
        # Status updates
        if self.slow_timer > 0: self.slow_timer -= dt
        if self.stun_timer > 0: self.stun_timer -= dt
        if self.knockback_timer > 0: self.knockback_timer -= dt

        # Knockback overrides everything else
        if self.knockback_timer > 0:
            self.x += self.knockback_speed * dt
            return

        # Stunned: no movement, no eating
        if self.stun_timer > 0:
            return

        # Calculate speed
        current_speed = self.speed
        if self.slow_timer > 0: current_speed *= self.slow_factor

        # Attack logic
        eating = False
        # Prioritize pumpkin, then normal plants
        targets = []
        for p in game_state.plants:
            if p.row == self.row and p.active:
                # Simple collision for eating
                if self.x < p.x + p.w and self.x + self.w > p.x:
                    # Ignore floating plants for eating?
                    if p.type in ["time_machine", "reshaper", "iced_coconut"]:
                        continue
                    targets.append(p)
        
        if targets:
            eating = True
            # Sort targets: Pumpkin first
            targets.sort(key=lambda p: 0 if p.type == "spiky_pumpkin" else 1)
            target = targets[0]
            
            target.hp -= self.damage * dt
            if target.hp <= 0: target.active = False
        
        if not eating:
            self.x -= current_speed * dt
