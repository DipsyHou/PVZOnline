from .base import Plant
from ...constants import CELL_W, CELL_H, COLS

class IcedCoconut(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "iced_coconut")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0 # Does not shoot
        self.cost = 175
        
        self.rolling_started = False
        self.roll_remaining = 0
        self.roll_speed = 0
        self.knocked_zombies = set()

    def update(self, dt, game_state):
        if not self.rolling_started:
            self.rolling_started = True
            max_cells = min(4, COLS - 1 - self.col)
            self.roll_remaining = max_cells * CELL_W
            self.roll_speed = 320
            
            # Detach pumpkin logic? In backend we might not have pumpkin attachment fully implemented yet.
            # JS: if(this.pumpkin) ...
            
        move = self.roll_speed * dt
        self.x += move
        self.roll_remaining -= move
        
        if self.roll_remaining <= 0:
            self.active = False
            
            # Explosion Logic
            radius = 150 # 1.5 cells
            damage = 1800
            slow_duration = 10.0
            slow_factor = 0.5
            
            for z in game_state.zombies:
                # Calculate distance from center to center
                dx = (z.x + z.w/2) - (self.x + self.w/2)
                dy = (z.y + z.h/2) - (self.y + self.h/2)
                dist = (dx**2 + dy**2)**0.5
                
                if dist <= radius:
                    z.take_damage(damage)
                    z.apply_slow(slow_duration, slow_factor)

            # Event
            game_state.events.append({
                "type": "particle",
                "x": self.x + self.w/2,
                "y": self.y + self.h/2,
                "kind": "ice_explosion"
            })
            return

        # Collision with zombies
        for z in game_state.zombies:
            if z.row != self.row: continue
            if z.id in self.knocked_zombies: continue
            
            # Simple collision
            if self.x + self.w > z.x and self.x < z.x + z.w:
                # Knockback
                z.apply_knockback(CELL_W, 0.5) # 1 cell back over 0.5s
                self.knocked_zombies.add(z.id)
