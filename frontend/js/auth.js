const API_URL = ""; 

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
            sessionStorage.setItem('username', data.username);
            sessionStorage.setItem('token', data.token);
            window.location.href = 'lobby.html';
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
    const authMsg = document.getElementById('auth-msg');
    authMsg.textContent = msg;
    authMsg.style.color = color;
}