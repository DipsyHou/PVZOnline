"""
工厂模式 - 动态加载植物和僵尸类
"""
import importlib
from typing import Dict, Type, Optional
from game.objects.plants.base import Plant
from game.objects.zombies.base import Zombie


class PlantFactory:
    """植物工厂 - 动态加载植物类"""
    
    _plant_classes: Dict[str, Type[Plant]] = {}
    
    @classmethod
    def register_plant(cls, plant_type: str) -> None:
        """
        动态注册植物类
        
        Args:
            plant_type: 植物类型名称，如 'peashooter'
        """
        if plant_type in cls._plant_classes:
            return
        
        try:
            # 转换类名: peashooter -> Peashooter
            class_name = ''.join(word.capitalize() for word in plant_type.split('_'))
            
            # 动态导入模块
            module = importlib.import_module(f'game.objects.plants.{plant_type}')
            plant_class = getattr(module, class_name)
            
            cls._plant_classes[plant_type] = plant_class
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Failed to load plant '{plant_type}': {e}")
    
    @classmethod
    def create_plant(cls, plant_type: str, col: int, row: int, level: int = 0) -> Optional[Plant]:
        """
        创建植物实例
        
        Args:
            plant_type: 植物类型
            col: 列位置
            row: 行位置
            level: 进化等级
            
        Returns:
            Plant实例或None
        """
        if plant_type not in cls._plant_classes:
            cls.register_plant(plant_type)
        
        plant_class = cls._plant_classes.get(plant_type)
        if not plant_class:
            return None
        
        plant = plant_class(col, row)
        plant.level = level
        return plant
    
    @classmethod
    def get_available_plants(cls) -> list:
        """获取所有已注册的植物类型"""
        return list(cls._plant_classes.keys())


class ZombieFactory:
    """僵尸工厂 - 动态加载僵尸类"""
    
    _zombie_classes: Dict[str, Type[Zombie]] = {}
    
    @classmethod
    def register_zombie(cls, zombie_type: str) -> None:
        """
        动态注册僵尸类
        
        Args:
            zombie_type: 僵尸类型名称，如 'normal', 'buckethead'
        """
        if zombie_type in cls._zombie_classes:
            return
        
        try:
            # 转换类名: normal -> NormalZombie, buckethead -> BucketheadZombie
            class_name = ''.join(word.capitalize() for word in zombie_type.split('_')) + 'Zombie'
            
            # 动态导入模块
            module = importlib.import_module(f'game.objects.zombies.{zombie_type}')
            zombie_class = getattr(module, class_name)
            
            cls._zombie_classes[zombie_type] = zombie_class
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Failed to load zombie '{zombie_type}': {e}")
    
    @classmethod
    def create_zombie(cls, zombie_type: str, row: int) -> Optional[Zombie]:
        """
        创建僵尸实例
        
        Args:
            zombie_type: 僵尸类型
            row: 行位置
            
        Returns:
            Zombie实例或None
        """
        if zombie_type not in cls._zombie_classes:
            cls.register_zombie(zombie_type)
        
        zombie_class = cls._zombie_classes.get(zombie_type)
        if not zombie_class:
            return None
        
        return zombie_class(row)
    
    @classmethod
    def get_available_zombies(cls) -> list:
        """获取所有已注册的僵尸类型"""
        return list(cls._zombie_classes.keys())
