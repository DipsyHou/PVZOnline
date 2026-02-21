import math
from .base import Plant
from ..bullet import Bullet

class WildGatling(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "wild_gatling")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 2.0
        self.cost = 450
        self.burst_index = 0
        self.burst_timer = 0
        self.is_bursting = False

    def update(self, dt, game_state):
        # 处理连发逻辑
        if self.is_bursting:
            self.burst_timer += dt
            # Bursts at 0.15, 0.30, 0.45, 0.60
            burst_times = [0.15, 0.30, 0.45, 0.60]
            
            while self.burst_index < 4 and self.burst_timer >= burst_times[self.burst_index]:
                self.fire_burst(game_state)
                self.burst_index += 1
            
            if self.burst_index >= 4:
                self.is_bursting = False
        
        # 调用基类 update（处理 shoot_timer 和 shoot 调用）
        super().update(dt, game_state)

    def shoot(self, game_state):
        # 检查是否有目标
        has_target = False
        for z in game_state.zombies:
            if z.row == self.row and z.x > self.x:
                has_target = True
                break
        
        if has_target:
            # 开始连发
            self.is_bursting = True
            self.burst_index = 0
            self.burst_timer = 0

    def fire_burst(self, game_state):
        bx = self.x + 40
        by = self.y + 20
        speed = 360
        angles = [-15, 0, 15]
        
        for deg in angles:
            rad = math.radians(deg)
            vx = math.cos(rad) * speed
            vy = math.sin(rad) * speed
            b = Bullet(bx, by, self.row, vx, vy, 20, "pea")
            game_state.bullets.append(b)
