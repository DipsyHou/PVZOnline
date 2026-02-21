from .base import Plant

class SpikyPumpkin(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "spiky_pumpkin")
        self.hp = 2000
        self.max_hp = 2000
        self.shoot_interval = 0
        self.cost = 150
