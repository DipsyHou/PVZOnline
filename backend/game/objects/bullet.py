import math
from .base import GameObject
from ..config import BULLET_W, BULLET_H

class Bullet(GameObject):
    def __init__(self, x, y, row, vx, vy, damage, kind="pea"):
        super().__init__(x, y, BULLET_W, BULLET_H, kind)
        self.row = row
        self.vx = vx
        self.vy = vy
        self.damage = damage
        self.kind = kind
        self.is_fire = False
        self.angle = math.atan2(vy, vx)
        
        # Collision properties
        self.pierce = 0
        self.hit_set = set()
        
        # Status effects
        self.stun = 0
        self.knockback_dist = 0
        self.knockback_duration = 0
        self.slow_duration = 0
        self.slow_factor = 1.0
        
        # Parabolic (Lobbed)
        self.start_x = x
        self.start_y = y
        self.target_x = None
        self.target_y = None
        self.target_id = None
        self.total_time = None
        self.elapsed = 0
        self.gravity = 1200
        
        # Homing
        self.homing = False
        self.target = None
        
        # Splash
        self.splash_radius = 0
        self.splash_damage = 0
        
        # Branch (Binary Tree)
        self.branch_level = 0
        self.height = 0
        
        # Spawner properties (e.g. for grape)
        self.burst_index = 0
        self.directions = None
        
        # Ignore specific zombie
        self.ignore_zombie_id = None

    @property
    def is_lobbed(self):
        return self.total_time is not None

    @property
    def is_passable_through_fire(self):
        return self.kind in ["pea", "needle", "corn", "branch"]

