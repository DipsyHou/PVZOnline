from .base import Zombie

class BucketheadZombie(Zombie):
    def __init__(self, row):
        super().__init__(row, "buckethead")
        self.hp = 200
        self.max_hp = 200
        self.speed = 20
        self.damage = 50
        self.armor = 1000
        self.max_armor = 1000
