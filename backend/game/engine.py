import time
from game.managers.EntityManager import EntityManager
from game.managers.PlantManager import PlantManager
from game.managers.ZombieManager import ZombieManager
from game.managers.BulletManager import BulletManager

class Game:
    def __init__(self, settings: dict, roles: dict):
        self.em = EntityManager()
        self.em.reset(settings, roles)
        
        self.plant_manager = PlantManager(self.em)
        self.zombie_manager = ZombieManager(self.em)
        self.bullet_manager = BulletManager(self.em)
        
        # For compatibility with plants calling game.transform_plant
        self.em.transform_plant = self.plant_manager.transform_plant

    def handle_command(self, username: str, data: dict):
        role = self.em.roles.get(username)
        if role == "plant":
            if data['type'] == 'place_plant':
                self.plant_manager.handle_place_plant(data)
            elif data['type'] == 'activate_plant':
                self.plant_manager.handle_activate_plant(data)
        elif role == "zombie":
            if data['type'] == 'spawn_zombie':
                self.zombie_manager.handle_spawn_zombie(data)

    def update(self):
        self.em.events = [] # Clear events
        now = time.time()
        dt = now - (self.last_time if hasattr(self, 'last_time') else now)
        self.last_time = now
        
        self.plant_manager.update(dt)
        self.zombie_manager.update(now, dt)
        self.bullet_manager.update(dt)
        
        # Cleanup dead objects
        self.em.plants = [p for p in self.em.plants if p.hp > 0 and p.active]
        self.em.zombies = [z for z in self.em.zombies if z.hp > 0 and z.active]
        self.em.bullets = [b for b in self.em.bullets if b.active]

    def get_state(self):
        now = time.time()
        remaining_cooldowns = {}
        for p_type, avail_time in self.em.plant_cooldowns.items():
            rem = avail_time - now
            if rem > 0:
                remaining_cooldowns[p_type] = rem
        for z_type, avail_time in self.em.zombie_cooldowns.items():
            rem = avail_time - now
            if rem > 0:
                remaining_cooldowns[z_type] = rem
        
        def r(val): return round(val, 1)

        plant_data = []
        for p in self.em.plants:
            data = {
                "id": p.id, "x": int(p.x), "y": int(p.y), "type": p.type, 
                "hp": int(p.hp), "max_hp": p.max_hp
            }
            if hasattr(p, 'shoot_timer'): data['shoot_timer'] = p.shoot_timer
            if hasattr(p, 'shoot_interval'): 
                if p.shoot_interval == float('inf'):
                    data['shoot_interval'] = 0
                else:
                    data['shoot_interval'] = p.shoot_interval
            if hasattr(p, 'life_timer'): data['life_timer'] = p.life_timer
            if hasattr(p, 'mimic_timer'): data['mimic_timer'] = p.mimic_timer
            if hasattr(p, 'float_timer'): data['float_timer'] = p.float_timer
            if hasattr(p, 'charge_time'): data['charge_time'] = p.charge_time
            if hasattr(p, 'laser_active_time'): data['laser_active_time'] = p.laser_active_time
            if hasattr(p, 'paired_id'): data['paired_id'] = p.paired_id
            plant_data.append(data)

        return {
            "type": "game_state",
            "sun": self.em.sun,
            "brains": self.em.brains,
            "plants": plant_data,
            "zombies": [{"id": z.id, "x": r(z.x), "y": r(z.y), "type": z.type, "hp": int(z.hp), "max_hp": z.max_hp, "armor": getattr(z, 'armor', 0), "max_armor": getattr(z, 'max_armor', 0), "is_slowed": z.slow_timer > 0, "is_stunned": z.stun_timer > 0} for z in self.em.zombies],
            "bullets": [{"id": b.id, "x": int(b.x), "y": int(b.y), "w": b.w, "h": b.h, "type": b.type, "is_fire": getattr(b, 'is_fire', False), "angle": getattr(b, 'angle', 0)} for b in self.em.bullets],
            "roles": self.em.roles,
            "cooldowns": remaining_cooldowns,
            "events": self.em.events
        }
