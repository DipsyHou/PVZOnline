from .base import Zombie
from ...constants import PLANT_W, CELL_W

class PriestZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "priest")
        self.hp = 200
        self.max_hp = 200
        self.speed = 20
        self.damage = 50
        
        self.heal_target_id = None
        self.heal_rate = 50
        self.link_cooldown = 0

    def update(self, now, dt, game_state):
        # Status updates
        if self.slow_timer > 0: self.slow_timer -= dt
        if self.stun_timer > 0: self.stun_timer -= dt
        if self.knockback_timer > 0: self.knockback_timer -= dt

        if self.stun_timer > 0:
            self.heal_target_id = None
            return

        if self.knockback_timer > 0:
            self.x += self.knockback_speed * dt
            return

        # Cooldown
        if self.link_cooldown > 0:
            self.link_cooldown -= dt
            self.heal_target_id = None

        # Validate Target
        target = None
        if self.heal_target_id:
            for z in game_state.zombies:
                if z.id == self.heal_target_id and z.active:
                    target = z
                    break
            
            if target:
                # Check distance
                cx = self.x + self.w / 2
                cy = self.y + self.h / 2
                zcx = target.x + target.w / 2
                zcy = target.y + target.h / 2
                dist_sq = (cx - zcx)**2 + (cy - zcy)**2
                max_dist = CELL_W * 3
                
                if target.hp >= target.max_hp or dist_sq > max_dist**2:
                    target = None
                    self.heal_target_id = None
                    self.link_cooldown = 1.0
            else:
                self.heal_target_id = None
                self.link_cooldown = 1.0

        # Find new target
        if not target and self.link_cooldown <= 0:
            cx = self.x + self.w / 2
            cy = self.y + self.h / 2
            max_dist = CELL_W * 3
            min_dist_sq = float('inf')
            
            for z in game_state.zombies:
                if z.id == self.id or not z.active: continue
                if z.hp >= z.max_hp: continue
                
                zcx = z.x + z.w / 2
                zcy = z.y + z.h / 2
                dist_sq = (cx - zcx)**2 + (cy - zcy)**2
                
                if dist_sq <= max_dist**2 and dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    target = z
            
            if target:
                self.heal_target_id = target.id

        # Action
        if target:
            # Heal
            amount = self.heal_rate * dt
            target.hp = min(target.max_hp, target.hp + amount)
            # Don't move/eat while healing
        else:
            # Normal behavior (move/eat)
            eating = False
            targets = []
            for p in game_state.plants:
                if p.row == self.row and p.active:
                    if self.x < p.x + p.w and self.x + self.w > p.x:
                        if p.type in ["time_machine", "reshaper", "iced_coconut"]: continue
                        targets.append(p)
            
            if targets:
                eating = True
                targets.sort(key=lambda p: 0 if p.type == "spiky_pumpkin" else 1)
                t = targets[0]
                t.hp -= self.damage * dt
                if t.hp <= 0: t.active = False
            
            if not eating:
                current_speed = self.speed
                if self.slow_timer > 0: current_speed *= self.slow_factor
                self.x -= current_speed * dt
