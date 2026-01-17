import { PLANT_CONFIGS, ZOMBIE_CONFIGS } from './config.js';

const username = sessionStorage.getItem('username');
if(!username) window.location.href = 'index.html';

async function loadInventory() {
    try {
        const res = await fetch(`/api/user/inventory?username=${username}`);
        const data = await res.json();
        if(data.status === 'success') {
            renderGrid('plant-grid', PLANT_CONFIGS, data.inventory.plants, data.plant_levels);
            renderGrid('zombie-grid', ZOMBIE_CONFIGS, data.inventory.zombies);
        }
    } catch (e) {
        console.error("Failed to load inventory", e);
    }
}

function renderGrid(elementId, configs, ownedList, levels = {}) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';
    
    Object.keys(configs).forEach(key => {
        const item = configs[key];
        const isOwned = ownedList.includes(key);
        const level = levels[key] || 0;
        
        const div = document.createElement('div');
        div.className = `card ${isOwned ? 'owned' : 'locked'}`;
        div.innerHTML = `
            <img src="${item.img}" alt="${item.name}">
            <div class="card-name">${item.name}</div>
            ${isOwned ? `<div class="card-level" style="position:absolute; top:2px; right:2px; background:rgba(0,0,0,0.5); color:gold; padding:1px 3px; border-radius:3px; font-size:10px;">Lv.${level}</div>` : ''}
            ${!isOwned ? '<div class="card-status">未拥有</div>' : ''}
        `;
        container.appendChild(div);
    });
}

loadInventory();
