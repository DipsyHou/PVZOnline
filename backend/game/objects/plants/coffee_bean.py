from .base import Plant

class CoffeeBean(Plant):
    """
    咖啡豆 - 攻速增益悬浮植物
    
    机制：
    - 悬浮植物，可放置在其他植物上方
    - 使本格植物攻速翻倍（shoot_interval减半）
    - 持续15秒后消失
    """
    
    def __init__(self, col, row):
        super().__init__(col, row, "coffee_bean")
        self.hp = 100
        self.max_hp = 100
        self.shoot_interval = 0  # 不射击
        self.cost = 75
        self.duration = 15.0  # 持续时间
        self.life_timer = 0
        self.boosted_plant = None  # 被加速的植物
        self.has_applied_boost = False
    
    def update(self, dt, game_state):
        """更新生命计时"""
        self.life_timer += dt
        
        # 应用加速效果（只在第一次）
        if not self.has_applied_boost:
            self.apply_boost(game_state)
            self.has_applied_boost = True
        
        # 时间到后消失
        if self.life_timer >= self.duration:
            self.active = False
            self.remove_boost()
    
    def apply_boost(self, game_state):
        """应用攻速加成"""
        # 查找同格的其他植物
        for p in game_state.plants:
            if p.col == self.col and p.row == self.row and p.id != self.id:
                # 跳过不需要射击的植物
                if p.shoot_interval == 0:
                    continue
                
                # 跳过已经被加速的植物
                if getattr(p, 'coffee_boosted', False):
                    continue
                
                p.original_shoot_interval = p.shoot_interval  # 记录原始射速

                # 特殊处理玉米机枪
                if p.type == 'corn_gatling':
                    p.original_base_interval = p.base_interval
                    p.original_min_interval = p.min_interval
                    p.base_interval *= 0.5
                    p.min_interval *= 0.5
                    p.shoot_interval *= 0.5
                else:
                    # 普通植物直接减半
                    p.shoot_interval *= 0.5
                
                # 标记植物
                p.coffee_boosted = True
                
                self.boosted_plant = p
                break
    
    def remove_boost(self):
        """移除攻速加成"""
        if self.boosted_plant and hasattr(self.boosted_plant, 'coffee_boosted'):
            p = self.boosted_plant
            
            # 恢复原始射速
            if hasattr(p, 'original_shoot_interval'):
                p.shoot_interval = p.original_shoot_interval
                delattr(p, 'original_shoot_interval')
            
            # 特殊处理玉米机枪
            if p.type == 'corn_gatling':
                if hasattr(p, 'original_base_interval'):
                    p.base_interval = p.original_base_interval
                    delattr(p, 'original_base_interval')
                if hasattr(p, 'original_min_interval'):
                    p.min_interval = p.original_min_interval
                    delattr(p, 'original_min_interval')
            
            # 移除标记
            p.coffee_boosted = False
    
    def on_death(self, game_state):
        """被铲掉时也要移除加成"""
        self.remove_boost()
