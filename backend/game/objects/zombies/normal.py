from .base import Zombie
from ...constants import PLANT_W

class NormalZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "normal")
        self.hp = 200
        self.max_hp = 200
        self.speed = 20
        self.damage = 20

    def update(self, now, dt, game_state):
        eating = False
        for p in game_state.plants:
            if p.row == self.row and abs(self.x - p.x - PLANT_W/2) < PLANT_W/2:
                eating = True
                p.hp -= self.damage * dt
                if p.hp <= 0: p.active = False
                break
        if not eating:
            self.x -= self.speed * dt
