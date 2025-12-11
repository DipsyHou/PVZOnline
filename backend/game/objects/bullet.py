from .base import GameObject
from ..constants import BULLET_W, BULLET_H
import math

class Bullet(GameObject):
    def __init__(self, x, y, row, angle=0):
        super().__init__(x, y, BULLET_W, BULLET_H, "pea")
        self.row = row
        self.speed = 300
        self.angle = angle
        self.vx = self.speed * math.cos(math.radians(angle))
        self.vy = self.speed * math.sin(math.radians(angle))
