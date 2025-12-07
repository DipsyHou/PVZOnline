import uuid
import time
import asyncio
from typing import List, Dict, Optional
from fastapi import WebSocket

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

class Plant(GameObject):
    def __init__(self, col, row, type_name):
        super().__init__(col * 80 + 10, row * 100 + 10, 60, 60, type_name)
        self.col = col
        self.row = row
        self.last_shot = 0
        self.shoot_interval = 1.5 

class Zombie(GameObject):
    def __init__(self, row, type_name):
        super().__init__(800, row * 100 + 10, 60, 80, type_name) 
        self.row = row
        self.speed = 20 
        self.damage = 20 

class Bullet(GameObject):
    def __init__(self, x, y, row):
        super().__init__(x, y, 10, 10, "pea")
        self.row = row
        self.speed = 300

class GameRoom:
    def __init__(self, room_id):
        self.room_id = room_id
        self.name = room_id  # Default name is room_id
        self.players: Dict[str, WebSocket] = {} # username -> websocket
        self.host: Optional[str] = None
        self.state = "waiting" # waiting, playing
        self.settings = {"mode": "pve", "level": "1", "tps": "30"}
        
        # Game State
        self.plants: List[Plant] = []
        self.zombies: List[Zombie] = []
        self.bullets: List[Bullet] = []
        self.running = False
        self.last_time = time.time()
        self.roles = {} # username -> role (plant/zombie)

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.players[username] = websocket
        if not self.host:
            self.host = username
        
        await self.broadcast_room_state()

    def disconnect(self, username: str):
        if username in self.players:
            del self.players[username]
        if username == self.host:
            if self.players:
                self.host = list(self.players.keys())[0]
            else:
                self.host = None # Room empty
        
        # If playing, maybe end game? For now just keep running or stop if empty
        if not self.players and self.state == "waiting":
            self.running = False
        elif not self.players and self.state == "playing":
            # Keep running for a bit to allow reconnect (e.g. page refresh)
            # Ideally add a timeout here to stop eventually
            pass
        else:
            # Notify others
            asyncio.ensure_future(self.broadcast_room_state())

    async def broadcast_room_state(self):
        state = {
            "type": "room_state",
            "data": {
                "room_id": self.room_id,
                "name": self.name,
                "players": list(self.players.keys()),
                "host": self.host,
                "settings": self.settings,
                "state": self.state
            }
        }
        await self.broadcast(state)

    async def handle_command(self, username: str, data: dict):
        if data['type'] == 'rename_room' and username == self.host:
            self.name = data.get('name', self.room_id)
            await self.broadcast_room_state()
            return

        if self.state == "waiting":
            if data['type'] == 'start_game' and username == self.host:
                self.state = "playing"
                self.running = True
                # Assign roles
                players_list = list(self.players.keys())
                self.roles[players_list[0]] = "plant"
                if len(players_list) > 1:
                    self.roles[players_list[1]] = "zombie"
                
                await self.broadcast({"type": "start_game"})
                asyncio.ensure_future(self.game_loop())
            elif data['type'] == 'update_settings' and username == self.host:
                self.settings.update(data.get('settings', {}))
                await self.broadcast_room_state()
                
        elif self.state == "playing":
            role = self.roles.get(username)
            if role == "plant" and data['type'] == 'place_plant':
                c, r = data['col'], data['row']
                if not any(p.col == c and p.row == r for p in self.plants):
                    self.plants.append(Plant(c, r, "peashooter"))
            elif role == "zombie" and data['type'] == 'spawn_zombie':
                r = data['row']
                self.zombies.append(Zombie(r, "normal"))

    async def game_loop(self):
        print(f"Room {self.room_id} game started")
        self.last_time = time.time()
        
        tps = int(self.settings.get('tps', 30))
        sleep_time = 1.0 / tps

        empty_start_time = 0
        while self.running and self.state == "playing":
            if not self.players:
                if empty_start_time == 0:
                    empty_start_time = time.time()
                elif time.time() - empty_start_time > 30: # 30 seconds timeout
                    print(f"Room {self.room_id} stopped (timeout)")
                    self.running = False
                    break
            else:
                empty_start_time = 0

            now = time.time()
            dt = now - self.last_time
            self.last_time = now
            
            # Game Logic (Same as before)
            for p in self.plants:
                if now - p.last_shot > p.shoot_interval:
                    if any(z.row == p.row and z.x > p.x for z in self.zombies):
                        p.last_shot = now
                        self.bullets.append(Bullet(p.x + 40, p.y + 20, p.row))

            for z in self.zombies:
                eating = False
                for p in self.plants:
                    if p.row == z.row and abs(p.x - z.x) < 40:
                        eating = True
                        p.hp -= z.damage * dt
                        if p.hp <= 0: p.active = False
                        break
                if not eating:
                    z.x -= z.speed * dt

            for b in self.bullets:
                b.x += b.speed * dt
                if b.x > 800: b.active = False
                for z in self.zombies:
                    if z.row == b.row and abs(b.x - z.x) < 30 and abs(b.y - z.y) < 40:
                        b.active = False
                        z.hp -= 20
                        if z.hp <= 0: z.active = False
                        break

            self.plants = [p for p in self.plants if p.active]
            self.zombies = [z for z in self.zombies if z.active]
            self.bullets = [b for b in self.bullets if b.active]

            state = {
                "type": "game_state",
                "plants": [{"id": p.id, "x": p.x, "y": p.y, "type": p.type, "hp": p.hp} for p in self.plants],
                "zombies": [{"id": z.id, "x": z.x, "y": z.y, "type": z.type, "hp": z.hp} for z in self.zombies],
                "bullets": [{"id": b.id, "x": b.x, "y": b.y} for b in self.bullets],
                "roles": self.roles
            }
            await self.broadcast(state)
            await asyncio.sleep(sleep_time)

    def is_empty(self):
        return len(self.players) == 0

    async def broadcast(self, message: dict):
        for conn in list(self.players.values()):
            try:
                await conn.send_json(message)
            except:
                pass

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, GameRoom] = {}

    def create_room(self) -> str:
        room_id = str(uuid.uuid4())[:6]
        self.rooms[room_id] = GameRoom(room_id)
        return room_id

    def get_room(self, room_id: str) -> Optional[GameRoom]:
        return self.rooms.get(room_id)
    
    def list_rooms(self):
        return [{"id": r.room_id, "name": r.name, "players": len(r.players), "state": r.state} for r in self.rooms.values()]

    def remove_room(self, room_id: str):
        if room_id in self.rooms:
            del self.rooms[room_id]
