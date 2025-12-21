from .base import Plant

class Sunflower(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "sunflower")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 16.0
        self.cost = 50

    def shoot(self, game_state):
        # Add sun to game state
        if game_state.player_states:
            for username in game_state.player_states:
                game_state.player_states[username]['sun'] += 25
        else:
            game_state.sun += 25
        # In a real multiplayer game, we might want to spawn a sun object that needs to be clicked,
        # but for now, auto-collect is fine or direct addition.
        # The JS version added directly to `sun` variable.
