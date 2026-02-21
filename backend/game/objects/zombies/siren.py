from .base import Zombie
from ...config import get_plant_category

class SirenZombie(Zombie):
    """海妖僵尸 - 吹响海螺使本行植物陷入睡眠"""
    
    def __init__(self, row):
        super().__init__(row, "siren")
        self.hp = 400
        self.max_hp = 400
        self.speed = 20
        self.damage = 50
        
        # 技能相关
        self.skill_cooldown = 0
        self.skill_interval = 10.0  # 技能CD 10秒
        self.skill_casting = False
        self.skill_cast_timer = 0
        self.skill_cast_duration = 2.0  # 吹响海螺需要2秒
        
    def update(self, now, dt, game_state):
        # 技能CD更新
        if self.skill_cooldown > 0:
            self.skill_cooldown -= dt
        
        # 施法过程
        if self.skill_casting:
            # 更新状态计时器（击退和眩晕会中断施法）
            if self.slow_timer > 0: self.slow_timer -= dt
            if self.stun_timer > 0: self.stun_timer -= dt
            if self.knockback_timer > 0: self.knockback_timer -= dt
            
            # 被击退或眩晕，中断施法
            if self.knockback_timer > 0 or self.stun_timer > 0:
                self.skill_casting = False
                self.skill_cast_timer = 0
                # 调用基类处理击退/眩晕
                super().update(now, dt, game_state)
                return
            
            # 继续施法
            self.skill_cast_timer += dt
            if self.skill_cast_timer >= self.skill_cast_duration:
                # 施法完成，使本行所有植物睡眠
                self._apply_sleep_to_plants(game_state)
                self.skill_casting = False
                self.skill_cast_timer = 0
                self.skill_cooldown = self.skill_interval
            return  # 施法时不移动
        
        # 检测是否应该开始施法
        if self.skill_cooldown <= 0 and self._has_plants_in_row(game_state):
            self.skill_casting = True
            self.skill_cast_timer = 0
            return
        
        # 没有施法，执行基类的正常逻辑（移动、啃食等）
        super().update(now, dt, game_state)
    
    def _has_plants_in_row(self, game_state):
        """检查本行是否有植物"""
        for p in game_state.plants:
            if p.row == self.row and p.active and get_plant_category(p.type) != "floating":
                return True
        return False
    
    def _apply_sleep_to_plants(self, game_state):
        """使本行所有植物陷入睡眠5秒（悬浮植物除外）"""
        for p in game_state.plants:
            if p.row == self.row and p.active:
                # 悬浮植物免疫睡眠
                if get_plant_category(p.type) == "floating":
                    continue
                p.sleep_timer = 5.0  # 睡眠5秒
