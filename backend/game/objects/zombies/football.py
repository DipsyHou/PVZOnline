from .base import Zombie
from ...config import PLANT_W

class FootballZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "football")
        self.hp = 200
        self.max_hp = 200
        self.speed = 40
        self.damage = 50
        self.armor = 1600
        self.max_armor = 1600

    
    def take_damage(self, amount):
        if self.armor > 0:
            self.armor -= amount
            if self.armor < 0:
                self.hp += self.armor
                self.armor = 0
        else:
            self.hp -= amount
