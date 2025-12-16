class EntityManager:
    def __init__(self):
        self.plants = []
        self.zombies = []
        self.bullets = []
        self.sun = 2000
        self.brains = 2000
        self.plant_cooldowns = {}
        self.zombie_cooldowns = {}
        self.events = []
        self.last_planted_type = None
        self.roles = {}
        self.settings = {}

    def reset(self, settings, roles):
        self.settings = settings
        self.roles = roles
        self.plants = []
        self.zombies = []
        self.bullets = []
        self.sun = 2000
        self.brains = 2000
        self.plant_cooldowns = {}
        self.zombie_cooldowns = {}
        self.events = []
        self.last_planted_type = None

    def add_event(self, event):
        self.events.append(event)
