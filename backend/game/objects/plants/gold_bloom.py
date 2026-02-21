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
        if getattr(self, 'coffee_boosted', False):
            self.sleep_timer = 0
        if self.sleep_timer > 0:
            self.sleep_timer -= dt
            return

        self.life_timer += dt
        if self.life_timer >= 8.0:
            # 计算植物玩家数量
            plant_player_count = sum(1 for role in game_state.roles.values() if role == 'plant')
            
            # 双人植物玩家时产出减半
            sun_amount = 500 // 2 if plant_player_count >= 2 else 500
            
            if game_state.player_states:
                for username in game_state.player_states:
                    game_state.player_states[username]['sun'] += sun_amount
            else:
                game_state.sun += sun_amount
            self.active = False
