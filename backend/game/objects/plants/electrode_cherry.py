import math
from .base import Plant
from ...constants import CELL_W, CELL_H

class ElectrodeCherry(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "electrode_cherry")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 0
        self.cost = 175
        self.paired_id = None

    def update(self, dt, game_state):
        # Find partner if not paired
        if not self.paired_id:
            best_dist = float('inf')
            best_p = None
            for p in game_state.plants:
                if p == self or p.type != "electrode_cherry" or p.active == False: continue
                # Check if p is already paired (need to check if p.paired_id is set)
                # But we can't easily access p's paired_id if it's not exposed or if we don't check properly.
                # Assuming p has paired_id attribute.
                if getattr(p, 'paired_id', None): continue
                
                dx = p.x - self.x
                dy = p.y - self.y
                dist = dx*dx + dy*dy
                if dist < best_dist:
                    best_dist = dist
                    best_p = p
            
            if best_p:
                self.paired_id = best_p.id
                best_p.paired_id = self.id
        else:
            # Check if partner is still alive
            partner = None
            for p in game_state.plants:
                if p.id == self.paired_id:
                    partner = p
                    break
            
            if not partner or not partner.active:
                self.paired_id = None
            else:
                # Beam damage logic
                # Line segment from self center to partner center
                x1 = self.x + CELL_W/2
                y1 = self.y + CELL_H/2
                x2 = partner.x + CELL_W/2
                y2 = partner.y + CELL_H/2
                
                # Check collision with zombies
                for z in game_state.zombies:
                    zx = z.x + z.w/2
                    zy = z.y + z.h/2
                    
                    # Distance from point to line segment
                    # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
                    # But we need segment, not line.
                    
                    l2 = (x1-x2)**2 + (y1-y2)**2
                    if l2 == 0: continue
                    
                    t = ((zx - x1) * (x2 - x1) + (zy - y1) * (y2 - y1)) / l2
                    t = max(0, min(1, t))
                    
                    proj_x = x1 + t * (x2 - x1)
                    proj_y = y1 + t * (y2 - y1)
                    
                    dist_sq = (zx - proj_x)**2 + (zy - proj_y)**2
                    
                    # Beam width approx 20px radius?
                    if dist_sq < 400:
                        z.take_damage(90 * dt) # 90 DPS
