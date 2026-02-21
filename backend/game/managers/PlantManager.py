import time
from typing import Dict, Optional
from game.factories import PlantFactory
from game.config import PLANT_CONFIGS, get_plant_category

class PlantManager:
    """植物管理器 - 使用工厂模式动态加载植物"""
    
    def __init__(self, entity_manager):
        self.em = entity_manager
        self.plant_info = PLANT_CONFIGS
    
    def _get_category(self, plant_type: str) -> str:
        """获取植物类别"""
        return get_plant_category(plant_type)

    def handle_place_plant(self, data: Dict, username: Optional[str] = None) -> None:
        """
        处理种植植物请求
        
        Args:
            data: 包含col, row, plant_type的字典
            username: 玩家用户名
        """
        c, r = data['col'], data['row']
        plant_type = data.get('plant_type', 'peashooter')
        
        info = self.plant_info.get(plant_type)
        if not info: 
            return

        cost = info["cost"]
        cooldown = info["cooldown"]
        now = time.time()

        # Determine resources based on user
        if username and username in self.em.player_states:
            p_state = self.em.player_states[username]
            current_sun = p_state['sun']
            cooldowns = p_state['cooldowns']
        else:
            current_sun = self.em.sun
            cooldowns = self.em.plant_cooldowns

        # Check cooldown
        if now < cooldowns.get(plant_type, 0):
            return

        if current_sun >= cost:
            # Determine effective type for placement rules
            effective_type = plant_type
            if plant_type == "mimic":
                # 模仿者只模仿自己上一次放置的植物
                last_type = None
                if username and username in self.em.player_states:
                    last_type = self.em.player_states[username].get('last_planted_type')
                else:
                    last_type = self.em.last_planted_type
                
                if not last_type: 
                    return
                effective_type = last_type

            # Check placement validity using category system
            existing_plants = [p for p in self.em.plants if p.col == c and p.row == r]
            can_place = False
            
            category = self._get_category(effective_type)
            
            if category == "floating":
                # 悬浮植物：每格最多1个悬浮植物（任意类型）
                has_floating = any(self._get_category(p.type) == "floating" for p in existing_plants)
                if not has_floating:
                    can_place = True
            
            elif category == "carrier":
                # 承载植物：每格只能有1个承载植物
                has_carrier = any(self._get_category(p.type) == "carrier" for p in existing_plants)
                if not has_carrier:
                    can_place = True
            
            else:  # category == "normal"
                # 普通植物：只能放在空格或只有carrier/floating的格子
                has_normal = any(self._get_category(p.type) == "normal" for p in existing_plants)
                if not has_normal:
                    can_place = True

            if can_place:
                # 使用工厂模式创建植物
                level = 0
                if username and username in self.em.player_states:
                    lvl_map = self.em.player_states[username].get('plant_levels', {})
                    level = int(lvl_map.get(plant_type, 0))
                
                new_plant = PlantFactory.create_plant(plant_type, c, r, level)
                if not new_plant:
                    return
                
                new_plant.owner = username  # Set owner
                
                if plant_type == "mimic":
                    # 模仿者使用玩家的last_planted_type
                    if username and username in self.em.player_states:
                        new_plant.mimic_target = self.em.player_states[username].get('last_planted_type')
                    else:
                        new_plant.mimic_target = self.em.last_planted_type
                else:
                    # 更新玩家的last_planted_type
                    if username and username in self.em.player_states:
                        self.em.player_states[username]['last_planted_type'] = plant_type
                    else:
                        self.em.last_planted_type = plant_type
                    
                self.em.plants.append(new_plant)
                
                # Deduct resources
                if username and username in self.em.player_states:
                    self.em.player_states[username]['sun'] -= cost
                    self.em.player_states[username]['cooldowns'][plant_type] = now + cooldown
                else:
                    self.em.sun -= cost
                    self.em.plant_cooldowns[plant_type] = now + cooldown

    def handle_shovel(self, data: Dict) -> None:
        """
        处理铲除植物
        
        Args:
            data: 包含col, row, is_bottom的字典
        """
        c, r = data['col'], data['row']
        is_bottom = data.get('is_bottom', False)
        
        # Find plants at this location
        plants_at_loc = [p for p in self.em.plants if p.col == c and p.row == r]
        
        if not plants_at_loc:
            return

        # 使用category系统区分植物
        # 优先级:
        # If is_bottom: Carrier -> Normal -> Floating
        # If !is_bottom: Normal -> Carrier -> Floating
        
        carrier = next((p for p in plants_at_loc if self._get_category(p.type) == "carrier"), None)
        normal_plant = next((p for p in plants_at_loc if self._get_category(p.type) == "normal"), None)
        floating = next((p for p in plants_at_loc if self._get_category(p.type) == "floating"), None)
        
        if is_bottom:
            # 底层点击：优先铲除承载植物
            target = carrier or normal_plant or floating
        else:
            # 顶层点击：优先铲除普通植物
            target = normal_plant or carrier or floating
        
        if target:
            target.hp = 0
            target.active = False

    def handle_activate_plant(self, data: Dict) -> None:
        """激活植物特殊能力"""
        c, r = data['col'], data['row']
        for p in self.em.plants:
            if p.col == c and p.row == r:
                if hasattr(p, 'activate'):
                    p.activate(self.em)
                break

    def handle_mouse_position(self, data: Dict, username: Optional[str] = None) -> None:
        """
        更新所有需要鼠标位置的植物（用于养剑葫等）
        只更新属于该玩家的植物
        
        Args:
            data: 包含mouse_x, mouse_y的字典
            username: 玩家用户名
        """
        mouse_x = data.get('mouse_x')
        mouse_y = data.get('mouse_y')
        
        if mouse_x is None or mouse_y is None:
            return
        
        # 只更新属于该玩家的、支持鼠标位置的植物
        for p in self.em.plants:
            if hasattr(p, 'set_mouse_position'):
                # 检查植物所有者
                plant_owner = getattr(p, 'owner', None)
                if plant_owner == username or (plant_owner is None and username is None):
                    p.set_mouse_position(mouse_x, mouse_y)

    def update(self, dt):
        for p in self.em.plants:
            p.update(dt, self.em)
        
        # Cleanup dead plants
        dead_plants = [p for p in self.em.plants if p.hp <= 0 or not p.active]
        for p in dead_plants:
            if hasattr(p, 'on_death'):
                p.on_death(self.em)

        self.em.plants = [p for p in self.em.plants if p.hp > 0 and p.active]
            
    def transform_plant(self, old_plant, new_type: str) -> None:
        """
        将植物转换为新类型（用于Mimic等）
        
        Args:
            old_plant: 旧植物实例
            new_type: 新植物类型
        """
        info = self.plant_info.get(new_type)
        if not info: 
            return
        
        # 使用工厂模式创建新植物
        new_plant = PlantFactory.create_plant(new_type, old_plant.col, old_plant.row)
        if not new_plant:
            return
        
        # 继承原植物的所有者
        new_plant.owner = getattr(old_plant, 'owner', None)
        
        if old_plant in self.em.plants:
            idx = self.em.plants.index(old_plant)
            self.em.plants[idx] = new_plant
            
            # Event for transformation effect
            self.em.add_event({
                "type": "particle",
                "x": new_plant.x + new_plant.w/2,
                "y": new_plant.y + new_plant.h/2,
                "kind": "mimic_transform"
            })
