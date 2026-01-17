import time
from game.objects.plants.peashooter import Peashooter
from game.objects.plants.sunflower import Sunflower
from game.objects.plants.pod_peashooter import PodPeashooter
from game.objects.plants.bomber import Bomber
from game.objects.plants.torchwood import Torchwood
from game.objects.plants.watermelon import Watermelon
from game.objects.plants.iced_coconut import IcedCoconut
from game.objects.plants.trumpet import Trumpet
from game.objects.plants.pine_shooter import PineShooter
from game.objects.plants.gold_bloom import GoldBloom
from game.objects.plants.spiky_pumpkin import SpikyPumpkin
from game.objects.plants.jalapeno_pair import JalapenoPair
from game.objects.plants.mimic import Mimic
from game.objects.plants.reshaper import Reshaper
from game.objects.plants.time_machine import TimeMachine
from game.objects.plants.laser_shroom import LaserShroom
from game.objects.plants.windmill import Windmill
from game.objects.plants.vine_trap import VineTrap
from game.objects.plants.electrode_cherry import ElectrodeCherry
from game.objects.plants.wild_gatling import WildGatling
from game.objects.plants.ninja_nut import NinjaNut
from game.objects.plants.citron import Citron
from game.objects.plants.corn_homing import CornHoming
from game.objects.plants.corn_gatling import CornGatling
from game.objects.plants.jelly import Jelly
from game.objects.plants.binary_tree import BinaryTree
from game.objects.plants.maguey import Maguey
from game.objects.plants.christmas_nut import ChristmasNut
from game.objects.plants.grape_pult import GrapePult
from game.objects.plants.acid_lemon import AcidLemon

