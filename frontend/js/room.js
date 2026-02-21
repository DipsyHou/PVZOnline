import { PLANT_CONFIGS, ZOMBIE_CONFIGS } from './config.js';

console.log("room.js loading...");

const username = sessionStorage.getItem('username');
if(!username) window.location.href = 'index.html';

const urlParams = new URLSearchParams(window.location.search);
const roomId = urlParams.get('roomId');
if(!roomId) window.location.href = 'lobby.html';

document.getElementById('room-title').textContent = `房间 ${roomId}`;

// WebSocket for room state
const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const wsUrl = `${protocol}://${window.location.host}/ws/room/${roomId}?username=${username}`;
let ws;

try {
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log("Connected to Room");
        loadInventory();
    };

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if(msg.type === 'room_state') {
            updateRoomUI(msg.data);
        } else if (msg.type === 'start_game') {
            window.location.href = `game.html?roomId=${roomId}`;
        }
    };
} catch (e) {
    console.error("WebSocket init failed", e);
}

let myInventory = { plants: [], zombies: [] };
let myPlantLevels = {};
let selectedDeck = { plants: [], zombies: [] };
let plantSlots = 12;
let zombieSlots = 10;

// Expose functions to window IMMEDIATELY
window.startGame = function() {
    console.log("startGame called");
    if(ws) ws.send(JSON.stringify({type: 'start_game'}));
};

window.leaveRoom = function() {
    if(ws) ws.close();
    window.location.href = 'lobby.html';
};

window.renameRoom = function() {
    const name = document.getElementById('room-name-input').value;
    if (name && ws) {
        ws.send(JSON.stringify({
            type: 'rename_room',
            name: name
        }));
    }
};

window.openDeckModal = function() {
    const modal = document.getElementById('deck-modal');
    if(modal) {
        modal.style.display = 'flex';
        renderDeckSelection(); // Re-render to ensure fresh state
    }
};

window.closeDeckModal = function() {
    const modal = document.getElementById('deck-modal');
    if(modal) modal.style.display = 'none';
};

window.confirmDeck = async function() {
    if(ws) {
        // Save to DB
        try {
            await fetch('/api/user/deck', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: username,
                    deck: selectedDeck
                })
            });
        } catch(e) {
            console.error("Failed to save deck", e);
        }

        ws.send(JSON.stringify({
            type: 'set_deck',
            deck: selectedDeck,
            plant_levels: myPlantLevels
        }));
        // alert("卡组已保存！"); // Optional: remove alert for smoother UX
        window.closeDeckModal();
    }
};

function updateRoomUI(data) {
    document.getElementById('room-title').textContent = data.name || `房间 ${data.room_id}`;

    const list = document.getElementById('player-list');
    if(list) {
        list.innerHTML = '';
        data.players.forEach(p => {
            const div = document.createElement('div');
            div.textContent = p + (p === data.host ? " (房主)" : "");
            div.style.padding = "5px";
            div.style.borderBottom = "1px solid #eee";
            list.appendChild(div);
        });
    }

    // Only host can change settings
    const isHost = data.host === username;
    
    const renameContainer = document.getElementById('rename-container');
    if (renameContainer) {
        renameContainer.style.display = isHost ? 'block' : 'none';
    }

    const modeSelect = document.getElementById('game-mode');
    const levelSelect = document.getElementById('game-level');
    const tpsSelect = document.getElementById('game-tps');
    const startBtn = document.getElementById('start-btn');

    if(modeSelect) {
        modeSelect.disabled = !isHost;
        levelSelect.disabled = !isHost;
        tpsSelect.disabled = !isHost;
        startBtn.disabled = !isHost;

        if(!isHost) {
            modeSelect.value = data.settings.mode;
            levelSelect.value = data.settings.level;
            tpsSelect.value = data.settings.tps || 30;
        }
    }
}

// Listen for settings changes by host
const modeEl = document.getElementById('game-mode');
if(modeEl) {
    modeEl.addEventListener('change', sendSettings);
    document.getElementById('game-level').addEventListener('change', sendSettings);
    document.getElementById('game-tps').addEventListener('change', sendSettings);
}

function sendSettings() {
    const mode = document.getElementById('game-mode').value;
    const level = document.getElementById('game-level').value;
    const tps = document.getElementById('game-tps').value;
    if(ws) {
        ws.send(JSON.stringify({
            type: 'update_settings',
            settings: { mode, level, tps }
        }));
    }
}

