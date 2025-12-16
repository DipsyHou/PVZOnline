from .base import Zombie
from ...constants import PLANT_W

class GargantuarZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "gargantuar")
        self.hp = 4500
        self.max_hp = 4500
        self.speed = 15
        self.damage = 50
