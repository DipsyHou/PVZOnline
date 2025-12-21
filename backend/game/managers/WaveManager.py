import time
import random
from game.constants import ROWS

class WaveManager:
    def __init__(self, zombie_manager, entity_manager):
        self.zm = zombie_manager
        self.em = entity_manager
        self.wave = 0
        # Next-wave countdown (seconds). New waves start on a fixed cadence.
        self.wave_timer = 20  # Start first wave after 20 seconds
        self.wave_interval = 30  # Fixed seconds between waves

        # Allow multiple waves to be active at the same time.
        # Each active wave has its own spawn queue and spawn timer.
        self.active_waves = []
        
        # Difficulty table by wave threshold.
        self.difficulty_map = {
            1: {"normal": 1.0},
            5: {"normal": 0.85, "buckethead": 0.15},
            8: {"normal": 0.70, "buckethead": 0.20, "exploder": 0.10},
            10: {"normal": 0.55, "buckethead": 0.18, "exploder": 0.12, "fisher": 0.08, "priest": 0.07},
            15: {"normal": 0.40, "buckethead": 0.18, "exploder": 0.12, "fisher": 0.10, "priest": 0.10, "football": 0.10},
            20: {"normal": 0.30, "buckethead": 0.17, "exploder": 0.12, "fisher": 0.10, "priest": 0.09, "football": 0.12, "football_forward": 0.10},
            25: {"normal": 0.22, "buckethead": 0.16, "exploder": 0.12, "fisher": 0.10, "priest": 0.10, "football": 0.12, "football_forward": 0.12, "gargantuar": 0.06},
        }

    def _get_available_weights(self):
        """Return a dict of {zombie_type: weight} for the current wave."""
        available = {"normal": 1.0}
        for w, spec in self.difficulty_map.items():
            if self.wave < w:
                continue

            available = spec

        # Remove any non-positive weights
        available = {k: float(v) for k, v in available.items() if float(v) > 0}
        return available or {"normal": 1.0}

    def _get_next_spawn_delay(self, wave_state) -> float:
        """Compute next spawn delay to try to finish the wave within its window."""
        zombies_left = len(wave_state["zombies_to_spawn"])
        if zombies_left <= 0:
            return 0

        elapsed = float(wave_state.get("time_in_wave", 0.0))
        target_duration = float(wave_state.get("target_duration", self.wave_interval))

        time_left = max(target_duration - elapsed, 0.0)
        if time_left <= 0:
            base = 0.05
        else:
            base = time_left / zombies_left

        # Small jitter so it doesn't look perfectly periodic.
        delay = base + random.uniform(-0.15, 0.15)

        # Clamp to keep gameplay reasonable.
        delay = max(0.05, min(2.0, delay))
        return delay

    def update(self, dt):
        self.wave_timer -= dt

        # Start waves on a fixed schedule, regardless of whether previous waves
        # have finished spawning.
        while self.wave_timer <= 0:
            self.start_next_wave()
            self.wave_timer += self.wave_interval

        # Update all active waves (multiple waves can spawn in parallel).
        if not self.active_waves:
            return

        for wave_state in list(self.active_waves):
            zombies_to_spawn = wave_state["zombies_to_spawn"]
            if not zombies_to_spawn:
                self.active_waves.remove(wave_state)
                continue

            wave_state["time_in_wave"] = float(wave_state.get("time_in_wave", 0.0)) + dt

            wave_state["spawn_timer"] -= dt
            if wave_state["spawn_timer"] > 0:
                continue

            z_type = zombies_to_spawn.pop(0)
            row = random.randint(0, ROWS - 1)
            self.zm.spawn_zombie(row, z_type)
            wave_state["spawn_timer"] = self._get_next_spawn_delay(wave_state)

    def start_next_wave(self):
        self.wave += 1
        
        # Calculate number of zombies based on wave
        count = -1 + int(self.wave * 2)
        
        # Determine available types with weights
        weights_map = self._get_available_weights()
        available_types = list(weights_map.keys())
        available_weights = [weights_map[t] for t in available_types]
        
        # Generate spawn list
        zombies_to_spawn = []
        for _ in range(count):
            zombies_to_spawn.append(random.choices(available_types, weights=available_weights, k=1)[0])

        # Shuffle
        random.shuffle(zombies_to_spawn)

        # Add as an active wave so multiple waves can spawn concurrently.
        self.active_waves.append({
            "wave": self.wave,
            "zombies_to_spawn": zombies_to_spawn,
            "spawn_timer": random.uniform(0.0, 0.3),
            "time_in_wave": 0.0,
            "target_duration": float(self.wave_interval),
        })
        
        # Notify players
        self.em.add_event({
            "type": "wave_start",
            "wave": self.wave,
            "count": count
        })
