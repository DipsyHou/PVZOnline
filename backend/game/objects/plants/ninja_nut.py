from .base import Plant

class NinjaNut(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "ninja_nut")
        self.hp = 4000
        self.max_hp = 4000
        self.shoot_interval = float('inf')
        self.cost = 100
        self.has_spawned_extras = False

    def update(self, dt, game_state):
        if not self.has_spawned_extras:
            self.has_spawned_extras = True
            offsets = [
                (0, -1), (0, 1), (1, 0), (1, -1), (1, 1), (-1, 0), (-1, -1), (-1, 1)
            ]
            spawned_count = 0
            for dc, dr in offsets:
                if spawned_count >= 2:
                    break
                target_col = self.col + dc
                target_row = self.row + dr
                
                if 0 <= target_col < 11 and 0 <= target_row < 7:
                    # Check if empty
                    if not any(p.col == target_col and p.row == target_row for p in game_state.plants):
                        # Create new NinjaNut
                        new_plant = NinjaNut(target_col, target_row)
                        new_plant.has_spawned_extras = True
                        game_state.plants.append(new_plant)
                        spawned_count += 1
