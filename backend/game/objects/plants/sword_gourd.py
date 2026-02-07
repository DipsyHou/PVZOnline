from .base import Plant
from ..bullet import Bullet

class SwordGourd(Plant):
    """
    养剑葫 - 发射追踪鼠标的飞剑
    
    机制：
    - 每15秒向鼠标位置发射飞剑
    - 飞剑持续追踪鼠标位置
    - 穿透敌人造成伤害
    - 存在时间10秒或飞出画面消失
    """
    
    def __init__(self, col, row):
        super().__init__(col, row, "sword_gourd")
        self.hp = 200
        self.max_hp = 200
        self.cost = 250
        self.shoot_interval = 5.0  # 5秒发射一次
        self.shoot_timer = 0
        
        # 鼠标位置（需要前端传递）
        self.target_x = None
        self.target_y = None

    def update(self, dt, game_state):
        """更新射击计时器"""
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.shoot(game_state)

    def shoot(self, game_state):
        """发射飞剑"""
        # 如果没有鼠标位置，默认向右发射
        if self.target_x is None or self.target_y is None:
            target_x = self.x + 500
            target_y = self.y + self.h / 2
        else:
            target_x = self.target_x
            target_y = self.target_y
        
        # 计算初始速度方向
        dx = target_x - (self.x + self.w / 2)
        dy = target_y - (self.y + self.h / 2)
        dist = (dx * dx + dy * dy) ** 0.5
        
        if dist > 0:
            speed = 360  # 飞剑速度
            vx = (dx / dist) * speed
            vy = (dy / dist) * speed
        else:
            vx = 360
            vy = 0
        
        # 创建飞剑子弹
        bx = self.x + self.w / 2
        by = self.y + self.h / 2
        
        b = Bullet(bx, by, self.row, vx, vy, 20, "flying_sword")
        b.w = 40
        b.h = 15
        b.pierce = 9999  # 无限穿透
        b.homing = True  # 启用追踪
        b.target = None  # 不追踪僵尸，追踪鼠标位置
        b.max_distance = 0  # 不限制距离
        b.life_time = 0  # 记录存在时间
        b.max_life_time = 10.0  # 10秒后开始返回
        b.is_sword = True  # 标记为飞剑
        b.is_returning = False  # 是否正在返回葫芦
        b.hit_set_clear_timer = 0  # hit_set清空计时器
        
        # 记录植物ID用于鼠标位置更新和返回
        b.plant_id = self.id
        
        game_state.bullets.append(b)
        
        # 添加发射事件
        game_state.add_event({
            "type": "sword_launch",
            "x": bx,
            "y": by,
            "target_x": target_x,
            "target_y": target_y
        })

    def set_mouse_position(self, x, y):
        """设置鼠标位置（由前端调用）"""
        self.target_x = x
        self.target_y = y
