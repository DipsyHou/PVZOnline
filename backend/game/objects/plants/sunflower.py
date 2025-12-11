from .base import Plant

class Sunflower(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "sunflower")
        self.hp = 200
        self.max_hp = 200
        self.action_interval = 16
        self.cost = 50

    def update(self, now, game_state):
        if now - self.last_action > self.action_interval:
            game_state.sun += 25
            self.last_action = now
