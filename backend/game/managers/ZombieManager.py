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
            "normal": {"cost": 50, "cooldown": 5, "class": NormalZombie},
            "buckethead": {"cost": 125, "cooldown": 10, "class": BucketheadZombie},
            "exploder": {"cost": 150, "cooldown": 15, "class": ExploderZombie},
            "fisher": {"cost": 175, "cooldown": 15, "class": FisherZombie},
            "football": {"cost": 175, "cooldown": 15, "class": FootballZombie},
            "football_forward": {"cost": 150, "cooldown": 15, "class": FootballForwardZombie},
            "gargantuar": {"cost": 300, "cooldown": 30, "class": GargantuarZombie},
            "priest": {"cost": 150, "cooldown": 15, "class": PriestZombie},
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

    def update(self, now, dt):
        for z in self.em.zombies:
            z.update(now, dt, self.em)
