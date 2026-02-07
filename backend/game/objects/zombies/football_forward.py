import random
from .base import Zombie
from ...config import PLANT_W, CELL_H, ROWS, CELL_W

class FootballForwardZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "football_forward")
        self.hp = 200
        self.max_hp = 200
        self.speed = 45
        self.damage = 50
        
        self.helm_hp = 2400
        self.max_helm_hp = 2400
        self.helm_active = True
        
        # Map for frontend
        self.armor = self.helm_hp
        self.max_armor = self.max_helm_hp

    def take_damage(self, amount):
        if self.helm_active and self.helm_hp > 0:
            self.helm_hp -= amount
            if self.helm_hp <= 0:
                overflow = -self.helm_hp
                self.helm_hp = 0
                self.helm_active = False
                self.hp -= overflow
                self.armor = 0 # Visual update helper
                self.max_armor = 0
            else:
                # Map helm hp to armor for frontend visualization
                self.armor = self.helm_hp
                self.max_armor = self.max_helm_hp
        else:
            super().take_damage(amount)

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

        # Check for contact
        targets = []
        for p in game_state.plants:
            if p.row == self.row and p.active:
                if self.x < p.x + p.w and self.x + self.w > p.x:
                    if p.type in ["time_machine", "reshaper", "iced_coconut"]: continue
                    targets.append(p)
        
        eating = False
        if targets:
            # Try to shove
            targets.sort(key=lambda p: 0 if p.type == "spiky_pumpkin" else 1)
            target = targets[0]
            
            c = target.col
            up_r = self.row - 1
            down_r = self.row + 1
            
            # Check availability
            def is_free(r, c):
                if r < 0 or r >= ROWS: return False
                for p in game_state.plants:
                    if p.active and p.row == r and p.col == c:
                        return False
                return True

            can_up = is_free(up_r, c)
            can_down = is_free(down_r, c)
            
            target_r = -1
            if can_up and not can_down:
                target_r = up_r
            elif not can_up and can_down:
                target_r = down_r
            elif can_up and can_down:
                target_r = up_r if random.random() < 0.5 else down_r
            
            if target_r != -1:
                # Move plant
                target.row = target_r
                target.y = target_r * CELL_H + (CELL_H - PLANT_W) / 2
                
                game_state.add_event({
                    "type": "particle",
                    "x": target.x + target.w/2,
                    "y": target.y + target.h/2,
                    "kind": "dust"
                })
                # Don't eat, continue moving
            else:
                # Blocked, so eat
                eating = True
                target.hp -= self.damage * dt
                if target.hp <= 0: target.active = False
        
        if not eating:
            self.x -= current_speed * dt
