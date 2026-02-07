"""
游戏配置文件 - 集中管理所有游戏常量和数值配置
"""

# ===== 游戏界面常量 =====
CELL_W = 100
CELL_H = 100
ROWS = 7
COLS = 11

# 衍生常量
SCREEN_WIDTH = (COLS + 1) * CELL_W
SCREEN_HEIGHT = ROWS * CELL_H

# 实体尺寸
PLANT_W = 80
PLANT_H = 80
ZOMBIE_W = 75
ZOMBIE_H = 100
BULLET_W = 20
BULLET_H = 20

# ===== 初始资源 =====
INITIAL_SUN = 200
INITIAL_BRAINS = 50

# ===== 资源生成速率 =====
# 脑子生成公式: base_rate * elapsed_minutes * (1 + elapsed_minutes / growth_factor)
BRAIN_BASE_RATE = 10
BRAIN_GROWTH_FACTOR = 4

# ===== 植物配置 =====
# category类型说明:
# - "normal": 普通植物，只能放在空格或有南瓜/悬浮植物的格子
# - "floating": 悬浮植物，可以放在任何格子上（不占用普通植物位置）
# - "carrier": 承载植物（如南瓜），可以和普通植物叠加

PLANT_CONFIGS = {
    "peashooter": {"cost": 100, "cooldown": 7, "category": "normal"},
    "acid_lemon": {"cost": 125, "cooldown": 7, "category": "normal"},
    "sunflower": {"cost": 50, "cooldown": 7, "category": "normal"},
    "grape_pult": {"cost": 225, "cooldown": 7, "category": "normal"},
    "pod_peashooter": {"cost": 225, "cooldown": 7, "category": "normal"},
    "bomber": {"cost": 200, "cooldown": 7, "category": "normal"},
    "torchwood": {"cost": 175, "cooldown": 7, "category": "normal"},
    "watermelon": {"cost": 300, "cooldown": 7, "category": "normal"},
    "iced_coconut": {"cost": 175, "cooldown": 30, "category": "floating"},
    "trumpet": {"cost": 50, "cooldown": 30, "category": "normal"},
    "pine_shooter": {"cost": 150, "cooldown": 7, "category": "normal"},
    "gold_bloom": {"cost": 150, "cooldown": 50, "category": "normal"},
    "spiky_pumpkin": {"cost": 150, "cooldown": 30, "category": "carrier"},
    "jalapeno_pair": {"cost": 225, "cooldown": 30, "category": "normal"},
    "mimic": {"cost": 325, "cooldown": 30, "category": "normal"},
    "reshaper": {"cost": 50, "cooldown": 30, "category": "floating"},
    "time_machine": {"cost": 125, "cooldown": 50, "category": "floating"},
    "laser_shroom": {"cost": 300, "cooldown": 15, "category": "normal"},
    "windmill": {"cost": 250, "cooldown": 30, "category": "normal"},
    "vine_trap": {"cost": 125, "cooldown": 30, "category": "normal"},
    "electrode_cherry": {"cost": 175, "cooldown": 15, "category": "normal"},
    "wild_gatling": {"cost": 450, "cooldown": 30, "category": "normal"},
    "ninja_nut": {"cost": 100, "cooldown": 30, "category": "normal"},
    "citron": {"cost": 200, "cooldown": 7, "category": "normal"},
    "corn_homing": {"cost": 375, "cooldown": 7, "category": "normal"},
    "corn_gatling": {"cost": 275, "cooldown": 7, "category": "normal"},
    "jelly": {"cost": 125, "cooldown": 7, "category": "normal"},
    "binary_tree": {"cost": 175, "cooldown": 7, "category": "normal"},
    "maguey": {"cost": 300, "cooldown": 15, "category": "normal"},
    "christmas_nut": {"cost": 50, "cooldown": 30, "category": "normal"},
    "sword_gourd": {"cost": 250, "cooldown": 30, "category": "normal"},
    "coffee_bean": {"cost": 75, "cooldown": 7, "category": "floating"},
}

# 辅助函数：获取植物类别
def get_plant_category(plant_type: str) -> str:
    """
    获取植物类别
    
    Args:
        plant_type: 植物类型名称
        
    Returns:
        植物类别: "normal", "floating", "carrier"
    """
    return PLANT_CONFIGS.get(plant_type, {}).get("category", "normal")

# ===== 僵尸配置 =====
ZOMBIE_CONFIGS = {
    "normal": {"cost": 50, "cooldown": 1},
    "buckethead": {"cost": 200, "cooldown": 1},
    "exploder": {"cost": 150, "cooldown": 1},
    "fisher": {"cost": 200, "cooldown": 1},
    "football": {"cost": 400, "cooldown": 1},
    "football_forward": {"cost": 600, "cooldown": 1},
    "gargantuar": {"cost": 900, "cooldown": 1},
    "priest": {"cost": 200, "cooldown": 1},
}

# ===== 游戏平衡性 =====
# 伤害倍率
FIRE_DAMAGE_MULTIPLIER = 2.0

# 火炮弹药配置
CORN_FIRE_DAMAGE = 40
CORN_FIRE_SPLASH_RADIUS = 100
CORN_FIRE_SPLASH_DAMAGE = 40

# ===== 房间配置 =====
ROOM_EMPTY_TIMEOUT = 30  # 秒 - 房间无人自动删除时间
ROOM_RECONNECT_BUFFER = 1  # 秒 - 游戏中断线重连缓冲时间

# ===== 默认装备 =====
DEFAULT_PLANTS = ["peashooter", "sunflower", "pod_peashooter", "watermelon", "pine_shooter"]
DEFAULT_ZOMBIES = ["normal", "buckethead", "exploder"]
