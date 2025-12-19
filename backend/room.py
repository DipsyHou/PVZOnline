import uuid
import asyncio
import time
from typing import Dict, Optional, List
from fastapi import WebSocket
from game.engine import Game
from game.constants import CELL_W, CELL_H, ROWS, COLS, SCREEN_WIDTH, SCREEN_HEIGHT, PLANT_W, PLANT_H, ZOMBIE_W, ZOMBIE_H, BULLET_W, BULLET_H

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.name = room_id
        self.players: Dict[str, WebSocket] = {} # username -> websocket
        self.host: Optional[str] = None
        self.state = "waiting" # waiting, playing
        self.settings = {"mode": "pve", "level": "1", "tps": "30"}
        self.game: Optional[Game] = None
        self.running = False
        self.roles = {} # username -> role

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.players[username] = websocket
        if not self.host:
            self.host = username
        
        await self.broadcast_room_state()

        if self.state == "playing":
            await websocket.send_json({
                "type": "start_game",
                "config": {
                    "CELL_W": CELL_W,
                    "CELL_H": CELL_H,
                    "ROWS": ROWS,
                    "COLS": COLS,
                    "SCREEN_WIDTH": SCREEN_WIDTH,
                    "SCREEN_HEIGHT": SCREEN_HEIGHT,
                    "PLANT_W": PLANT_W,
                    "PLANT_H": PLANT_H,
                    "ZOMBIE_W": ZOMBIE_W,
                    "ZOMBIE_H": ZOMBIE_H,
                    "BULLET_W": BULLET_W,
                    "BULLET_H": BULLET_H
                }
            })
            # Send full state immediately
            if self.game:
                await websocket.send_json(self.game.get_state())

    def disconnect(self, username: str):
        if username in self.players:
            del self.players[username]
        if username == self.host:
            if self.players:
                self.host = list(self.players.keys())[0]
            else:
                self.host = None # Room empty
        
        if not self.players and self.state == "waiting":
            self.running = False
        elif not self.players and self.state == "playing":
            pass # Handled by game loop timeout
        else:
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

        if data['type'] == 'set_mode' and username == self.host:
            mode = data.get('mode')
            if mode in ['pve', 'endless']:
                self.settings['mode'] = mode
                await self.broadcast_room_state()
            return

        if data['type'] == 'update_settings' and username == self.host:
            new_settings = data.get('settings', {})
            # Validate mode
            if 'mode' in new_settings and new_settings['mode'] not in ['pve', 'endless']:
                return
            self.settings.update(new_settings)
            await self.broadcast_room_state()
            return

        if self.state == "waiting":
            if data['type'] == 'start_game' and username == self.host:
                self.state = "playing"
                self.running = True
                
                # Assign roles
                players_list = list(self.players.keys())
                
                if self.settings.get('mode') == 'endless':
                    # Endless mode: everyone is plant
                    for p in players_list:
                        self.roles[p] = "plant"
                else:
                    # PvP mode
                    self.roles[players_list[0]] = "plant"
                    if len(players_list) > 1:
                        self.roles[players_list[1]] = "zombie"
                
                await self.broadcast({
                    "type": "start_game",
                    "config": {
                        "CELL_W": CELL_W,
                        "CELL_H": CELL_H,
                        "ROWS": ROWS,
                        "COLS": COLS,
                        "SCREEN_WIDTH": SCREEN_WIDTH,
                        "SCREEN_HEIGHT": SCREEN_HEIGHT,
                        "PLANT_W": PLANT_W,
                        "PLANT_H": PLANT_H,
                        "ZOMBIE_W": ZOMBIE_W,
                        "ZOMBIE_H": ZOMBIE_H,
                        "BULLET_W": BULLET_W,
                        "BULLET_H": BULLET_H
                    }
                })
                
                # Initialize Game
                self.game = Game(self.settings, self.roles)
                asyncio.ensure_future(self.game_loop())
                
            elif data['type'] == 'update_settings' and username == self.host:
                self.settings.update(data.get('settings', {}))
                await self.broadcast_room_state()
                
        elif self.state == "playing" and self.game:
            # Delegate game commands to Game instance
            self.game.handle_command(username, data)

    async def game_loop(self):
        print(f"Room {self.room_id} game started")
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

            # Update Game State
            if self.game:
                self.game.update()
                state = self.game.get_state()
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
        self.rooms: Dict[str, Room] = {}

    def create_room(self) -> str:
        room_id = str(uuid.uuid4())[:6]
        self.rooms[room_id] = Room(room_id)
        return room_id

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)
    
    def list_rooms(self):
        return [{"id": r.room_id, "name": r.name, "players": len(r.players), "state": r.state} for r in self.rooms.values()]

    def remove_room(self, room_id: str):
        if room_id in self.rooms:
            del self.rooms[room_id]
