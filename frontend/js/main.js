const API_URL = ""; // 相对路径

// 页面元素
const authPage = document.getElementById('auth-page');
const lobbyPage = document.getElementById('lobby-page');
const gamePage = document.getElementById('game-page');
const authMsg = document.getElementById('auth-msg');

let currentUser = null;

// --- 认证逻辑 ---

async function handleLogin() {
    const u = document.getElementById('username').value;
    const p = document.getElementById('password').value;
    if(!u || !p) return showMsg("请输入用户名和密码");

    try {
        const res = await fetch(`${API_URL}/api/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: u, password: p})
        });
        const data = await res.json();
        if(res.ok) {
            currentUser = data.username;
            showLobby();
        } else {
            showMsg(data.detail);
        }
    } catch(e) {
        showMsg("连接服务器失败");
    }
}

async function handleRegister() {
    const u = document.getElementById('username').value;
    const p = document.getElementById('password').value;
    if(!u || !p) return showMsg("请输入用户名和密码");

    try {
        const res = await fetch(`${API_URL}/api/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: u, password: p})
        });
        const data = await res.json();
        if(res.ok) {
            showMsg("注册成功，请登录", "green");
        } else {
            showMsg(data.detail);
        }
    } catch(e) {
        showMsg("连接服务器失败");
    }
}

function showMsg(msg, color="red") {
    authMsg.textContent = msg;
    authMsg.style.color = color;
}

// --- 页面切换 ---

function showLobby() {
    authPage.classList.add('hidden');
    gamePage.classList.add('hidden');
    lobbyPage.classList.remove('hidden');
    document.getElementById('welcome-msg').textContent = `欢迎, ${currentUser}`;
    document.body.style.justifyContent = 'center'; // 居中显示菜单
}

function logout() {
    currentUser = null;
    lobbyPage.classList.add('hidden');
    authPage.classList.remove('hidden');
}

function startGame(mode) {
    lobbyPage.classList.add('hidden');
    gamePage.classList.remove('hidden');
    document.getElementById('game-mode-display').textContent = mode === 'pve' ? "单人模式" : "联机对战";
    document.body.style.justifyContent = 'flex-start'; // 游戏时靠上或自由布局
    
    // 初始化游戏 (在 game.js 中定义)
    if(window.initGame) window.initGame(mode);
}

function backToLobby() {
    // 停止游戏循环
    if(window.stopGame) window.stopGame();
    showLobby();
}