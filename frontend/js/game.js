import { Config } from './config.js';
import { AssetManager } from './modules/AssetManager.js';
import { GameState } from './modules/GameState.js';
import { Network } from './modules/Network.js';
import { Renderer } from './modules/Renderer.js';
import { UIManager } from './modules/UIManager.js';
import { InputHandler } from './modules/InputHandler.js';
import { ParticleSystem } from './modules/ParticleSystem.js';

class Game {
    constructor() {
        this.canvas = document.getElementById('game');
        this.username = sessionStorage.getItem('username');
        if(!this.username) window.location.href = 'index.html';

        const urlParams = new URLSearchParams(window.location.search);
        this.roomId = urlParams.get('roomId');
        if(!this.roomId) window.location.href = 'lobby.html';

        this.assetManager = new AssetManager();
        this.gameState = new GameState();
        this.particleSystem = new ParticleSystem();
        this.renderer = new Renderer(this.canvas, this.assetManager);
        
        this.uiManager = new UIManager({
            onSelectPlant: (type) => {
                this.inputHandler.selectPlant(type);
                this.uiManager.update(this.gameState, this.gameState.myRole, type);
            },
            onSelectZombie: (type) => {
                this.inputHandler.selectZombie(type);
                this.uiManager.update(this.gameState, this.gameState.myRole, type);
            }
        });

        this.network = new Network(this.roomId, this.username, {
            onOpen: () => {},
            onStartGame: (config) => {
                Config.update(config);
                this.renderer.resize();
            },
            onGameState: (msg) => {
                this.gameState.update(msg, this.username);
                this.uiManager.update(this.gameState, this.gameState.myRole, this.inputHandler.getSelectedItem());
                this.handleEvents(msg.events);
            }
        });

        this.inputHandler = new InputHandler(this.canvas, this.network, this.gameState);
        
        this.lastTime = performance.now();
        this.loop = this.loop.bind(this);
    }

    start() {
        this.assetManager.preload();
        this.network.connect();
        requestAnimationFrame(this.loop);
    }

    handleEvents(events) {
        if(!events) return;
        events.forEach(e => {
            if(e.kind === 'watermelon_splash'){
                this.particleSystem.spawn(e.x, e.y, '#2e8b57', 15, {style: 'splash'});
            } else if(e.kind === 'bomb_splash'){
                this.particleSystem.spawn(e.x, e.y, '#c0392b', 15, {style: 'splash'});
            } else if(e.kind === 'jalapeno_explosion'){
                const c = Math.floor(e.x / Config.CELL_W);
                const r = Math.floor(e.y / Config.CELL_H);

                // Row fire
                for(let i=0; i<Config.COLS; i++){
                    const tx = i * Config.CELL_W + Config.CELL_W/2;
                    const ty = r * Config.CELL_H + Config.CELL_H/2;
                    this.particleSystem.spawn(tx, ty, '#ff4500', 15, {style: 'fire'});
                    this.particleSystem.spawn(tx, ty, '#ffcc00', 5, {style: 'fire'});
                }

                // Column fire
                for(let i=0; i<Config.ROWS; i++){
                    if(i === r) continue; 
                    const tx = c * Config.CELL_W + Config.CELL_W/2;
                    const ty = i * Config.CELL_H + Config.CELL_H/2;
                    this.particleSystem.spawn(tx, ty, '#ff4500', 15, {style: 'fire'});
                    this.particleSystem.spawn(tx, ty, '#ffcc00', 5, {style: 'fire'});
                }
            } else if(e.kind === 'ice_explosion'){
                this.particleSystem.spawn(e.x, e.y, '#aee7ff', 26, {style: 'spark'});
                this.particleSystem.spawn(e.x, e.y, '#4da3ff', 10, {style: 'smoke'});
            } else if(e.kind === 'mimic_transform'){
                this.particleSystem.spawn(e.x, e.y, '#999999', 15, {style: 'spark'});
            }
        });
    }

    loop() {
        const now = performance.now();
        const dt = now - this.lastTime;
        this.lastTime = now;

        this.gameState.updateInterpolation();
        this.particleSystem.update(dt);
        
        // Bullet trails
        Object.values(this.gameState.bullets).forEach(b => {
            if(b.type === 'citron_plasma' && Math.random() < 0.3){
                 this.particleSystem.spawn(b.x + (b.w||20)/2, b.y + (b.h||20)/2, '#00FFFF', 1, {style: 'spark'});
            } else if(b.type === 'arrow' && Math.random() < 0.4){
                 // Magic Archer trail
                 const cx = b.x + (b.w||40)/2;
                 const cy = b.y + (b.h||10)/2;
                 this.particleSystem.spawn(cx, cy, '#00FFFF', 1, {style: 'spark'});
            }
        });

        this.renderer.draw(this.gameState, this.particleSystem);
        requestAnimationFrame(this.loop);
    }
}

const game = new Game();
game.start();

// Expose for back button
window.backToLobby = function() {
    game.network.close();
    window.location.href = 'lobby.html';
};
