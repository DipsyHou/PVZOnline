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
from game_engine import RoomManager

app = FastAPI()

# CORS 设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # WebSocket 403 Fix: Cannot use wildcard with credentials=True
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
                 (username TEXT PRIMARY KEY, password TEXT, wins INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

init_db()

# 数据模型
class UserAuth(BaseModel):
    username: str
    password: str

# --- 用户 API ---

@app.post("/api/register")
def register(user: UserAuth):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # 简单哈希存储
        pwd_hash = hashlib.sha256(user.password.encode()).hexdigest()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, pwd_hash))
        conn.commit()
        return {"status": "success", "message": "注册成功"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="用户名已存在")
    finally:
        conn.close()

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
        if room.is_empty() and room.state == "waiting":
            room.running = False
            room_manager.remove_room(room_id)
            print(f"Room {room_id} deleted (empty)")

# --- 静态文件服务 ---
# 挂载前端目录
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    # 监听所有IP，端口8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