class PlantManager:
    def __init__(self, entity_manager):
        self.em = entity_manager
        self.plant_info = {
            "peashooter": {"cost": 100, "cooldown": 7, "class": Peashooter},
            "acid_lemon": {"cost": 125, "cooldown": 7, "class": AcidLemon},
            "sunflower": {"cost": 50, "cooldown": 7, "class": Sunflower},
            "grape_pult": {"cost": 225, "cooldown": 7, "class": GrapePult},
            "pod_peashooter": {"cost": 225, "cooldown": 7, "class": PodPeashooter},
            "bomber": {"cost": 200, "cooldown": 7, "class": Bomber},
            "torchwood": {"cost": 175, "cooldown": 7, "class": Torchwood},
            "watermelon": {"cost": 300, "cooldown": 7, "class": Watermelon},
            "iced_coconut": {"cost": 175, "cooldown": 30, "class": IcedCoconut},
            "trumpet": {"cost": 50, "cooldown": 30, "class": Trumpet},
            "pine_shooter": {"cost": 150, "cooldown": 7, "class": PineShooter},
            "gold_bloom": {"cost": 150, "cooldown": 50, "class": GoldBloom},
            "spiky_pumpkin": {"cost": 150, "cooldown": 30, "class": SpikyPumpkin},
            "jalapeno_pair": {"cost": 225, "cooldown": 30, "class": JalapenoPair},
            "mimic": {"cost": 325, "cooldown": 30, "class": Mimic},
            "reshaper": {"cost": 50, "cooldown": 30, "class": Reshaper},
            "time_machine": {"cost": 125, "cooldown": 50, "class": TimeMachine},
            "laser_shroom": {"cost": 300, "cooldown": 15, "class": LaserShroom},
            "windmill": {"cost": 250, "cooldown": 30, "class": Windmill},
            "vine_trap": {"cost": 125, "cooldown": 30, "class": VineTrap},
            "electrode_cherry": {"cost": 175, "cooldown": 15, "class": ElectrodeCherry},
            "wild_gatling": {"cost": 450, "cooldown": 30, "class": WildGatling},
            "ninja_nut": {"cost": 100, "cooldown": 30, "class": NinjaNut},
            "citron": {"cost": 200, "cooldown": 7, "class": Citron},
            "corn_homing": {"cost": 375, "cooldown": 7, "class": CornHoming},
            "corn_gatling": {"cost": 275, "cooldown": 7, "class": CornGatling},
            "jelly": {"cost": 125, "cooldown": 7, "class": Jelly},
            "binary_tree": {"cost": 175, "cooldown": 7, "class": BinaryTree},
            "maguey": {"cost": 300, "cooldown": 15, "class": Maguey},
            "christmas_nut": {"cost": 50, "cooldown": 30, "class": ChristmasNut},
        }

    def handle_place_plant(self, data, username=None):
        c, r = data['col'], data['row']
        plant_type = data.get('plant_type', 'peashooter')
        
        info = self.plant_info.get(plant_type)
        if not info: return

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
                if not self.em.last_planted_type: return
                effective_type = self.em.last_planted_type

            # Check placement validity
            existing_plants = [p for p in self.em.plants if p.col == c and p.row == r]
            can_place = False
            
            if effective_type in ["time_machine", "reshaper"]:
                # Floating plants can be placed anywhere (limit 1 per type per cell?)
                if not any(p.type == effective_type for p in existing_plants):
                    can_place = True
            
            elif effective_type == "spiky_pumpkin":
                # Can place if no pumpkin exists
                if not any(p.type == "spiky_pumpkin" for p in existing_plants):
                    can_place = True
            
            else:
                # Normal plant
                # Can place if cell is empty OR only has pumpkin/floating
                has_normal = any(p.type not in ["spiky_pumpkin", "time_machine", "reshaper"] for p in existing_plants)
                if not has_normal:
                    can_place = True

            if can_place:
                new_plant = info["class"](c, r)
                if username and username in self.em.player_states:
                    lvl_map = self.em.player_states[username].get('plant_levels', {})
                    new_plant.level = int(lvl_map.get(plant_type, 0))
                else:
                    new_plant.level = 0
                new_plant.owner = username # Set owner
                
                if plant_type == "mimic":
                    new_plant.mimic_target = self.em.last_planted_type
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

    def handle_shovel(self, data):
        c, r = data['col'], data['row']
        is_bottom = data.get('is_bottom', False)
        
        # Find plants at this location
        plants_at_loc = [p for p in self.em.plants if p.col == c and p.row == r]
        
        if not plants_at_loc:
            return

        # Priority: 
        # If is_bottom: Pumpkin -> Normal -> Floating
        # If !is_bottom: Normal -> Pumpkin -> Floating
        
        pumpkin = next((p for p in plants_at_loc if p.type == "spiky_pumpkin"), None)
        normal_plant = next((p for p in plants_at_loc if p.type not in ["spiky_pumpkin", "time_machine", "reshaper"]), None)
        
        if is_bottom:
            if pumpkin:
                pumpkin.hp = 0
                pumpkin.active = False
                return
            if normal_plant:
                normal_plant.hp = 0
                normal_plant.active = False
                return
        else:
            if normal_plant:
                normal_plant.hp = 0
                normal_plant.active = False
                return
            if pumpkin:
                pumpkin.hp = 0
                pumpkin.active = False
                return

        # If only floating plants left, remove the first one found
        if plants_at_loc:
            plants_at_loc[0].hp = 0
            plants_at_loc[0].active = False

    def handle_activate_plant(self, data):
        c, r = data['col'], data['row']
        for p in self.em.plants:
            if p.col == c and p.row == r:
                if hasattr(p, 'activate'):
                    p.activate(self.em)
                break

    def update(self, dt):
        for p in self.em.plants:
            p.update(dt, self.em)
        
        # Cleanup dead plants
        dead_plants = [p for p in self.em.plants if p.hp <= 0 or not p.active]
        for p in dead_plants:
            if hasattr(p, 'on_death'):
                p.on_death(self.em)

        self.em.plants = [p for p in self.em.plants if p.hp > 0 and p.active]
            
    def transform_plant(self, old_plant, new_type):
        info = self.plant_info.get(new_type)
        if not info: return
        
        new_class = info["class"]
        new_plant = new_class(old_plant.col, old_plant.row)
        
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
