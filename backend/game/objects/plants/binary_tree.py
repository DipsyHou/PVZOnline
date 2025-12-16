from .base import Plant
from ..bullet import Bullet

class BinaryTree(Plant):
    def __init__(self, col, row):
        super().__init__(col, row, "binary_tree")
        self.hp = 200
        self.max_hp = 200
        self.shoot_interval = 2.0
        self.cost = 175

    def shoot(self, game_state):
        bx = self.x + 20
        by = self.y
        speed = 400
        vy = 100
        
        # Upward branch
        b1 = Bullet(bx, by, self.row, speed, -vy, 20, "branch")
        b1.branch_level = 0
        b1.height = 3
        game_state.bullets.append(b1)
        
        # Downward branch
        b2 = Bullet(bx, by, self.row, speed, vy, 20, "branch")
        b2.branch_level = 0
        b2.height = 3
        game_state.bullets.append(b2)
