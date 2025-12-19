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
            },
            onSelectShovel: () => {
                this.inputHandler.selectShovel();
                this.uiManager.update(this.gameState, this.gameState.myRole, this.inputHandler.getSelectedItem());
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
        this.uiManager.handleEvents(events);
        this.renderer.handleEvents(events, this.particleSystem);
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

        const inputState = {
            hoverCol: this.inputHandler.hoverCol,
            hoverRow: this.inputHandler.hoverRow,
            isShovelSelected: this.inputHandler.isShovelSelected,
            isBottom: this.inputHandler.isBottom
        };
        this.renderer.draw(this.gameState, this.particleSystem, inputState);
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
