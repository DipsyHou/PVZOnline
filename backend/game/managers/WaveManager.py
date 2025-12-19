import time
import random
from game.constants import ROWS

class WaveManager:
    def __init__(self, zombie_manager, entity_manager):
        self.zm = zombie_manager
        self.em = entity_manager
        self.wave = 0
        self.wave_timer = 5 # Start first wave after 5 seconds
        self.wave_interval = 20 # seconds between waves
        self.zombies_to_spawn = []
        self.spawn_timer = 0
        
        # Difficulty weights (higher wave -> more difficult zombies)
        self.difficulty_map = {
            1: ["normal"],
            5: ["normal", "buckethead"],
            8: ["normal", "buckethead", "exploder"],
            10: ["normal", "buckethead", "exploder", "fisher", "priest"],
            15: ["normal", "buckethead", "exploder", "fisher", "priest", "football"],
            20: ["normal", "buckethead", "exploder", "fisher", "priest", "football", "football_forward"],
            25: ["normal", "buckethead", "exploder", "fisher", "priest", "football", "football_forward", "gargantuar"]
        }

    def update(self, dt):
        self.wave_timer -= dt
        
        if self.wave_timer <= 0 and not self.zombies_to_spawn:
            self.start_next_wave()
            
        if self.zombies_to_spawn:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                z_type = self.zombies_to_spawn.pop(0)
                row = random.randint(0, ROWS - 1)
                self.zm.spawn_zombie(row, z_type)
                self.spawn_timer = random.uniform(0.5, 2.0) # Random interval

    def start_next_wave(self):
        self.wave += 1
        self.wave_timer = self.wave_interval
        
        # Calculate number of zombies based on wave
        count = -1 + int(self.wave * 2)
        
        # Determine available types
        available_types = ["normal"]
        for w, types in self.difficulty_map.items():
            if self.wave >= w:
                available_types = types
        
        # Generate spawn list
        self.zombies_to_spawn = []
        for _ in range(count):
            self.zombies_to_spawn.append(random.choice(available_types))
            
        # Shuffle
        random.shuffle(self.zombies_to_spawn)
        
        # Notify players
        self.em.add_event({
            "type": "wave_start",
            "wave": self.wave,
            "count": count
        })
