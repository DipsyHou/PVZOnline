import time
from ..base import GameObject
from ...config import CELL_W, CELL_H, PLANT_W, PLANT_H

class Plant(GameObject):
    def __init__(self, col, row, type_name):
        # Center the plant in the cell
        x = col * CELL_W + (CELL_W - PLANT_W) / 2
        y = row * CELL_H + (CELL_H - PLANT_H) / 2
        super().__init__(x, y, PLANT_W, PLANT_H, type_name)
        self.col = col
        self.row = row
        self.shoot_timer = 0
        self.shoot_interval = 1.5 # seconds
        self.cost = 0
        self.hp = 200
        self.max_hp = 200
        self.pumpkin = None # Attached pumpkin
        self.level = 0 # Evolution level (0-9)
        self.sleep_timer = 0 # 睡眠计时器

    def update(self, dt, game_state):
        # 咖啡豆加速的植物免疫睡眠
        if getattr(self, 'coffee_boosted', False):
            self.sleep_timer = 0
        
        # 更新睡眠状态
        if self.sleep_timer > 0:
            self.sleep_timer -= dt
        
        # 睡眠中的植物无法攻击
        if self.sleep_timer > 0:
            return
        
        # Basic shoot timer logic
        if self.shoot_interval > 0:
            self.shoot_timer += dt
            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                self.shoot(game_state)

    def shoot(self, game_state):
        pass
