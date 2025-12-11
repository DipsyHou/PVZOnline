const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 游戏配置
let CELL_W = 100;
let CELL_H = 100;
let ROWS = 7;
let COLS = 11;
let SCREEN_WIDTH = COLS * CELL_W;
let SCREEN_HEIGHT = ROWS * CELL_H;
let PLANT_W = 60;
let PLANT_H = 60;
let ZOMBIE_W = 60;
let ZOMBIE_H = 80;
let BULLET_W = 20;
let BULLET_H = 20;

// 动态设置画布大小
function resizeCanvas() {
    canvas.width = SCREEN_WIDTH;
    canvas.height = SCREEN_HEIGHT;
}
resizeCanvas();

// 游戏状态 (本地插值用)
// 结构: { id: { x, y, targetX, targetY, type, hp, ... } }
let gameObjects = {
    plants: {},
    zombies: {},
    bullets: {}
};

let myRole = null;
let ws = null;
let selectedPlant = 'peashooter';
let currentSun = 50;
let currentCooldowns = {};
const PLANT_COOLDOWNS = {
    peashooter: 0,
    sunflower: 0,
    pod_peashooter: 7
};

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
        if (p.type === 'sunflower') {
            ctx.fillStyle = '#f1c40f'; // Yellow for sunflower
        } else {
            ctx.fillStyle = '#00ff00'; // Green for peashooter
        }
        ctx.fillRect(p.x, p.y, PLANT_W, PLANT_H);
        // 血条
        ctx.fillStyle = 'red';
        ctx.fillRect(p.x, p.y - 5, PLANT_W * (p.hp / p.max_hp), 5);
    });

    // 画僵尸
    Object.values(gameObjects.zombies).forEach(z => {
        ctx.fillStyle = '#555555';
        ctx.fillRect(z.x, z.y, ZOMBIE_W, ZOMBIE_H);
        // 血条
        ctx.fillStyle = 'red';
        ctx.fillRect(z.x, z.y - 5, ZOMBIE_W * (z.hp / z.max_hp), 5);
    });

    // 画子弹
    Object.values(gameObjects.bullets).forEach(b => {
        ctx.fillStyle = '#00ff00';
        ctx.beginPath();
        ctx.arc(b.x + BULLET_W/2, b.y + BULLET_H/2, BULLET_W/2, 0, Math.PI*2);
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
            ws.send(JSON.stringify({
                type: 'place_plant', 
                col: c, 
                row: r,
                plant_type: selectedPlant
            }));
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
    if (msg.type === 'start_game' && msg.config) {
        CELL_W = msg.config.CELL_W;
        CELL_H = msg.config.CELL_H;
        ROWS = msg.config.ROWS;
        COLS = msg.config.COLS;
        SCREEN_WIDTH = msg.config.SCREEN_WIDTH;
        SCREEN_HEIGHT = msg.config.SCREEN_HEIGHT;
        PLANT_W = msg.config.PLANT_W;
        PLANT_H = msg.config.PLANT_H;
        ZOMBIE_W = msg.config.ZOMBIE_W;
        ZOMBIE_H = msg.config.ZOMBIE_H;
        BULLET_W = msg.config.BULLET_W;
        BULLET_H = msg.config.BULLET_H;
        resizeCanvas();
    }

    if(msg.type === 'game_state') {
        myRole = msg.roles[username];
        currentSun = msg.sun || 0;
        currentCooldowns = msg.cooldowns || {};
        updateUI();
        
        // Sync objects
        syncObjects('plants', msg.plants);
        syncObjects('zombies', msg.zombies);
        syncObjects('bullets', msg.bullets);
    }
};

function updateUI() {
    const sunDisplay = document.getElementById('sun-display');
    const plantControls = document.getElementById('plant-controls');
    
    if (myRole === 'plant') {
        sunDisplay.style.display = 'inline';
        sunDisplay.textContent = `阳光: ${currentSun}`;
        plantControls.style.display = 'block';
        
        // Update button states
        updatePlantButton('peashooter', 100);
        updatePlantButton('sunflower', 50);
        updatePlantButton('pod_peashooter', 225);
    } else {
        sunDisplay.style.display = 'none';
        plantControls.style.display = 'none';
    }
}

function updatePlantButton(type, cost) {
    const btn = document.getElementById(`btn-${type}`);
    if (!btn) return;
    
    const remaining = currentCooldowns[type] || 0;
    const total = PLANT_COOLDOWNS[type] || 1;
    const overlay = btn.querySelector('.cooldown-overlay');
    
    // Update cooldown overlay
    if (remaining > 0) {
        const pct = (remaining / total) * 100;
        if(overlay) overlay.style.height = `${pct}%`;
        btn.style.cursor = 'not-allowed';
        // Keep opacity normal so we can see the cooldown progress, or dim it?
        // Usually card is dark when cooling down.
        // But here we use overlay.
    } else {
        if(overlay) overlay.style.height = '0%';
    }

    if (currentSun >= cost && remaining <= 0) {
        btn.style.opacity = '1';
        btn.style.cursor = 'pointer';
        if (selectedPlant === type) {
            btn.style.borderColor = 'white';
        } else {
            btn.style.borderColor = 'transparent';
        }
    } else {
        // If cooling down or not enough sun
        if (remaining > 0) {
             // Cooling down
             btn.style.opacity = '0.8'; 
        } else {
             // Not enough sun
             btn.style.opacity = '0.5';
             btn.style.cursor = 'not-allowed';
             btn.style.borderColor = 'transparent';
        }
    }
}

function selectPlant(type) {
    selectedPlant = type;
    updateUI();
}

function syncObjects(type, serverList) {
    const localMap = gameObjects[type];
    const serverIds = new Set();

    serverList.forEach(sObj => {
        serverIds.add(sObj.id);
        if (localMap[sObj.id]) {
            // Update existing object
            // Only update fields that are present in sObj
            if (sObj.x !== undefined) localMap[sObj.id].targetX = sObj.x;
            if (sObj.y !== undefined) localMap[sObj.id].targetY = sObj.y;
            if (sObj.hp !== undefined) localMap[sObj.id].hp = sObj.hp;
            if (sObj.max_hp !== undefined) localMap[sObj.id].max_hp = sObj.max_hp;
            if (sObj.type !== undefined) localMap[sObj.id].type = sObj.type;
        } else {
            // New object
            // If it's a partial update (missing x/y/type), we might have a problem if we don't have defaults.
            // But for plants, we send full sync every 1s.
            // For zombies/bullets, we always send x/y.
            localMap[sObj.id] = {
                ...sObj,
                targetX: sObj.x || 0,
                targetY: sObj.y || 0
            };
        }
    });

    // Remove objects not in server list
    // Wait, if server sends partial list?
    // No, server sends FULL list of objects, but with PARTIAL fields.
    // So if an ID is missing from serverList, it means it's gone.
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
