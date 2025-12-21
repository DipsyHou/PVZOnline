import uvicorn
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import sqlite3
import hashlib
import uuid
import json
import os
import asyncio
import time
import math

# 导入游戏引擎
from room import RoomManager

app = FastAPI()

# CORS 设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库初始化
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "pvz.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, wins INTEGER DEFAULT 0, 
                  inventory TEXT DEFAULT '[]', deck TEXT DEFAULT '[]')''')
    
    # Check if columns exist (for migration)
    c.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in c.fetchall()]
    if 'inventory' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN inventory TEXT DEFAULT '[]'")
    if 'deck' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN deck TEXT DEFAULT '[]'")
        
    conn.commit()
    conn.close()

init_db()

# Default Inventory
DEFAULT_PLANTS = ["peashooter", "sunflower", "pod_peashooter", "watermelon", "pine_shooter"]
DEFAULT_ZOMBIES = ["normal", "buckethead", "exploder"]

# 数据模型
class UserAuth(BaseModel):
    username: str
    password: str

class DeckUpdate(BaseModel):
    username: str
    deck: Dict[str, List[str]]

# --- 用户 API ---

@app.post("/api/register")
def register(user: UserAuth):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # 简单哈希存储
        pwd_hash = hashlib.sha256(user.password.encode()).hexdigest()
        
        # Initial inventory
        inventory = {
            "plants": DEFAULT_PLANTS,
            "zombies": DEFAULT_ZOMBIES
        }
        # Initial deck (same as inventory for now)
        deck = {
            "plants": DEFAULT_PLANTS,
            "zombies": DEFAULT_ZOMBIES
        }
        
        c.execute("INSERT INTO users (username, password, inventory, deck) VALUES (?, ?, ?, ?)", 
                  (user.username, pwd_hash, json.dumps(inventory), json.dumps(deck)))
        conn.commit()
        return {"status": "success", "message": "注册成功"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="用户名已存在")
    finally:
        conn.close()

@app.get("/api/user/inventory")
def get_inventory(username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT inventory, deck FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {
            "status": "success", 
            "inventory": json.loads(result[0]), 
            "deck": json.loads(result[1])
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/user/deck")
def update_deck(data: DeckUpdate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get current deck (check if user exists)
    c.execute("SELECT deck FROM users WHERE username=?", (data.username,))
    result = c.fetchone()
    if not result:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    # Update deck directly
    c.execute("UPDATE users SET deck=? WHERE username=?", (json.dumps(data.deck), data.username))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/api/login")
def login(user: UserAuth):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    pwd_hash = hashlib.sha256(user.password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, pwd_hash))
    result = c.fetchone()
    conn.close()
    
    if result:
        # 实际生产中应返回 JWT Token，这里简化返回用户信息
        return {"status": "success", "username": user.username, "token": f"token_{user.username}"}
    else:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

# 全局房间管理
room_manager = RoomManager()

@app.get("/api/rooms")
def list_rooms():
    return room_manager.list_rooms()

@app.post("/api/rooms")
def create_room():
    room_id = room_manager.create_room()
    return {"status": "success", "room_id": room_id}

@app.websocket("/ws/room/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str = "Guest"):
    print(f"WS Connect: {room_id}, {username}")
    room = room_manager.get_room(room_id)
    if not room:
        await websocket.close(code=4004, reason="Room not found")
        return
    
    await room.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_json()
            await room.handle_command(username, data)
    except WebSocketDisconnect:
        room.disconnect(username)
        if room.is_empty():
            # 如果是游戏中，给予一定的重连缓冲时间（处理页面跳转）
            if room.state == "playing":
                await asyncio.sleep(1)
                if room.is_empty():
                    room.running = False
                    room_manager.remove_room(room_id)
                    print(f"Room {room_id} deleted (empty playing timeout)")
            else:
                # 等待状态直接删除
                room.running = False
                room_manager.remove_room(room_id)
                print(f"Room {room_id} deleted (empty waiting)")

# --- 静态文件服务 ---
# 挂载前端目录
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    # 监听所有IP，端口80
    uvicorn.run(app, host="0.0.0.0", port=8000)
