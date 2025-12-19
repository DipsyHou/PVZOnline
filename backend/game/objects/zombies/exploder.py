from .base import Zombie
from ...constants import PLANT_W, CELL_W, CELL_H, ROWS, COLS

class ExploderZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "exploder")
        self.hp = 200
        self.max_hp = 200
        self.speed = 40
        self.damage = 500

    def update(self, now, dt, game_state):
        # Status updates
        if self.slow_timer > 0: self.slow_timer -= dt
        if self.stun_timer > 0: self.stun_timer -= dt
        if self.knockback_timer > 0: self.knockback_timer -= dt

        # Calculate speed
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
                    if p.type in ["time_machine", "reshaper", "iced_coconut"]:
                        continue
                    targets.append(p)
        
        if targets:
            # Explode!
            self.hp = 0
            self.active = False
            
            # Visual effect
            game_state.add_event({
                "type": "particle",
                "x": self.x + self.w/2,
                "y": self.y + self.h/2,
                "kind": "explosion"
            })
            
            # Damage 3x3 area
            center_col = int((self.x + self.w/2) / CELL_W)
            center_row = self.row
            
            for r in range(center_row - 1, center_row + 2):
                for c in range(center_col - 1, center_col + 2):
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        cell_plants = [p for p in game_state.plants if p.active and p.row == r and p.col == c]
                        
                        # Check for pumpkin
                        pumpkin = next((p for p in cell_plants if p.type == 'spiky_pumpkin'), None)
                        
                        if pumpkin:
                            # Only damage pumpkin
                            pumpkin.hp -= 500
                            if pumpkin.hp <= 0: pumpkin.active = False
                        else:
                            # Damage all
                            for p in cell_plants:
                                p.hp -= 500
                                if p.hp <= 0: p.active = False
        else:
            self.x -= current_speed * dt
