import { Config } from '../config.js';

export class InputHandler {
    constructor(canvas, network, gameState) {
        this.canvas = canvas;
        this.network = network;
        this.gameState = gameState;
        this.selectedPlant = 'peashooter';
        this.selectedZombie = 'normal';
        
        this.init();
    }

    init() {
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
    }

    handleClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const c = Math.floor(x / Config.CELL_W);
        const r = Math.floor(y / Config.CELL_H);

        if(c >= 0 && c < Config.COLS && r >= 0 && r < Config.ROWS) {
            if(this.gameState.myRole === 'plant') {
                // Check if clicking on an activatable plant (Citron)
                let clickedActivatable = false;
                Object.values(this.gameState.plants).forEach(p => {
                    const pc = Math.floor(p.x / Config.CELL_W);
                    const pr = Math.floor(p.y / Config.CELL_H);
                    if(pc === c && pr === r && p.type === 'citron') {
                        clickedActivatable = true;
                    }
                });

                if(clickedActivatable) {
                    this.network.sendActivatePlant(c, r);
                } else {
                    this.network.sendPlacePlant(c, r, this.selectedPlant);
                }
            } else if (this.gameState.myRole === 'zombie') {
                this.network.sendSpawnZombie(r, this.selectedZombie);
            }
        }
    }

    selectPlant(type) {
        this.selectedPlant = type;
    }

    selectZombie(type) {
        this.selectedZombie = type;
    }
    
    getSelectedItem() {
        if (this.gameState.myRole === 'plant') return this.selectedPlant;
        if (this.gameState.myRole === 'zombie') return this.selectedZombie;
        return null;
    }
}