// --- Deck Selection ---

async function loadInventory() {
    try {
        const res = await fetch(`/api/user/inventory?username=${username}`);
        const data = await res.json();
        if(data.status === 'success') {
            myInventory = data.inventory;
            myPlantLevels = data.plant_levels || {};
            plantSlots = data.plant_slots || 12;
            zombieSlots = data.zombie_slots || 10;
            // Use saved deck if available
            if (data.deck) {
                selectedDeck = data.deck;
            } else {
                selectedDeck = { plants: [], zombies: [] };
            }

            // Sync deck to server immediately
            if(ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'set_deck',
                    deck: selectedDeck,
                    plant_levels: myPlantLevels
                }));
            }
            
            // Don't auto-show, wait for button click
            // renderDeckSelection(); 
        }
    } catch (e) {
        console.error("Failed to load inventory", e);
    }
}

function renderDeckSelection() {
    renderSelectGrid('deck-plants', PLANT_CONFIGS, myInventory.plants, selectedDeck.plants, 'plants', myPlantLevels, plantSlots);
    renderSelectGrid('deck-zombies', ZOMBIE_CONFIGS, myInventory.zombies, selectedDeck.zombies, 'zombies', {}, zombieSlots);
}

function renderSelectGrid(elementId, configs, ownedList, selectedList, type, levels = {}, maxSlots = 10) {
    const container = document.getElementById(elementId);
    if(!container) return;
    container.innerHTML = '';
    
    // 按照 configs 中的定义顺序排序 ownedList
    const configKeys = Object.keys(configs);
    const sortedOwnedList = ownedList.slice().sort((a, b) => {
        const indexA = configKeys.indexOf(a);
        const indexB = configKeys.indexOf(b);
        return indexA - indexB;
    });
    
    // 显示当前选择数量/上限
    const counterDiv = document.createElement('div');
    counterDiv.style.cssText = 'width:100%; text-align:center; padding:8px; margin-bottom:10px; background:rgba(0,0,0,0.3); border-radius:5px; color:#ecf0f1; font-weight:bold;';
    const currentCount = selectedList.length;
    const isOverLimit = currentCount > maxSlots;
    counterDiv.innerHTML = `已选择: <span style="color:${isOverLimit ? '#e74c3c' : '#2ecc71'}">${currentCount}</span> / ${maxSlots}`;
    container.appendChild(counterDiv);
    
    sortedOwnedList.forEach(key => {
        if(!configs[key]) return;
        const item = configs[key];
        const isSelected = selectedList.includes(key);
        const level = levels[key] || 0;
        
        const div = document.createElement('div');
        div.className = `card ${isSelected ? 'owned' : ''}`;
        div.style.cursor = 'pointer';
        div.style.border = isSelected ? '2px solid #2ecc71' : '1px solid #95a5a6';
        div.style.backgroundColor = isSelected ? 'rgba(46, 204, 113, 0.2)' : 'rgba(0,0,0,0.2)';
        div.style.opacity = isSelected ? '1' : '0.7';
        div.style.width = '70px';
        div.style.height = '90px';
        div.style.display = 'flex';
        div.style.flexDirection = 'column';
        div.style.alignItems = 'center';
        div.style.justifyContent = 'center';
        div.style.margin = '2px';
        div.style.borderRadius = '5px';
        div.style.color = '#ecf0f1';
        div.style.position = 'relative';
        
        div.innerHTML = `
            <img src="${item.img}" style="width:45px;height:45px;object-fit:contain; margin-bottom:5px;">
            <div style="font-size:10px; text-align:center;">${item.name}</div>
            ${type === 'plants' ? `<div style="position:absolute; top:2px; right:2px; background:rgba(0,0,0,0.5); color:gold; padding:1px 3px; border-radius:3px; font-size:8px;">Lv.${level}</div>` : ''}
        `;
        
        div.onclick = () => toggleSelection(type, key, maxSlots);
        container.appendChild(div);
    });
}

function toggleSelection(type, key, maxSlots = 10) {
    const list = selectedDeck[type];
    const idx = list.indexOf(key);
    if(idx >= 0) {
        // 取消选择
        list.splice(idx, 1);
    } else {
        // 添加选择，检查是否超过上限
        if(list.length >= maxSlots) {
            alert(`最多只能选择 ${maxSlots} 张卡牌！`);
            return;
        }
        list.push(key);
    }
    renderDeckSelection();
}

console.log("room.js loaded successfully");
