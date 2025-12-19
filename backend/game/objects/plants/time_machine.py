from .base import Plant

class TimeMachine(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "time_machine")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0
        self.cost = 125
        self.float_timer = 3.0

    def update(self, dt, game_state):
        self.float_timer -= dt
        if self.float_timer <= 0:
            self.active = False
            
            # Find target plant
            target = None
            for p in game_state.plants:
                if p.col == self.col and p.row == self.row and p != self and p.active:
                    target = p
                    break
            
            if target:
                # Reset cooldown for ALL players
                if game_state.player_states:
                    for username in game_state.player_states:
                        if target.type in game_state.player_states[username]['cooldowns']:
                            del game_state.player_states[username]['cooldowns'][target.type]

                # Reset cooldown (Global/Legacy)
                if target.type in game_state.plant_cooldowns:
                    del game_state.plant_cooldowns[target.type]
