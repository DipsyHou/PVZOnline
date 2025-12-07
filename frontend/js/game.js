const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 游戏配置
const CELL_W = 80;
const CELL_H = 100;
const ROWS = 5;
const COLS = 9;

// 游戏状态 (本地插值用)
// 结构: { id: { x, y, targetX, targetY, type, hp, ... } }
let gameObjects = {
    plants: {},
    zombies: {},
    bullets: {}
};

let myRole = null;
let ws = null;

const username = sessionStorage.getItem('username');
if(!username) window.location.href = 'index.html';

const urlParams = new URLSearchParams(window.location.search);
const roomId = urlParams.get('roomId');
if(!roomId) window.location.href = 'lobby.html';

// 渲染循环
function loop() {
    updateInterpolation();
    draw();
    requestAnimationFrame(loop);
}

// 插值平滑逻辑 (LERP)
function updateInterpolation() {
    const factor = 0.2; // 平滑因子 (0.1~0.3 比较合适)
    
    ['plants', 'zombies', 'bullets'].forEach(type => {
        for (let id in gameObjects[type]) {
            let obj = gameObjects[type][id];
            // 简单的线性插值: current = current + (target - current) * factor
            obj.x += (obj.targetX - obj.x) * factor;
            obj.y += (obj.targetY - obj.y) * factor;
            
            // 如果距离很近，直接吸附，避免抖动
            if(Math.abs(obj.targetX - obj.x) < 0.5) obj.x = obj.targetX;
            if(Math.abs(obj.targetY - obj.y) < 0.5) obj.y = obj.targetY;
        }
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 画网格
    ctx.strokeStyle = 'rgba(0,0,0,0.1)';
    for(let r=0; r<ROWS; r++) {
        for(let c=0; c<COLS; c++) {
            ctx.strokeRect(c*CELL_W, r*CELL_H, CELL_W, CELL_H);
        }
    }

    // 画植物
    Object.values(gameObjects.plants).forEach(p => {
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(p.x, p.y, 60, 60);
        // 血条
        ctx.fillStyle = 'red';
        ctx.fillRect(p.x, p.y - 5, 60 * (p.hp/100), 5);
    });

    // 画僵尸
    Object.values(gameObjects.zombies).forEach(z => {
        ctx.fillStyle = '#555555';
        ctx.fillRect(z.x, z.y, 60, 80);
        // 血条
        ctx.fillStyle = 'red';
        ctx.fillRect(z.x, z.y - 5, 60 * (z.hp/100), 5);
    });

    // 画子弹
    Object.values(gameObjects.bullets).forEach(b => {
        ctx.fillStyle = '#00ff00';
        ctx.beginPath();
        ctx.arc(b.x, b.y + 15, 10, 0, Math.PI*2);
        ctx.fill();
    });
    
    // UI 提示
    ctx.fillStyle = 'white';
    ctx.font = '20px Arial';
    let roleText = "观众";
    if (myRole === 'plant') roleText = "植物 (点击网格种豌豆)";
    if (myRole === 'zombie') roleText = "僵尸 (点击行放僵尸)";
    
    ctx.fillText(`角色: ${roleText}`, 10, 30);
}

// 交互：发送指令给服务器
canvas.addEventListener('click', (e) => {
    if(!ws) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const c = Math.floor(x / CELL_W);
    const r = Math.floor(y / CELL_H);

    if(c >= 0 && c < COLS && r >= 0 && r < ROWS) {
        if(myRole === 'plant') {
            ws.send(JSON.stringify({type: 'place_plant', col: c, row: r}));
        } else if (myRole === 'zombie') {
            ws.send(JSON.stringify({type: 'spawn_zombie', row: r}));
        }
    }
});

// 初始化连接
const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const wsUrl = `${protocol}://${window.location.host}/ws/room/${roomId}?username=${username}`;
ws = new WebSocket(wsUrl);

ws.onopen = () => {
    console.log("Connected to Game Server");
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if(msg.type === 'game_state') {
        myRole = msg.roles[username];
        
        // 同步状态
        syncObjects('plants', msg.plants);
        syncObjects('zombies', msg.zombies);
        syncObjects('bullets', msg.bullets);

        const infoSpan = document.getElementById('game-info');
        if(infoSpan) {
            infoSpan.textContent = `房间: ${roomId} | 玩家: ${username} | 角色: ${myRole}`;
        }
    }
};

function syncObjects(type, serverList) {
    const localMap = gameObjects[type];
    const serverIds = new Set();

    serverList.forEach(sObj => {
        serverIds.add(sObj.id);
        if (localMap[sObj.id]) {
            // 已存在：更新目标位置
            localMap[sObj.id].targetX = sObj.x;
            localMap[sObj.id].targetY = sObj.y;
            localMap[sObj.id].hp = sObj.hp; // 血量直接同步
        } else {
            // 新增：直接创建
            localMap[sObj.id] = {
                ...sObj,
                targetX: sObj.x,
                targetY: sObj.y
            };
        }
    });

    // 删除不存在的对象
    for (let id in localMap) {
        if (!serverIds.has(id)) {
            delete localMap[id];
        }
    }
}

loop();

function backToLobby() {
    ws.close();
    window.location.href = 'lobby.html';
}
