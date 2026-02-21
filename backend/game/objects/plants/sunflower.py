from .base import Plant

class Sunflower(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "sunflower")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 16.0
        self.cost = 50

    def shoot(self, game_state):
        # 计算植物玩家数量
        plant_player_count = sum(1 for role in game_state.roles.values() if role == 'plant')
        
        # 双人植物玩家时产出减半
        sun_amount = 25 // 2 if plant_player_count >= 2 else 25
        
        # Add sun to game state
        if game_state.player_states:
            for username in game_state.player_states:
                game_state.player_states[username]['sun'] += sun_amount
        else:
            game_state.sun += sun_amount
        # In a real multiplayer game, we might want to spawn a sun object that needs to be clicked,
        # but for now, auto-collect is fine or direct addition.
        # The JS version added directly to `sun` variable.
