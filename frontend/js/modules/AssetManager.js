import { PLANT_CONFIGS, ZOMBIE_CONFIGS } from '../config.js';

export class AssetManager {
    constructor() {
        this.images = {};
    }

    preload() {
        Object.keys(PLANT_CONFIGS).forEach(k => {
            const img = new Image();
            img.src = PLANT_CONFIGS[k].img;
            this.images[k] = img;
        });
        Object.keys(ZOMBIE_CONFIGS).forEach(k => {
            const img = new Image();
            img.src = ZOMBIE_CONFIGS[k].img;
            this.images[k] = img;
        });
    }

    getImage(key) {
        return this.images[key];
    }
}
