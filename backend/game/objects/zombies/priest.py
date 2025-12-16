from .base import Zombie
from ...constants import PLANT_W

class PriestZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "priest")
        self.hp = 200
        self.max_hp = 200
        self.speed = 20
        self.damage = 50
