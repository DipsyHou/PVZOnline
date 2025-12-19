import time
from game.objects.zombies.normal import NormalZombie
from game.objects.zombies.buckethead import BucketheadZombie
from game.objects.zombies.exploder import ExploderZombie
from game.objects.zombies.fisher import FisherZombie
from game.objects.zombies.football import FootballZombie
from game.objects.zombies.football_forward import FootballForwardZombie
from game.objects.zombies.gargantuar import GargantuarZombie
from game.objects.zombies.priest import PriestZombie

class ZombieManager:
    def __init__(self, entity_manager):
        self.em = entity_manager
        self.zombie_info = {
            "normal": {"cost": 50, "cooldown": 1, "class": NormalZombie},
            "buckethead": {"cost": 200, "cooldown": 1, "class": BucketheadZombie},
            "exploder": {"cost": 150, "cooldown": 1, "class": ExploderZombie},
            "fisher": {"cost": 200, "cooldown": 1, "class": FisherZombie},
            "football": {"cost": 400, "cooldown": 1, "class": FootballZombie},
            "football_forward": {"cost": 600, "cooldown": 1, "class": FootballForwardZombie},
            "gargantuar": {"cost": 900, "cooldown": 1, "class": GargantuarZombie},
            "priest": {"cost": 200, "cooldown": 1, "class": PriestZombie},
        }

    def handle_spawn_zombie(self, data):
        r = data['row']
        z_type = data.get('zombie_type', 'normal')
        
        info = self.zombie_info.get(z_type)
        if not info: return

        cost = info["cost"]
        cooldown = info["cooldown"]
        now = time.time()

        if now < self.em.zombie_cooldowns.get(z_type, 0):
            return

        if self.em.brains >= cost:
            self.em.zombies.append(info["class"](r))
            self.em.brains -= cost
            self.em.zombie_cooldowns[z_type] = now + cooldown

    def spawn_zombie(self, row, z_type):
        info = self.zombie_info.get(z_type)
        if info:
            self.em.zombies.append(info["class"](row))

    def update(self, now, dt):
        for z in self.em.zombies:
            z.update(now, dt, self.em)
