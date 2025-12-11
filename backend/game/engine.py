import time
from typing import List
from game.objects.plants.peashooter import Peashooter
from game.objects.plants.sunflower import Sunflower
from game.objects.plants.pod_peashooter import PodPeashooter
from game.objects.zombies.normal import NormalZombie
from game.objects.bullet import Bullet
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_W, BULLET_H, ZOMBIE_W, ZOMBIE_H

class Game:
    def __init__(self, settings: dict, roles: dict):
        self.settings = settings
        self.roles = roles
        self.plants = []
        self.zombies = []
        self.bullets = []
        self.last_time = time.time()
        self.sun = 2000  # Initial sun
        self.plant_cooldowns = {} # type -> available_time

    def handle_command(self, username: str, data: dict):
        role = self.roles.get(username)
        if role == "plant" and data['type'] == 'place_plant':
            c, r = data['col'], data['row']
            plant_type = data.get('plant_type', 'peashooter')
            
            # Define costs and cooldowns
            plant_info = {
                "peashooter": {"cost": 100, "cooldown": 0, "class": Peashooter},
                "sunflower": {"cost": 50, "cooldown": 0, "class": Sunflower},
                "pod_peashooter": {"cost": 225, "cooldown": 7, "class": PodPeashooter}
            }
            
            info = plant_info.get(plant_type)
            if not info: return

            cost = info["cost"]
            cooldown = info["cooldown"]
            now = time.time()

            # Check cooldown
            if now < self.plant_cooldowns.get(plant_type, 0):
                return

            if self.sun >= cost:
                if not any(p.col == c and p.row == r for p in self.plants):
                    self.plants.append(info["class"](c, r))
                    self.sun -= cost
                    self.plant_cooldowns[plant_type] = now + cooldown
        elif role == "zombie" and data['type'] == 'spawn_zombie':
            r = data['row']
            self.zombies.append(NormalZombie(r))

    def update(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        
        # Game Logic
        for p in self.plants:
            p.update(now, self)

        for z in self.zombies:
            z.update(now, dt, self)

        for b in self.bullets:
            if hasattr(b, 'vx'):
                b.x += b.vx * dt
                b.y += b.vy * dt
            else:
                b.x += b.speed * dt

            if b.x > SCREEN_WIDTH or b.x < 0 or b.y > SCREEN_HEIGHT or b.y < 0: 
                b.active = False
            
            for z in self.zombies:
                if b.x + BULLET_W > z.x and b.x < z.x + ZOMBIE_W and b.y + BULLET_H > z.y and b.y < z.y + ZOMBIE_H:
                    b.active = False
                    z.hp -= 20
                    if z.hp <= 0: z.active = False
                    break

        self.plants = [p for p in self.plants if p.active]
        self.zombies = [z for z in self.zombies if z.active]
        self.bullets = [b for b in self.bullets if b.active]

    def get_state(self, full_sync=True):
        now = time.time()
        remaining_cooldowns = {}
        for p_type, avail_time in self.plant_cooldowns.items():
            rem = avail_time - now
            if rem > 0:
                remaining_cooldowns[p_type] = rem
        
        # Helper for rounding
        def r(val): return round(val, 1)

        # Plants: Static, so only send full data on full_sync
        if full_sync:
            plants_data = [{"id": p.id, "x": int(p.x), "y": int(p.y), "type": p.type, "hp": int(p.hp), "max_hp": p.max_hp} for p in self.plants]
        else:
            # Only send ID and HP for updates
            plants_data = [{"id": p.id, "x": int(p.x), "y": int(p.y), "hp": int(p.hp)} for p in self.plants]

        return {
            "type": "game_state",
            "sun": self.sun,
            "plants": plants_data,
            "zombies": [{"id": z.id, "x": r(z.x), "y": r(z.y), "type": z.type, "hp": int(z.hp), "max_hp": z.max_hp} for z in self.zombies],
            "bullets": [{"id": b.id, "x": int(b.x), "y": int(b.y)} for b in self.bullets],
            "roles": self.roles,
            "cooldowns": remaining_cooldowns
        }
