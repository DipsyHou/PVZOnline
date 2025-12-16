from .base import Zombie
from ...constants import PLANT_W

class FootballForwardZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "football_forward")
        self.hp = 200
        self.max_hp = 200
        self.speed = 50
        self.damage = 50
