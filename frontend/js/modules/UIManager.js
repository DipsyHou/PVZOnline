import { Config } from '../config.js';

export class UIManager {
    constructor(callbacks) {
        this.callbacks = callbacks; // { onSelectPlant, onSelectZombie }
        this.sunContainer = document.getElementById('sun');
        this.plantSlotBar = document.getElementById('plant-slot-bar');
        this.brainsContainer = document.getElementById('brains');
        this.zombieSlotBar = document.getElementById('zombie-slot-bar');
        this.sunCount = document.getElementById('sun-count');
        this.brainsCount = document.getElementById('brains-count');
        
        this.generatedPlantCards = false;
        this.generatedZombieCards = false;
    }

    update(gameState, myRole, selectedItem) {
        const { sun, brains, cooldowns } = gameState;

        if (myRole === 'plant') {
            if(this.sunContainer) this.sunContainer.style.display = 'block';
            if(this.plantSlotBar) {
                this.plantSlotBar.style.display = 'flex';
                if(!this.generatedPlantCards) this.generatePlantCards();
            }
            if(this.brainsContainer) this.brainsContainer.style.display = 'none';
            if(this.zombieSlotBar) this.zombieSlotBar.style.display = 'none';
            
            if(this.sunCount) this.sunCount.textContent = sun;
            
            Object.keys(Config.PLANT_CONFIGS).forEach(type => {
                this.updatePlantButton(type, Config.PLANT_CONFIGS[type].cost, sun, cooldowns, selectedItem);
            });

        } else if (myRole === 'zombie') {
            if(this.sunContainer) this.sunContainer.style.display = 'none';
            if(this.plantSlotBar) this.plantSlotBar.style.display = 'none';
            if(this.brainsContainer) this.brainsContainer.style.display = 'block';
            if(this.zombieSlotBar) {
                this.zombieSlotBar.style.display = 'flex';
                if(!this.generatedZombieCards) this.generateZombieCards();
            }

            if(this.brainsCount) this.brainsCount.textContent = brains;

            Object.keys(Config.ZOMBIE_CONFIGS).forEach(type => {
                this.updateZombieButton(type, Config.ZOMBIE_CONFIGS[type].cost, brains, cooldowns, selectedItem);
            });
        } else {
            if(this.sunContainer) this.sunContainer.style.display = 'none';
            if(this.plantSlotBar) this.plantSlotBar.style.display = 'none';
            if(this.brainsContainer) this.brainsContainer.style.display = 'none';
            if(this.zombieSlotBar) this.zombieSlotBar.style.display = 'none';
        }
    }

    generatePlantCards() {
        this.plantSlotBar.innerHTML = '';
        Object.keys(Config.PLANT_CONFIGS).forEach(type => {
            const cfg = Config.PLANT_CONFIGS[type];
            const card = document.createElement('div');
            card.className = 'plant-card';
            card.id = `btn-${type}`;
            card.onclick = () => this.callbacks.onSelectPlant(type);
            
            card.innerHTML = `
                <img src="${cfg.img}" class="plant-card-icon" alt="${cfg.name}">
                <div class="name">${cfg.name}</div>
                <div class="cost">${cfg.cost}</div>
                <div class="cooldown-mask"></div>
            `;
            this.plantSlotBar.appendChild(card);
        });
        this.generatedPlantCards = true;
    }

    generateZombieCards() {
        this.zombieSlotBar.innerHTML = '';
        Object.keys(Config.ZOMBIE_CONFIGS).forEach(type => {
            const cfg = Config.ZOMBIE_CONFIGS[type];
            const card = document.createElement('div');
            card.className = 'plant-card'; // Reuse style
            card.id = `btn-${type}`;
            card.onclick = () => this.callbacks.onSelectZombie(type);
            
            card.innerHTML = `
                <img src="${cfg.img}" class="plant-card-icon" alt="${cfg.name}">
                <div class="name">${cfg.name}</div>
                <div class="cost">${cfg.cost}</div>
                <div class="cooldown-mask"></div>
            `;
            this.zombieSlotBar.appendChild(card);
        });
        this.generatedZombieCards = true;
    }

    updatePlantButton(type, cost, currentSun, cooldowns, selectedPlant) {
        const btn = document.getElementById(`btn-${type}`);
        if (!btn) return;
        
        const remaining = cooldowns[type] || 0;
        const total = Config.PLANT_CONFIGS[type].cooldown || 1;
        const overlay = btn.querySelector('.cooldown-mask');
        
        if (remaining > 0) {
            const pct = (remaining / total) * 100;
            if(overlay) overlay.style.height = `${pct}%`;
            btn.style.cursor = 'not-allowed';
        } else {
            if(overlay) overlay.style.height = '0%';
        }

        if (currentSun >= cost && remaining <= 0) {
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
            if (selectedPlant === type) {
                btn.classList.add('selected');
            } else {
                btn.classList.remove('selected');
            }
        } else {
            btn.classList.remove('selected');
            if (remaining > 0) {
                 btn.style.opacity = '0.8'; 
            } else {
                 btn.style.opacity = '0.5';
                 btn.style.cursor = 'not-allowed';
            }
        }
    }

    updateZombieButton(type, cost, currentBrains, cooldowns, selectedZombie) {
        const btn = document.getElementById(`btn-${type}`);
        if (!btn) return;
        
        const remaining = cooldowns[type] || 0;
        const total = Config.ZOMBIE_CONFIGS[type].cooldown || 1;
        const overlay = btn.querySelector('.cooldown-mask');
        
        if (remaining > 0) {
            const pct = (remaining / total) * 100;
            if(overlay) overlay.style.height = `${pct}%`;
            btn.style.cursor = 'not-allowed';
        } else {
            if(overlay) overlay.style.height = '0%';
        }

        if (currentBrains >= cost && remaining <= 0) {
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
            if (selectedZombie === type) {
                btn.classList.add('selected');
            } else {
                btn.classList.remove('selected');
            }
        } else {
            btn.classList.remove('selected');
            if (remaining > 0) {
                 btn.style.opacity = '0.8'; 
            } else {
                 btn.style.opacity = '0.5';
                 btn.style.cursor = 'not-allowed';
            }
        }
    }
}
