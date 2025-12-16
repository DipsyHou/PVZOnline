from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, ZOMBIE_W, ZOMBIE_H
from game.objects.bullet import Bullet

class BulletManager:
    def __init__(self, entity_manager):
        self.em = entity_manager

    def update(self, dt):
        for b in self.em.bullets:
            b.update(dt, self.em)
            
            if b.x > SCREEN_WIDTH or b.x < -100 or b.y > SCREEN_HEIGHT or b.y < -1000: 
                b.active = False
                continue

            # Max distance check
            if hasattr(b, 'max_distance') and b.max_distance > 0:
                dist = ((b.x - b.start_x)**2 + (b.y - b.start_y)**2)**0.5
                if dist >= b.max_distance:
                    b.active = False
                    continue

            if b.kind not in ["watermelon", "corn_homing"] or (b.kind == "corn_homing" and not b.homing):
                 for z in self.em.zombies:
                    if b.active and b.x + b.w > z.x and b.x < z.x + ZOMBIE_W and b.y + b.h > z.y and b.y < z.y + ZOMBIE_H:
                        if z.id in b.hit_set: continue
                        
                        z.take_damage(b.damage)
                        b.hit_set.add(z.id)

                        if b.splash_radius > 0:
                            for other_z in self.em.zombies:
                                if other_z.id == z.id: continue
                                dx = (other_z.x + ZOMBIE_W/2) - (z.x + ZOMBIE_W/2)
                                dy = (other_z.y + ZOMBIE_H/2) - (z.y + ZOMBIE_H/2)
                                dist = (dx**2 + dy**2)**0.5
                                if dist <= b.splash_radius:
                                    other_z.take_damage(b.splash_damage)
                            
                            self.em.add_event({
                                "type": "particle", 
                                "x": z.x + ZOMBIE_W/2, 
                                "y": z.y + ZOMBIE_H/2, 
                                "kind": b.kind + "_splash"
                            })
                        
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
                            break

                        if b.stun > 0: z.apply_stun(b.stun)
                        if b.slow_duration > 0: z.apply_slow(b.slow_duration, b.slow_factor)
                        if b.knockback_dist > 0: z.apply_knockback(b.knockback_dist, b.knockback_duration)

                        if b.pierce <= 0:
                            b.active = False
                            break
                        else:
                            b.pierce -= 1
            
            if (b.kind == "watermelon" or b.kind == "bomb") and b.total_time and b.elapsed >= b.total_time:
                b.active = False
                for z in self.em.zombies:
                    dx = (z.x + ZOMBIE_W/2) - b.x
                    dy = (z.y + ZOMBIE_H/2) - b.y
                    dist = (dx**2 + dy**2)**0.5
                    if dist <= b.splash_radius:
                        z.take_damage(b.splash_damage)
                        if b.slow_duration > 0: z.apply_slow(b.slow_duration, b.slow_factor)
                
                self.em.add_event({
                    "type": "particle", 
                    "x": b.x, 
                    "y": b.y, 
                    "kind": b.kind + "_splash"
                })
