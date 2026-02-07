import time
from game.managers.EntityManager import EntityManager
from game.managers.PlantManager import PlantManager
from game.managers.ZombieManager import ZombieManager
from game.managers.BulletManager import BulletManager
from game.managers.WaveManager import WaveManager

class Game:
    def __init__(self, settings: dict, roles: dict, player_decks=None):
        self.em = EntityManager()
        self.em.reset(settings, roles, player_decks)
        
        self.plant_manager = PlantManager(self.em)
        self.zombie_manager = ZombieManager(self.em)
        self.bullet_manager = BulletManager(self.em)
        
        self.mode = settings.get('mode', 'pve')
        if self.mode == 'endless':
            self.wave_manager = WaveManager(self.zombie_manager, self.em)
        else:
            self.wave_manager = None
        
        # For compatibility with plants calling game.transform_plant
        self.em.transform_plant = self.plant_manager.transform_plant
        
        self.start_time = time.time()

    def handle_command(self, username: str, data: dict):
        role = self.em.roles.get(username)
        if role == "plant":
            if data['type'] == 'place_plant':
                self.plant_manager.handle_place_plant(data, username)
            elif data['type'] == 'activate_plant':
                self.plant_manager.handle_activate_plant(data)
            elif data['type'] == 'shovel':
                self.plant_manager.handle_shovel(data)
            elif data['type'] == 'mouse_position':
                self.plant_manager.handle_mouse_position(data)
        elif role == "zombie":
            if data['type'] == 'spawn_zombie':
                self.zombie_manager.handle_spawn_zombie(data)

    def update(self):
        self.em.events = [] # Clear events
        now = time.time()
        dt = now - (self.last_time if hasattr(self, 'last_time') else now)
        self.last_time = now
        
        if self.wave_manager:
            self.wave_manager.update(dt)

        self.plant_manager.update(dt)
        self.zombie_manager.update(now, dt, self.start_time)
        self.bullet_manager.update(dt)

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
            if hasattr(p, 'shoot_interval'): data['shoot_interval'] = p.shoot_interval
            if hasattr(p, 'base_interval'): data['base_interval'] = p.base_interval
            if hasattr(p, 'min_interval'): data['min_interval'] = p.min_interval
            if hasattr(p, 'life_timer'): data['life_timer'] = p.life_timer
            if hasattr(p, 'mimic_timer'): data['mimic_timer'] = p.mimic_timer
            if hasattr(p, 'float_timer'): data['float_timer'] = p.float_timer
            if hasattr(p, 'charge_time'): data['charge_time'] = p.charge_time
            if hasattr(p, 'laser_active_time'): data['laser_active_time'] = p.laser_active_time
            if hasattr(p, 'paired_id'): data['paired_id'] = p.paired_id
            plant_data.append(data)

        zombie_data = []
        for z in self.em.zombies:
            z_data = {
                "id": z.id, "x": r(z.x), "y": r(z.y), "type": z.type, 
                "hp": int(z.hp), "max_hp": z.max_hp, 
                "armor": getattr(z, 'armor', 0), "max_armor": getattr(z, 'max_armor', 0), 
                "is_slowed": z.slow_timer > 0, "is_stunned": z.stun_timer > 0
            }
            if hasattr(z, 'smash_timer'): z_data['smash_timer'] = z.smash_timer
            if hasattr(z, 'is_hooking'): z_data['is_hooking'] = z.is_hooking
            if hasattr(z, 'hook_target_id'): z_data['hook_target_id'] = z.hook_target_id
            if hasattr(z, 'hook_charge_time'): z_data['hook_charge_time'] = z.hook_charge_time
            if hasattr(z, 'heal_target_id'): z_data['heal_target_id'] = z.heal_target_id
            zombie_data.append(z_data)

        bullet_data = []
        for b in self.em.bullets:
            data = {
                "id": b.id,
                "x": int(b.x),
                "y": int(b.y),
                "w": b.w,
                "h": b.h,
                "type": b.type
            }
            if hasattr(b, 'is_fire'): data['is_fire'] = b.is_fire
            if hasattr(b, 'angle'): data['angle'] = b.angle
            if hasattr(b, 'vx'): data['vx'] = b.vx
            if hasattr(b, 'vy'): data['vy'] = b.vy
            bullet_data.append(data)

        return {
            "type": "game_state",
            "sun": self.em.sun,
            "brains": int(self.em.brains),
            "player_states": self.em.get_processed_player_states(now),
            "plants": plant_data,
            "zombies": zombie_data,
            "bullets": bullet_data,
            "roles": self.em.roles,
            "cooldowns": remaining_cooldowns,
            "events": self.em.events
        }
