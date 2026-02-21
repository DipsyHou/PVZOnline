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
import logging

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pvz_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 导入游戏引擎
from room import RoomManager
from game.config import DEFAULT_PLANTS, DEFAULT_ZOMBIES

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
    """初始化数据库"""
    try:
        # 确保数据库目录存在
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (username TEXT PRIMARY KEY, password TEXT, wins INTEGER DEFAULT 0, 
                      inventory TEXT DEFAULT '[]', deck TEXT DEFAULT '[]', plant_levels TEXT DEFAULT '{}')''')
        
        # Check if columns exist (for migration)
        c.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in c.fetchall()]
        if 'inventory' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN inventory TEXT DEFAULT '[]'")
            logger.info("Added 'inventory' column to users table")
        if 'deck' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN deck TEXT DEFAULT '[]'")
            logger.info("Added 'deck' column to users table")
        if 'plant_levels' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN plant_levels TEXT DEFAULT '{}'")
            logger.info("Added 'plant_levels' column to users table")
        if 'plant_slots' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN plant_slots INTEGER DEFAULT 12")
            logger.info("Added 'plant_slots' column to users table")
        if 'zombie_slots' not in columns:
            c.execute("ALTER TABLE users ADD COLUMN zombie_slots INTEGER DEFAULT 10")
            logger.info("Added 'zombie_slots' column to users table")
            
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

init_db()

# Default Inventory - 从配置文件导入
# DEFAULT_PLANTS 和 DEFAULT_ZOMBIES 已在顶部导入

# 数据模型
class UserAuth(BaseModel):
    username: str
    password: str

class DeckUpdate(BaseModel):
    username: str
    deck: Dict[str, List[str]]
    plant_levels: Optional[Dict[str, int]] = None

# --- 用户 API ---

@app.post("/api/register")
def register(user: UserAuth):
    """用户注册"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
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
        
        # Initial plant levels (all 0)
        plant_levels = {p: 0 for p in DEFAULT_PLANTS}
        c.execute("INSERT INTO users (username, password, inventory, deck, plant_levels, plant_slots, zombie_slots) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (user.username, pwd_hash, json.dumps(inventory), json.dumps(deck), json.dumps(plant_levels), 12, 10))
        conn.commit()
        
        logger.info(f"User registered successfully: {user.username}")
        return {"status": "success", "message": "注册成功"}
    except sqlite3.IntegrityError:
        logger.warning(f"Registration failed - username already exists: {user.username}")
        raise HTTPException(status_code=400, detail="用户名已存在")
    except Exception as e:
        logger.error(f"Registration error for {user.username}: {e}")
        raise HTTPException(status_code=500, detail="注册失败，请稍后重试")
    finally:
        conn.close()

@app.get("/api/user/inventory")
def get_inventory(username: str):
    """获取用户仓库信息"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT inventory, deck, plant_levels, plant_slots, zombie_slots FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()
        
        if result:
            return {
                "status": "success", 
                "inventory": json.loads(result[0]), 
                "deck": json.loads(result[1]),
                "plant_levels": json.loads(result[2]) if len(result) > 2 else {},
                "plant_slots": result[3] if len(result) > 3 else 12,
                "zombie_slots": result[4] if len(result) > 4 else 10
            }
        else:
            logger.warning(f"Inventory request for non-existent user: {username}")
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching inventory for {username}: {e}")
        raise HTTPException(status_code=500, detail="获取仓库信息失败")

@app.post("/api/user/deck")
def update_deck(data: DeckUpdate):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get current deck (check if user exists)
    c.execute("SELECT deck, plant_levels FROM users WHERE username=?", (data.username,))
    result = c.fetchone()
    if not result:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    # Update deck directly
    c.execute("UPDATE users SET deck=? WHERE username=?", (json.dumps(data.deck), data.username))
    if data.plant_levels is not None:
        c.execute("UPDATE users SET plant_levels=? WHERE username=?", (json.dumps(data.plant_levels), data.username))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/api/login")
def login(user: UserAuth):
    """用户登录"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        pwd_hash = hashlib.sha256(user.password.encode()).hexdigest()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, pwd_hash))
        result = c.fetchone()
        conn.close()
        
        if result:
            logger.info(f"User logged in: {user.username}")
            # 实际生产中应返回 JWT Token，这里简化返回用户信息
            return {"status": "success", "username": user.username, "token": f"token_{user.username}"}
        else:
            logger.warning(f"Failed login attempt for user: {user.username}")
            raise HTTPException(status_code=401, detail="用户名或密码错误")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {user.username}: {e}")
        raise HTTPException(status_code=500, detail="登录失败，请稍后重试")

# 全局房间管理
room_manager = RoomManager()

@app.get("/api/rooms")
def list_rooms():
    return room_manager.list_rooms()

@app.post("/api/rooms")
def create_room():
    """创建房间"""
    try:
        room_id = room_manager.create_room()
        logger.info(f"Room created: {room_id}")
        return {"status": "success", "room_id": room_id}
    except Exception as e:
        logger.error(f"Failed to create room: {e}")
        raise HTTPException(status_code=500, detail="创建房间失败")

@app.websocket("/ws/room/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str = "Guest"):
    """WebSocket房间连接"""
    logger.info(f"WS Connect: room={room_id}, user={username}")
    room = room_manager.get_room(room_id)
    if not room:
        logger.warning(f"WebSocket connection failed - room not found: {room_id}")
        await websocket.close(code=4004, reason="Room not found")
        return
    
    try:
        await room.connect(websocket, username)
        while True:
            data = await websocket.receive_json()
            await room.handle_command(username, data)
    except WebSocketDisconnect:
        logger.info(f"WS Disconnect: room={room_id}, user={username}")
        room.disconnect(username)
        if room.is_empty():
            # 如果是游戏中，给予一定的重连缓冲时间（处理页面跳转）
            if room.state == "playing":
                await asyncio.sleep(1)
                if room.is_empty():
                    room.running = False
                    room_manager.remove_room(room_id)
                    logger.info(f"Room {room_id} deleted (empty playing timeout)")
            else:
                # 等待状态直接删除
                room.running = False
                room_manager.remove_room(room_id)
                logger.info(f"Room {room_id} deleted (empty waiting)")
    except Exception as e:
        logger.error(f"WebSocket error in room {room_id} for user {username}: {e}")
        room.disconnect(username)

# --- 静态文件服务 ---
# 挂载前端目录
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    # 监听所有IP，端口80
    uvicorn.run(app, host="0.0.0.0", port=8000)
