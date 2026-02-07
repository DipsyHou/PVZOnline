from .base import Zombie

class NormalZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "normal")
        self.hp = 200
        self.max_hp = 200
        self.speed = 20
        self.damage = 50
