from .base import Zombie
from ...constants import PLANT_W

class FisherZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "fisher")
        self.hp = 200
        self.max_hp = 200
        self.speed = 20
        self.damage = 50
