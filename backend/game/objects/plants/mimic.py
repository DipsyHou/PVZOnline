from .base import Plant

class Mimic(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "mimic")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0
        self.cost = 325
        self.mimic_timer = 3.0
        self.mimic_target = None

    def update(self, dt, game_state):
        if self.mimic_target:
            self.mimic_timer -= dt
            if self.mimic_timer <= 0:
                # Transform
                if hasattr(game_state, 'transform_plant'):
                    game_state.transform_plant(self, self.mimic_target)
