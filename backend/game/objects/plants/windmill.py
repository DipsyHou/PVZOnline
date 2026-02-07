from .base import Plant

class Windmill(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "windmill")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0
        self.cost = 250

    def update(self, dt, game_state):
        pass
