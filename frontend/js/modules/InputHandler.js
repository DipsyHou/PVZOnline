import { Config } from '../config.js';

export class InputHandler {
    constructor(canvas, network, gameState) {
        this.canvas = canvas;
        this.network = network;
        this.gameState = gameState;
        this.selectedPlant = 'peashooter';
        this.selectedZombie = 'normal';
        this.isShovelSelected = false;
        
        this.init();
    }

    init() {
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.hoverCol = -1;
        this.hoverRow = -1;
    }

    handleMouseMove(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        this.hoverCol = Math.floor(x / Config.CELL_W);
        this.hoverRow = Math.floor(y / Config.CELL_H);
        
        const relY = y % Config.CELL_H;
        this.isBottom = relY > (Config.CELL_H / 2);
    }

    handleClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const c = Math.floor(x / Config.CELL_W);
        const r = Math.floor(y / Config.CELL_H);
        
        const relY = y % Config.CELL_H;
        const isBottom = relY > (Config.CELL_H / 2);

        if(c >= 0 && c < Config.COLS && r >= 0 && r < Config.ROWS) {
            if(this.gameState.myRole === 'plant') {
                if (this.isShovelSelected) {
                    this.network.sendShovel(c, r, isBottom);
                    this.isShovelSelected = false;
                    this.canvas.style.cursor = 'default';
                } else {
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
                }
            } else if (this.gameState.myRole === 'zombie') {
                this.network.sendSpawnZombie(r, this.selectedZombie);
            }
        }
    }

    selectPlant(type) {
        this.selectedPlant = type;
        this.isShovelSelected = false;
        this.canvas.style.cursor = 'default';
    }

    selectZombie(type) {
        this.selectedZombie = type;
    }

    selectShovel() {
        this.isShovelSelected = !this.isShovelSelected;
        if(this.isShovelSelected) {
             this.canvas.style.cursor = `url('assets/svg/shovel.svg') 25 25, auto`;
        } else {
             this.canvas.style.cursor = 'default';
        }
    }
    
    getSelectedItem() {
        if (this.gameState.myRole === 'plant') {
            if (this.isShovelSelected) return 'shovel';
            return this.selectedPlant;
        }
        if (this.gameState.myRole === 'zombie') return this.selectedZombie;
        return null;
    }
}
