from .base import Plant

class Reshaper(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "reshaper")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0
        self.cost = 50
        self.life_timer = 0

    def update(self, dt, game_state):
        # Instant effect then die
        self.life_timer += dt
        if self.life_timer > 0.1:
            self.active = False
            
            # Find target plant at this location (excluding self)
            target = None
            for p in game_state.plants:
                if p.col == self.col and p.row == self.row and p != self and p.active:
                    target = p
                    break
            
            if target:
                # Refund sun
                # We need to know the cost of the target. 
                # Since we don't have a global config easily accessible here, 
                # we rely on the plant instance having a 'cost' attribute.
                if hasattr(target, 'cost'):
                    game_state.sun += target.cost
                
                # Reset cooldown
                if target.type in game_state.plant_cooldowns:
                    del game_state.plant_cooldowns[target.type]
                
                # Remove target
                target.active = False
