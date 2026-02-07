import uuid

class GameObject:
    def __init__(self, x, y, w, h, type_name):
        self.id = str(uuid.uuid4())[:8]
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type_name
        self.hp = 100
        self.max_hp = 100
        self.active = True
