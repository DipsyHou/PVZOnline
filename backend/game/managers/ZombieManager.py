import time
from typing import Dict, Optional
from game.factories import ZombieFactory
from game.config import ZOMBIE_CONFIGS, INITIAL_BRAINS, BRAIN_BASE_RATE, BRAIN_GROWTH_FACTOR

class ZombieManager:
    """僵尸管理器 - 使用工厂模式动态加载僵尸"""
    
    def __init__(self, entity_manager):
        self.em = entity_manager
        self.zombie_info = ZOMBIE_CONFIGS

    def handle_spawn_zombie(self, data: Dict) -> None:
        """
        处理生成僵尸请求
        
        Args:
            data: 包含row, zombie_type的字典
        """
        r = data['row']
        z_type = data.get('zombie_type', 'normal')
        
        info = self.zombie_info.get(z_type)
        if not info: 
            return

        cost = info["cost"]
        cooldown = info["cooldown"]
        now = time.time()

        if now < self.em.zombie_cooldowns.get(z_type, 0):
            return

        if self.em.brains >= cost:
            # 使用工厂模式创建僵尸
            new_zombie = ZombieFactory.create_zombie(z_type, r)
            if new_zombie:
                self.em.zombies.append(new_zombie)
                self.em.brains -= cost
                self.em.zombie_cooldowns[z_type] = now + cooldown

    def spawn_zombie(self, row: int, z_type: str) -> None:
        """
        直接生成僵尸（用于波次系统）
        
        Args:
            row: 行位置
            z_type: 僵尸类型
        """
        new_zombie = ZombieFactory.create_zombie(z_type, row)
        if new_zombie:
            self.em.zombies.append(new_zombie)

    def update(self, now: float, dt: float, start_time: float) -> None:
        """
        更新所有僵尸
        
        Args:
            now: 当前时间戳
            dt: 时间增量
            start_time: 游戏开始时间
        """
        # Brain generation - 使用配置常量
        elapsed_minutes = (now - start_time) / 60
        if elapsed_minutes > 0:
            brain_rate = BRAIN_BASE_RATE * elapsed_minutes * (1 + elapsed_minutes / BRAIN_GROWTH_FACTOR)
            self.em.brains += brain_rate * dt

        for z in self.em.zombies:
            z.update(now, dt, self.em)
            
        # Cleanup dead zombies
        self.em.zombies = [z for z in self.em.zombies if z.hp > 0 and z.active]
