from .base import Zombie
from ...config import PLANT_W, CELL_W, COLS

class FisherZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "fisher")
        self.hp = 400
        self.max_hp = 400
        self.speed = 20
        self.damage = 50
        
        self.hook_cooldown = 0
        self.hook_charge_time = 0
        self.is_hooking = False
        self.hook_target_id = None

    def update(self, now, dt, game_state):
        # Status updates
        if self.slow_timer > 0: self.slow_timer -= dt
        if self.stun_timer > 0: self.stun_timer -= dt
        if self.knockback_timer > 0: self.knockback_timer -= dt

        if self.stun_timer > 0:
            # Stunned: no movement, no hook progress
            return

        if self.knockback_timer > 0:
            self.x += self.knockback_speed * dt
            return

        # Hook Logic
        if self.hook_cooldown > 0:
            self.hook_cooldown -= dt

        if self.is_hooking:
            self.hook_charge_time += dt
            if self.hook_charge_time >= 1.0:
                # Execute hook
                target = None
                for p in game_state.plants:
                    if p.id == self.hook_target_id and p.active:
                        target = p
                        break
                
                if target:
                    # Move plant 1 cell right
                    current_col = target.col
                    new_col = current_col + 1
                    
                    # Check if new pos is valid (inside grid and empty)
                    if new_col < COLS:
                        # Check if occupied
                        occupied = False
                        for p in game_state.plants:
                            if p.active and p.row == self.row and p.col == new_col:
                                occupied = True
                                break
                        
                        if not occupied:
                            target.col = new_col
                            target.x = new_col * CELL_W + (CELL_W - PLANT_W) / 2
                            
                            game_state.add_event({
                                "type": "particle",
                                "x": target.x + target.w/2,
                                "y": target.y + target.h/2,
                                "kind": "hook_pull"
                            })

                # Reset
                self.is_hooking = False
                self.hook_target_id = None
                self.hook_cooldown = 5.0
                self.hook_charge_time = 0
        else:
            # Not hooking
            # Check if we should start hooking
            # Only if not eating (eating handled by super logic usually, but here we override)
            
            # Check for eating first (standard behavior)
            eating = False
            targets = []
            for p in game_state.plants:
                if p.row == self.row and p.active:
                    if self.x < p.x + p.w and self.x + self.w > p.x:
                        # Ignore floating plants
                        from ...config import get_plant_category
                        if get_plant_category(p.type) == "floating":
                            continue
                        targets.append(p)
            
            if targets:
                eating = True
                targets.sort(key=lambda p: 0 if p.type == "spiky_pumpkin" else 1)
                target = targets[0]
                target.hp -= self.damage * dt
                if target.hp <= 0: target.active = False
            
            if not eating:
                # Try to hook if cooldown ready
                if self.hook_cooldown <= 0:
                    # Find rightmost plant to the left of zombie
                    best_col = -1
                    target = None
                    zombie_col = int(self.x / CELL_W)
                    
                    from ...config import get_plant_category
                    for p in game_state.plants:
                        if p.row == self.row and p.active and p.col < zombie_col:
                            # Ignore floating plants for hooking
                            if get_plant_category(p.type) == "floating":
                                continue
                            if p.col > best_col:
                                best_col = p.col
                                target = p
                    
                    if target:
                        self.is_hooking = True
                        self.hook_target_id = target.id
                        self.hook_charge_time = 0
                
                if not self.is_hooking:
                    # Move
                    current_speed = self.speed
                    if self.slow_timer > 0: current_speed *= self.slow_factor
                    self.x -= current_speed * dt
