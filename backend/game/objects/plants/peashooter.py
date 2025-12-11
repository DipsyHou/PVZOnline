from .base import Plant
from ..bullet import Bullet

class Peashooter(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "peashooter")
        self.hp = 300
        self.max_hp = 300
        self.action_interval = 1.5
        self.cost = 100

    def update(self, now, game_state):
        if now - self.last_action > self.action_interval:
            # Check if any zombie in the same row and to the right
            if any(z.row == self.row and z.x > self.x for z in game_state.zombies):
                self.last_action = now
                game_state.bullets.append(Bullet(self.x + 40, self.y + 20, self.row))
