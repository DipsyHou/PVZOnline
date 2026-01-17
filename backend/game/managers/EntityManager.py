class EntityManager:
    def __init__(self):
        self.plants = []
        self.zombies = []
        self.bullets = []
        self.sun = 200
        self.brains = 50
        self.plant_cooldowns = {}
        self.zombie_cooldowns = {}
        self.events = []
        self.last_planted_type = None
        self.roles = {}
        self.settings = {}

    def reset(self, settings, roles, player_decks=None):
        self.settings = settings
        self.roles = roles
        self.plants = []
        self.zombies = []
        self.bullets = []
        self.sun = 200 # Legacy/Global fallback
        self.brains = 50
        self.plant_cooldowns = {} # Legacy/Global fallback
        self.zombie_cooldowns = {}
        self.events = []
        self.last_planted_type = None
        
        # Per-player state
        self.player_states = {}
        for user, role in roles.items():
            if role == 'plant':
                lvl_map = {}
                if player_decks and user in player_decks:
                    lvl_map = player_decks[user].get('plant_levels', {}) or {}
                self.player_states[user] = {
                    'sun': 200,
                    'cooldowns': {},
                    'plant_levels': lvl_map
                }
        self.last_planted_type = None

    def add_event(self, event):
        self.events.append(event)

    def get_processed_player_states(self, now):
        processed = {}
        if hasattr(self, 'player_states') and self.player_states:
            for user, state in self.player_states.items():
                processed[user] = {
                    'sun': state['sun'],
                    'cooldowns': {}
                }
                for p_type, avail_time in state['cooldowns'].items():
                    rem = avail_time - now
                    if rem > 0:
                        processed[user]['cooldowns'][p_type] = rem
        return processed
