import math
from .base import GameObject
from ..constants import BULLET_W, BULLET_H, CELL_W, CELL_H, ROWS, COLS

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
        
        # Parabolic
        self.start_x = x
        self.start_y = y
        self.target_x = None
        self.target_y = None
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

    def update(self, dt, game_state):
        self.elapsed += dt
        
        # Torchwood interaction
        if self.kind in ["pea", "needle", "corn", "branch"] and not self.is_fire:
            c = int(self.x / CELL_W)
            r = int(self.y / CELL_H)
            if 0 <= r < ROWS and 0 <= c < COLS:
                # Find torchwood at this location
                for p in game_state.plants:
                    if p.col == c and p.row == r and p.type == "torchwood":
                        self.is_fire = True
                        if self.kind == "corn":
                            self.damage = 40
                            self.splash_radius = 100 # approximate
                            self.splash_damage = 40
                        else:
                            self.damage *= 2
                        break

        # Homing Logic
        if self.homing and self.target and self.target.hp > 0:
            tx = self.target.x + self.target.w / 2
            ty = self.target.y + self.target.h / 2
            dx = tx - self.x
            dy = ty - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                speed = math.sqrt(self.vx**2 + self.vy**2)
                turn_rate = 5 * dt
                
                current_angle = math.atan2(self.vy, self.vx)
                target_angle = math.atan2(dy, dx)
                
                diff = target_angle - current_angle
                while diff < -math.pi: diff += math.pi * 2
                while diff > math.pi: diff -= math.pi * 2
                
                new_angle = current_angle + max(-turn_rate, min(turn_rate, diff))
                self.vx = math.cos(new_angle) * speed
                self.vy = math.sin(new_angle) * speed

        # Movement
        if self.total_time:
            # Parabolic
            t = min(self.elapsed, self.total_time)
            self.x = self.start_x + self.vx * t
            self.y = self.start_y + self.vy * t + 0.5 * self.gravity * t * t
        else:
            # Linear
            self.x += self.vx * dt
            self.y += self.vy * dt
