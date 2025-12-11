from .base import Plant
from ..bullet import Bullet

class PodPeashooter(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "pod_peashooter")
        self.hp = 200
        self.max_hp = 200
        self.action_interval = 1.5
        self.cost = 225
        self.cooldown = 7

    def update(self, now, game_state):
        if now - self.last_action > self.action_interval:
            # Fire 5 bullets
            angles = [-30, -15, 0, 15, 30]
            for angle in angles:
                # Adjust spawn position slightly if needed, or just center
                game_state.bullets.append(Bullet(self.x + 40, self.y + 20, self.row, angle))
            self.last_action = now
