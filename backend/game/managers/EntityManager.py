from typing import Dict, List, Any, Optional
from game.config import INITIAL_SUN, INITIAL_BRAINS

class EntityManager:
    """实体管理器 - 管理所有游戏实体和资源"""
    
    def __init__(self):
        self.plants: List[Any] = []
        self.zombies: List[Any] = []
        self.bullets: List[Any] = []
        self.sun: int = INITIAL_SUN
        self.brains: int = INITIAL_BRAINS
        self.plant_cooldowns: Dict[str, float] = {}
        self.zombie_cooldowns: Dict[str, float] = {}
        self.events: List[Dict[str, Any]] = []
        self.last_planted_type: Optional[str] = None
        self.roles: Dict[str, str] = {}
        self.settings: Dict[str, Any] = {}
        self.player_states: Dict[str, Dict[str, Any]] = {}

    def reset(self, settings: Dict[str, Any], roles: Dict[str, str], player_decks: Optional[Dict] = None) -> None:
        """
        重置游戏状态
        
        Args:
            settings: 游戏设置
            roles: 玩家角色分配
            player_decks: 玩家卡组配置
        """
        self.settings = settings
        self.roles = roles
        self.plants = []
        self.zombies = []
        self.bullets = []
        self.sun = INITIAL_SUN  # Legacy/Global fallback
        self.brains = INITIAL_BRAINS
        self.plant_cooldowns = {}  # Legacy/Global fallback
        self.zombie_cooldowns = {}
        self.events = []
        self.last_planted_type = None
        
        # Per-player state
        self.player_states = {}
        for user, role in roles.items():
            if role == 'plant':
                lvl_map = {}
                if player_decks and user in player_decks:
                    lvl_map = player_decks[user].get('plant_levels', {}) or {}
                self.player_states[user] = {
                    'sun': INITIAL_SUN,
                    'cooldowns': {},
                    'plant_levels': lvl_map
                }

    def add_event(self, event: Dict[str, Any]) -> None:
        """
        添加游戏事件
        
        Args:
            event: 事件数据字典
        """
        self.events.append(event)

    def get_processed_player_states(self, now: float) -> Dict[str, Dict[str, Any]]:
        """
        获取处理后的玩家状态（包含剩余冷却时间）
        
        Args:
            now: 当前时间戳
            
        Returns:
            处理后的玩家状态字典
        """
        processed = {}
        if hasattr(self, 'player_states') and self.player_states:
            for user, state in self.player_states.items():
                processed[user] = {
                    'sun': state['sun'],
                    'cooldowns': {}
                }
                for p_type, avail_time in state['cooldowns'].items():
                    rem = avail_time - now
                    if rem > 0:
                        processed[user]['cooldowns'][p_type] = rem
        return processed
