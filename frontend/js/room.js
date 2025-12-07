const username = sessionStorage.getItem('username');
if(!username) window.location.href = 'index.html';

const urlParams = new URLSearchParams(window.location.search);
const roomId = urlParams.get('roomId');
if(!roomId) window.location.href = 'lobby.html';

document.getElementById('room-title').textContent = `房间 ${roomId}`;

// WebSocket for room state (players joining/leaving, settings change, game start)
const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const wsUrl = `${protocol}://${window.location.host}/ws/room/${roomId}?username=${username}`;
const ws = new WebSocket(wsUrl);

ws.onopen = () => {
    console.log("Connected to Room");
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if(msg.type === 'room_state') {
        updateRoomUI(msg.data);
    } else if (msg.type === 'start_game') {
        window.location.href = `game.html?roomId=${roomId}`;
    }
};

function updateRoomUI(data) {
    document.getElementById('room-title').textContent = data.name || `房间 ${data.room_id}`;

    const list = document.getElementById('player-list');
    list.innerHTML = '';
    data.players.forEach(p => {
        const div = document.createElement('div');
        div.textContent = p + (p === data.host ? " (房主)" : "");
        div.style.padding = "5px";
        div.style.borderBottom = "1px solid #eee";
        list.appendChild(div);
    });

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

    modeSelect.disabled = !isHost;
    levelSelect.disabled = !isHost;
    tpsSelect.disabled = !isHost;
    startBtn.disabled = !isHost; // Allow 1 player start for testing

    // Update values if not host (to sync with host)
    if(!isHost) {
        modeSelect.value = data.settings.mode;
        levelSelect.value = data.settings.level;
        tpsSelect.value = data.settings.tps || 30;
    }
}

function startGame() {
    ws.send(JSON.stringify({type: 'start_game'}));
}

function leaveRoom() {
    ws.close();
    window.location.href = 'lobby.html';
}

// Listen for settings changes by host
if(document.getElementById('game-mode')) {
    document.getElementById('game-mode').addEventListener('change', sendSettings);
    document.getElementById('game-level').addEventListener('change', sendSettings);
    document.getElementById('game-tps').addEventListener('change', sendSettings);
}

function sendSettings() {
    const mode = document.getElementById('game-mode').value;
    const level = document.getElementById('game-level').value;
    const tps = document.getElementById('game-tps').value;
    ws.send(JSON.stringify({
        type: 'update_settings',
        settings: { mode, level, tps }
    }));
}

function renameRoom() {
    const name = document.getElementById('room-name-input').value;
    if (name) {
        ws.send(JSON.stringify({
            type: 'rename_room',
            name: name
        }));
    }
}