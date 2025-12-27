from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, ZOMBIE_W, ZOMBIE_H, CELL_W, CELL_H, ROWS, COLS
from game.objects.bullet import Bullet
import random
import math

class BulletManager:
    def __init__(self, entity_manager):
        self.em = entity_manager

    def update(self, dt):
        # Iterate over a copy of the list to avoid issues with appending during iteration
        for b in self.em.bullets[:]:
            self.update_bullet_position(b, dt)
            
            if self.is_out_of_bounds(b):
                b.active = False
                continue

            if hasattr(b, 'max_distance') and b.max_distance > 0:
                dist = ((b.x - b.start_x)**2 + (b.y - b.start_y)**2)**0.5
                if dist >= b.max_distance:
                    b.active = False
                    continue

            if b.kind == "grape_spawner":
                self.handle_grape_spawner(b)
                continue

            if b.is_lobbed:
                self.handle_lobbed_collision(b)
            else:
                self.handle_straight_collision(b)

        # Cleanup dead bullets
        self.em.bullets = [b for b in self.em.bullets if b.active]

    def update_bullet_position(self, b, dt):
        b.elapsed += dt

        # Homing Logic
        if b.homing and b.target and b.target.hp > 0:
            tx = b.target.x + b.target.w / 2
            ty = b.target.y + b.target.h / 2
            dx = tx - b.x
            dy = ty - b.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                speed = math.sqrt(b.vx**2 + b.vy**2)
                turn_rate = 5 * dt
                
                current_angle = math.atan2(b.vy, b.vx)
                target_angle = math.atan2(dy, dx)
                
                diff = target_angle - current_angle
                while diff < -math.pi: diff += math.pi * 2
                while diff > math.pi: diff -= math.pi * 2
                
                new_angle = current_angle + max(-turn_rate, min(turn_rate, diff))
                b.vx = math.cos(new_angle) * speed
                b.vy = math.sin(new_angle) * speed

        # Movement
        if b.is_lobbed:
            # Parabolic
            t = min(b.elapsed, b.total_time)
            b.x = b.start_x + b.vx * t
            b.y = b.start_y + b.vy * t + 0.5 * b.gravity * t * t
        else:
            # Linear
            b.x += b.vx * dt
            b.y += b.vy * dt

    def is_out_of_bounds(self, b):
        return b.x > SCREEN_WIDTH or b.x < -100 or b.y > SCREEN_HEIGHT or b.y < -1000

    def handle_straight_collision(self, b):
        # Torchwood Interaction
        if b.is_passable_through_fire and not b.is_fire:
            c = int(b.x / CELL_W)
            r = int(b.y / CELL_H)
            if 0 <= r < ROWS and 0 <= c < COLS:
                for p in self.em.plants:
                    if p.col == c and p.row == r and p.type == "torchwood":
                        b.is_fire = True
                        if b.kind == "corn":
                            b.damage = 40
                            b.splash_radius = 100
                            b.splash_damage = 40
                        else:
                            b.damage *= 2
                        break

        # Zombie Collision
        for z in self.em.zombies:
            if b.active and b.x + b.w > z.x and b.x < z.x + ZOMBIE_W and b.y + b.h > z.y and b.y < z.y + ZOMBIE_H:
                if z.id in b.hit_set: continue
                if hasattr(b, 'ignore_zombie_id') and b.ignore_zombie_id == z.id: continue
                
                z.take_damage(b.damage)
                b.hit_set.add(z.id)

                # Splash for straight bullets (e.g. fire corn)
                if b.splash_radius > 0:
                    self.apply_splash(b, z.x + ZOMBIE_W/2, z.y + ZOMBIE_H/2, ignore_id=z.id)
                
                # Special Effects
                self.apply_status_effects(b, z)
                self.handle_special_on_hit(b)

                if b.pierce <= 0:
                    b.active = False
                    break
                else:
                    b.pierce -= 1

    def handle_lobbed_collision(self, b):
        if b.total_time and b.elapsed >= b.total_time:
            b.active = False
            hit_zombie_id = None
            
            # Guaranteed hit on target
            if hasattr(b, 'target_id') and b.target_id:
                target_z = next((z for z in self.em.zombies if z.id == b.target_id), None)
                if target_z:
                    target_z.take_damage(b.damage)
                    hit_zombie_id = target_z.id
                    if b.slow_duration > 0: target_z.apply_slow(b.slow_duration, b.slow_factor)
            
            # If no target locked, check direct hit (e.g. if target died but bullet still lands)
            if hit_zombie_id is None:
                 for z in self.em.zombies:
                    if b.x + b.w > z.x and b.x < z.x + ZOMBIE_W and b.y + b.h > z.y and b.y < z.y + ZOMBIE_H:
                        z.take_damage(b.damage)
                        hit_zombie_id = z.id
                        if b.slow_duration > 0: z.apply_slow(b.slow_duration, b.slow_factor)
                        break

            # Splash Logic
            if b.splash_radius > 0:
                self.apply_splash(b, b.x, b.y, ignore_id=hit_zombie_id)
            
                self.em.add_event({
                    "type": "particle", 
                    "x": b.x, 
                    "y": b.y, 
                    "kind": b.kind + "_splash"
                })

            self.handle_special_on_hit(b, hit_zombie_id)

    def apply_splash(self, b, x, y, ignore_id=None):
        for z in self.em.zombies:
            if z.id == ignore_id: continue
            dx = (z.x + ZOMBIE_W/2) - x
            dy = (z.y + ZOMBIE_H/2) - y
            dist = (dx**2 + dy**2)**0.5
            if dist <= b.splash_radius:
                z.take_damage(b.splash_damage)
                if b.slow_duration > 0: z.apply_slow(b.slow_duration, b.slow_factor)

    def apply_status_effects(self, b, z):
        if b.stun > 0: z.apply_stun(b.stun)
        if b.slow_duration > 0: z.apply_slow(b.slow_duration, b.slow_factor)
        if b.knockback_dist > 0: z.apply_knockback(b.knockback_dist, b.knockback_duration)

    def handle_special_on_hit(self, b, hit_zombie_id=None):
        if b.kind == "branch":
            if b.height > 0:
                speed = 400
                vy = 100
                
                b1 = Bullet(b.x, b.y, b.row, speed, -vy, 20, "branch")
                b1.branch_level = b.branch_level + 1
                b1.height = b.height - 1
                b1.is_fire = b.is_fire
                if b1.is_fire: b1.damage *= 2
                b1.hit_set = b.hit_set.copy()
                self.em.bullets.append(b1)
                
                b2 = Bullet(b.x, b.y, b.row, speed, vy, 20, "branch")
                b2.branch_level = b.branch_level + 1
                b2.height = b.height - 1
                b2.is_fire = b.is_fire
                if b2.is_fire: b2.damage *= 2
                b2.hit_set = b.hit_set.copy()
                self.em.bullets.append(b2)
            
            b.active = False

        elif b.kind == "grape":
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random.shuffle(directions)
            
            # Add 2 random directions
            all_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            directions.extend([random.choice(all_dirs) for _ in range(2)])
            
            # Create a spawner bullet that stays at impact location
            spawner = Bullet(b.x - 10, b.y, b.row, 0, 0, 0, "grape_spawner")
            spawner.directions = directions
            if hit_zombie_id is not None:
                spawner.ignore_zombie_id = hit_zombie_id
            self.em.bullets.append(spawner)

    def handle_grape_spawner(self, b):
        burst_times = [0, 0, 0, 0, 0.1, 0.2]
        
        while b.burst_index < len(burst_times) and b.elapsed >= burst_times[b.burst_index]:
            if b.directions and b.burst_index < len(b.directions):
                dx, dy = b.directions[b.burst_index]
                speed = 400
                vx = dx * speed
                vy = dy * speed
                
                sb = Bullet(b.x, b.y, b.row, vx, vy, 20, "grape_small")
                if b.ignore_zombie_id is not None:
                    sb.ignore_zombie_id = b.ignore_zombie_id
                self.em.bullets.append(sb)
            
            b.burst_index += 1
        
        if b.burst_index >= len(burst_times):
            b.active = False
