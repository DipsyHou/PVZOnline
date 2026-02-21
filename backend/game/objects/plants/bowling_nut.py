from .base import Plant
from ...config import SCREEN_HEIGHT, SCREEN_WIDTH, ZOMBIE_W, ZOMBIE_H
import random

class BowlingNut(Plant):
    """
    坚果保龄球 - 弹跳攻击悬浮植物
    
    机制：
    - 悬浮植物，放置后立刻向右滚动
    - 碰到僵尸造成100点伤害，随机向右上或右下方向弹跳
    - 碰到上下边界反弹（横向速度不变，纵向速度反向）
    - 无限穿透，直到飞出屏幕
    """
    
    def __init__(self, col, row):
        super().__init__(col, row, "bowling_nut")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0  # 不射击
        self.cost = 50
        
        # 滚动状态
        self.rolling = True
        self.vx = 200  # 向右速度
        self.vy = 0    # 初始纵向速度为0
        self.hit_zombies = set()  # 当前已击中的僵尸ID集合
        self.hit_count = 0  # 总击中次数
        self.max_hits = 10  # 最大击中次数，避免无限滚动

    def update(self, dt, game_state):
        if not self.rolling:
            return
        
        # 更新位置
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # 检查上下边界碰撞并反弹
        if self.y <= 0:
            self.y = 0
            self.vy = -self.vy  # 纵向速度反向
        elif self.y + self.h >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.h
            self.vy = -self.vy  # 纵向速度反向
        
        # 检查是否飞出屏幕右侧或达到最大击中次数
        if self.x > SCREEN_WIDTH or self.hit_count >= self.max_hits:
            self.active = False
            return
        
        # 检查僵尸碰撞
        for z in game_state.zombies:
            if not z.active or z.hp <= 0:
                continue
            
            offset = 15  # 碰撞检测偏移，避免判断过于宽松
            # 碰撞检测
            if (self.x + self.w > z.x + offset and 
                self.x + offset < z.x + ZOMBIE_W and 
                self.y + self.h > z.y +offset and 
                self.y + offset < z.y + ZOMBIE_H):
                
                # 如果已经击中过这个僵尸，跳过
                if z.id in self.hit_zombies:
                    continue
                
                # 造成伤害
                z.take_damage(100)
                
                # 记录击中
                self.hit_zombies.add(z.id)
                self.hit_count += 1
                
                # 碰撞后纵向速度
                if self.vy > 0:
                    # 当前向下或静止，弹跳后向上
                    self.vy = -150
                elif self.vy < 0:
                    # 当前向上，弹跳后向下
                    self.vy = 150
                else:
                    # 当前静止，随机选择向上或向下弹跳
                    self.vy = random.choice([-150, 150])
                


                # 添加碰撞特效
                game_state.add_event({
                    "type": "particle",
                    "x": self.x + self.w / 2,
                    "y": self.y + self.h / 2,
                    "kind": "bowling_hit"
                })
                
                # 检查是否达到最大击中次数
                if self.hit_count >= self.max_hits:
                    self.active = False
                    return
                
                break  # 每帧只处理一次碰撞
