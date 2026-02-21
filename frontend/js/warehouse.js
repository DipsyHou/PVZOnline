import { PLANT_CONFIGS, ZOMBIE_CONFIGS } from './config.js';

const username = sessionStorage.getItem('username');
if(!username) window.location.href = 'index.html';

async function loadInventory() {
    try {
        const res = await fetch(`/api/user/inventory?username=${username}`);
        const data = await res.json();
        if(data.status === 'success') {
            renderGrid('plant-grid', PLANT_CONFIGS, data.inventory.plants, data.plant_levels, 'plant');
            renderGrid('zombie-grid', ZOMBIE_CONFIGS, data.inventory.zombies, {}, 'zombie');
        }
    } catch (e) {
        console.error("Failed to load inventory", e);
    }
}

function renderGrid(elementId, configs, ownedList, levels = {}, type = 'plant') {
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
        
        // 添加点击事件
        div.style.cursor = 'pointer';
        div.addEventListener('click', () => showDetailModal(key, item, type));
        
        container.appendChild(div);
    });
}

function showDetailModal(key, config, type) {
    const modal = document.getElementById('detail-modal');
    const categoryMap = {
        'normal': '普通植物',
        'carrier': '承载植物',
        'floating': '悬浮植物'
    };
    
    // 填充数据
    document.getElementById('modal-name').textContent = config.name;
    document.getElementById('modal-img').src = config.img;
    document.getElementById('modal-cost').textContent = type === 'plant' ? `${config.cost} 阳光` : `${config.cost} 脑子`;
    document.getElementById('modal-cooldown').textContent = `${config.cooldown} 秒`;
    
    // 生命值（悬浮植物不显示，僵尸必有，其他植物可选）
    if (config.hp && !(type === 'plant' && config.category === 'floating')) {
        document.getElementById('modal-hp-container').style.display = 'block';
        let hpText = config.hp.toString();
        if (config.armor) {
            hpText += ` + ${config.armor}护甲`;
        }
        document.getElementById('modal-hp').textContent = hpText;
    } else {
        document.getElementById('modal-hp-container').style.display = 'none';
    }
    
    // 类别（仅植物）
    if (type === 'plant' && config.category) {
        document.getElementById('modal-category-container').style.display = 'block';
        document.getElementById('modal-category').textContent = categoryMap[config.category] || config.category;
    } else {
        document.getElementById('modal-category-container').style.display = 'none';
    }
    
    // 描述
    document.getElementById('modal-desc').textContent = config.desc || '暂无描述';
    
    // 显示弹窗
    modal.style.display = 'flex';
}

window.closeDetailModal = function() {
    document.getElementById('detail-modal').style.display = 'none';
}

// 点击弹窗外部关闭
window.onclick = function(event) {
    const modal = document.getElementById('detail-modal');
    if (event.target === modal) {
        closeDetailModal();
    }
}

// ESC键关闭弹窗
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeDetailModal();
    }
});

loadInventory();
