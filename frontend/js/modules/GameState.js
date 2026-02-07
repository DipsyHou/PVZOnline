import { Config } from '../config.js';

export class GameState {
    constructor() {
        this.plants = {};
        this.zombies = {};
        this.bullets = {};
        this.sun = 50;
        this.brains = 50;
        this.cooldowns = {};
        this.myRole = null;
    }

    update(serverState, username) {
        this.myRole = serverState.roles[username];
        
        if (serverState.player_states && serverState.player_states[username]) {
            // Use per-player state
            const myState = serverState.player_states[username];
            this.sun = myState.sun;
            this.cooldowns = myState.cooldowns;
        } else {
            // Fallback to global state
            this.sun = serverState.sun || 0;
            this.cooldowns = serverState.cooldowns || {};
        }
        
        this.brains = serverState.brains || 0;
        
        this.syncObjects('plants', serverState.plants);
        this.syncObjects('zombies', serverState.zombies);
        this.syncObjects('bullets', serverState.bullets);
    }

    syncObjects(type, serverList) {
        const localMap = this[type];
        const serverIds = new Set();

        serverList.forEach(sObj => {
            serverIds.add(sObj.id);
            if (localMap[sObj.id]) {
                // Update existing
                const obj = localMap[sObj.id];
                
                // Save current interpolated position
                const currentX = obj.x;
                const currentY = obj.y;
                
                // Copy new properties from server
                Object.assign(obj, sObj);
                
                // Restore interpolated position
                obj.x = currentX;
                obj.y = currentY;
                
                // Set targets
                obj.targetX = sObj.x;
                obj.targetY = sObj.y;

            } else {
                // Create new
                localMap[sObj.id] = {
                    ...sObj,
                    targetX: sObj.x || 0,
                    targetY: sObj.y || 0,
                    // Ensure defaults
                    w: sObj.w || (type === 'bullets' ? Config.BULLET_W : (type === 'plants' ? Config.PLANT_W : Config.ZOMBIE_W)),
                    h: sObj.h || (type === 'bullets' ? Config.BULLET_H : (type === 'plants' ? Config.PLANT_H : Config.ZOMBIE_H)),
                };
            }
        });

        // Remove missing
        for (let id in localMap) {
            if (!serverIds.has(id)) {
                delete localMap[id];
            }
        }
    }

    updateInterpolation() {
        const factor = 0.2; 
        ['plants', 'zombies', 'bullets'].forEach(type => {
            for (let id in this[type]) {
                let obj = this[type][id];
                if(obj.targetX !== undefined) {
                    obj.x += (obj.targetX - obj.x) * factor;
                    if(Math.abs(obj.targetX - obj.x) < 0.5) obj.x = obj.targetX;
                }
                if(obj.targetY !== undefined) {
                    obj.y += (obj.targetY - obj.y) * factor;
                    if(Math.abs(obj.targetY - obj.y) < 0.5) obj.y = obj.targetY;
                }
            }
        });
    }
}
