from .base import Zombie
from ...constants import PLANT_W

class ExploderZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "exploder")
        self.hp = 200
        self.max_hp = 200
        self.speed = 40
        self.damage = 500
