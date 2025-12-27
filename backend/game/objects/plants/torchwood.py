from .base import Plant

class Torchwood(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "torchwood")
        self.hp = 500
        self.max_hp = 500
        self.shoot_interval = 0 # Does not shoot
        self.cost = 175

    def update(self, dt, game_state):
        # Torchwood logic is passive (handled by bullets)
        pass
