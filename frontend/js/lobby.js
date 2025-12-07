const username = sessionStorage.getItem('username');
if(!username) window.location.href = 'index.html';

document.getElementById('welcome-msg').textContent = `欢迎, ${username}`;

async function loadRooms() {
    const list = document.getElementById('room-list');
    list.innerHTML = '<p>加载中...</p>';
    try {
        const res = await fetch('/api/rooms');
        const rooms = await res.json();
        list.innerHTML = '';
        if(rooms.length === 0) {
            list.innerHTML = '<p>暂无房间，请创建</p>';
            return;
        }
        rooms.forEach(room => {
            const div = document.createElement('div');
            div.className = 'mode-card'; // Reuse style
            div.style.margin = '10px';
            div.style.cursor = 'pointer';
            const roomName = room.name || `房间 ${room.id}`;
            div.innerHTML = `<h3>${roomName}</h3><p>ID: ${room.id}</p><p>玩家: ${room.players}/2 - ${room.state}</p>`;
            div.onclick = () => joinRoom(room.id);
            list.appendChild(div);
        });
    } catch(e) {
        list.innerHTML = '<p>加载失败</p>';
    }
}

async function createRoom() {
    try {
        const res = await fetch('/api/rooms', { method: 'POST' });
        const data = await res.json();
        if(res.ok) {
            window.location.href = `room.html?roomId=${data.room_id}`;
        } else {
            alert(data.detail);
        }
    } catch(e) {
        alert("创建失败");
    }
}

function joinRoom(roomId) {
    window.location.href = `room.html?roomId=${roomId}`;
}

function logout() {
    sessionStorage.clear();
    window.location.href = 'index.html';
}

loadRooms();
setInterval(loadRooms, 5000); // Refresh every 5s