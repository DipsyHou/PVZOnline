from .base import Plant

class GoldBloom(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "gold_bloom")
        self.hp = 50
        self.max_hp = 50
        self.shoot_interval = 0
        self.cost = 150
        self.life_timer = 0

    def update(self, dt, game_state):
        self.life_timer += dt
        if self.life_timer >= 8.0:
            if game_state.player_states:
                for username in game_state.player_states:
                    game_state.player_states[username]['sun'] += 500
            else:
                game_state.sun += 500
            self.active = False
