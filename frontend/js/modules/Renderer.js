import { Config } from '../config.js';

export class Renderer {
    constructor(canvas, assetManager) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.assetManager = assetManager;
    }

    resize() {
        this.canvas.width = Config.SCREEN_WIDTH;
        this.canvas.height = Config.SCREEN_HEIGHT;
    }

    handleEvents(events, particleSystem) {
        events.forEach(e => {
            if(e.kind === 'watermelon_splash'){
                particleSystem.spawn(e.x, e.y, '#2e8b57', 15, {style: 'splash'});
            } else if(e.kind === 'grape_splash'){
                particleSystem.spawn(e.x, e.y, '#800080', 15, {style: 'splash'});
            } else if(e.kind === 'bomb_splash'){
                particleSystem.spawn(e.x, e.y, '#c0392b', 15, {style: 'splash'});
            } else if(e.kind === 'jalapeno_explosion'){
                const c = Math.floor(e.x / Config.CELL_W);
                const r = Math.floor(e.y / Config.CELL_H);

                // Row fire
                for(let i=0; i<Config.COLS; i++){
                    const tx = i * Config.CELL_W + Config.CELL_W/2;
                    const ty = r * Config.CELL_H + Config.CELL_H/2;
                    particleSystem.spawn(tx, ty, '#ff4500', 15, {style: 'fire'});
                    particleSystem.spawn(tx, ty, '#ffcc00', 5, {style: 'fire'});
                }

                // Column fire
                for(let i=0; i<Config.ROWS; i++){
                    if(i === r) continue; 
                    const tx = c * Config.CELL_W + Config.CELL_W/2;
                    const ty = i * Config.CELL_H + Config.CELL_H/2;
                    particleSystem.spawn(tx, ty, '#ff4500', 15, {style: 'fire'});
                    particleSystem.spawn(tx, ty, '#ffcc00', 5, {style: 'fire'});
                }
            } else if(e.kind === 'ice_explosion'){
                particleSystem.spawn(e.x, e.y, '#aee7ff', 26, {style: 'spark'});
                particleSystem.spawn(e.x, e.y, '#4da3ff', 10, {style: 'smoke'});
            } else if(e.kind === 'mimic_transform'){
                particleSystem.spawn(e.x, e.y, '#999999', 15, {style: 'spark'});
            } else if(e.kind === 'explosion'){
                particleSystem.spawn(e.x, e.y, '#ff4500', 30, {style: 'splash'});
                particleSystem.spawn(e.x, e.y, '#ffcc00', 15, {style: 'fire'});
            } else if(e.kind === 'christmas_explosion'){
                particleSystem.spawn(e.x, e.y, null, 5, {style: 'confetti'});
                // particleSystem.spawn(e.x, e.y, '#ff0000', 10, {style: 'spark'});
                particleSystem.spawn(e.x, e.y, '#ffffff', 20, {style: 'spark'});
            } else if(e.kind === 'smash'){
                particleSystem.spawn(e.x, e.y, '#ff0000', 20, {style: 'spark'});
                particleSystem.spawn(e.x, e.y, '#8B0000', 10, {style: 'splash'});
            } else if(e.kind === 'hook_pull'){
                particleSystem.spawn(e.x, e.y, '#ffffff', 10, {style: 'ring'});
            } else if(e.kind === 'dust'){
                particleSystem.spawn(e.x, e.y, '#dddddd', 10, {style: 'smoke'});
            } else if(e.kind === 'acid_corrosion'){
                particleSystem.spawn(e.x, e.y, '#ffffff', 5, {style: 'smoke'});
            }
        });
    }

    draw(gameState, particleSystem, inputState) {
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw Grid
        this.drawGrid();

        // Draw Plants
        Object.values(gameState.plants).forEach(p => this.drawPlant(p, gameState, inputState));

        // Draw Zombies
        Object.values(gameState.zombies).forEach(z => this.drawZombie(z, gameState));

        // Draw Bullets
        Object.values(gameState.bullets).forEach(b => this.drawBullet(b));

        // Draw Particles
        if (particleSystem) particleSystem.draw(ctx);
    }

    drawGrid() {
        const ctx = this.ctx;
        ctx.save();
        ctx.strokeStyle = 'rgba(0,0,0,0.3)';
        ctx.lineWidth = 1;
        for(let r=0; r<Config.ROWS; r++) {
            for(let c=0; c<Config.COLS; c++) {
                ctx.strokeRect(c*Config.CELL_W, r*Config.CELL_H, Config.CELL_W, Config.CELL_H);
            }
        }
        ctx.restore();
    }

    drawPlant(p, gameState, inputState) {
        const ctx = this.ctx;
        
        // Highlight if shovel is selected and mouse is over this plant
        let shouldHighlight = false;
        if (inputState && inputState.isShovelSelected) {
             const pc = Math.floor(p.x / Config.CELL_W);
             const pr = Math.floor(p.y / Config.CELL_H);
             if (pc === inputState.hoverCol && pr === inputState.hoverRow) {
                 // Check if this cell has both pumpkin and normal plant
                 const cellPlants = Object.values(gameState.plants).filter(op => 
                     Math.floor(op.x/Config.CELL_W) === pc && Math.floor(op.y/Config.CELL_H) === pr
                 );
                 const hasPumpkin = cellPlants.some(cp => cp.type === 'spiky_pumpkin');
                 const hasNormal = cellPlants.some(cp => cp.type !== 'spiky_pumpkin' && cp.type !== 'time_machine' && cp.type !== 'reshaper');
                 
                 if (hasPumpkin && hasNormal) {
                     if (p.type === 'spiky_pumpkin') {
                         shouldHighlight = inputState.isBottom;
                     } else if (p.type !== 'spiky_pumpkin' && p.type !== 'time_machine' && p.type !== 'reshaper') {
                         shouldHighlight = !inputState.isBottom;
                     }
                 } else {
                     // Only one type (or floating), highlight whatever is there
                     shouldHighlight = true;
                 }
             }
        }

        ctx.save();
        if (shouldHighlight) {
            ctx.filter = 'brightness(1.5)';
        }

        const img = this.assetManager.getImage(p.type);
        if (img && img.complete) {
            ctx.drawImage(img, p.x, p.y, Config.PLANT_W, Config.PLANT_H);
        } else {
            ctx.fillStyle = '#00ff00';
            ctx.fillRect(p.x, p.y, Config.PLANT_W, Config.PLANT_H);
        }
        ctx.restore();

        // HP Bar
        const hpRatio = p.hp / p.max_hp;
        const barH = 6;
        let barY = p.y; // Default top
        
        if (p.type === 'spiky_pumpkin') {
            // Draw at bottom for Pumpkin
            barY = p.y + Config.PLANT_H - barH - 2;
        }
        
        // Background
        ctx.fillStyle = 'rgba(0,0,0,0.6)';
        ctx.fillRect(p.x, barY, Config.PLANT_W, barH);
        
        // HP
        ctx.fillStyle = '#ff4444';
        ctx.fillRect(p.x, barY, Config.PLANT_W * hpRatio, barH);
        
        // Border
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 1;
        ctx.strokeRect(p.x, barY, Config.PLANT_W, barH);
        
        // Overlay
        this.drawPlantOverlay(ctx, p, gameState);
    }

    drawZombie(z, gameState) {
        const ctx = this.ctx;
        const img = this.assetManager.getImage(z.type);
        
        ctx.save();
        if (z.is_slowed) {
            // Apply blue-ish filter for slow effect (copied from page project)
            ctx.filter = 'sepia(1) hue-rotate(200deg) saturate(4) brightness(0.7)';
        }

        if (img && img.complete) {
            ctx.drawImage(img, z.x, z.y, Config.ZOMBIE_W, Config.ZOMBIE_H);
        } else {
            ctx.fillStyle = '#555555';
            ctx.fillRect(z.x, z.y, Config.ZOMBIE_W, Config.ZOMBIE_H);
        }
        ctx.restore();

        // Gargantuar Hammer
        if(z.type === 'gargantuar' && z.smash_timer > 0){
            ctx.save();
            const pivotX = z.x + Config.ZOMBIE_W * 0.7;
            const pivotY = z.y + Config.ZOMBIE_H * 0.4;
            
            const p = z.smash_timer / 1.0; 
            const angle = -Math.PI/2 - (Math.PI/2 * p);
            
            ctx.translate(pivotX, pivotY);
            ctx.rotate(angle);
            
            ctx.fillStyle = '#654321';
            ctx.fillRect(0, -4, 50, 8);
            ctx.fillStyle = '#444';
            ctx.fillRect(50, -15, 25, 30);
            ctx.restore();
        }

        // Fisher Line
        if(z.type === 'fisher' && z.is_hooking && z.hook_target_id){
            const target = gameState.plants[z.hook_target_id];
            if(target){
                const startX = z.x + 10;
                const startY = z.y + Config.ZOMBIE_H/2;
                const endX = target.x + Config.PLANT_W/2;
                const endY = target.y + Config.PLANT_H/2;
                
                // Animation: extend line based on charge time (0 to 1.0s)
                const progress = Math.min(1, (z.hook_charge_time || 0) / 1.0);
                const curX = startX + (endX - startX) * progress;
                const curY = startY + (endY - startY) * progress;

                ctx.beginPath();
                ctx.moveTo(startX, startY);
                ctx.lineTo(curX, curY);
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // Hook graphic
                ctx.fillStyle = '#888';
                ctx.beginPath();
                ctx.arc(curX, curY, 5, 0, Math.PI*2);
                ctx.fill();
            }
        }

        // Priest Healing Beam
        if(z.type === 'priest' && z.heal_target_id){
            const target = gameState.zombies[z.heal_target_id];
            if(target){
                const startX = z.x + Config.ZOMBIE_W/2;
                const startY = z.y + Config.ZOMBIE_H/2;
                const endX = target.x + Config.ZOMBIE_W/2;
                const endY = target.y + Config.ZOMBIE_H/2;
                
                ctx.save();
                ctx.beginPath();
                ctx.moveTo(startX, startY);
                ctx.lineTo(endX, endY);
                ctx.strokeStyle = 'rgba(0, 255, 0, 0.5)';
                ctx.lineWidth = 4;
                ctx.stroke();
                
                // Pulse effect
                const time = Date.now() / 200;
                ctx.strokeStyle = `rgba(200, 255, 200, ${Math.abs(Math.sin(time))})`;
                ctx.lineWidth = 2;
                ctx.stroke();
                ctx.restore();
            }
        }

        // HP Bar & Armor Bar
        const barW = Config.ZOMBIE_W;
        const barH = 6;
        
        // HP Bar (Top)
        const hpY = z.y;
        ctx.fillStyle = 'rgba(0,0,0,0.7)'; // Background
        ctx.fillRect(z.x, hpY, barW, barH);
        ctx.fillStyle = '#ff3333'; // HP Color
        ctx.fillRect(z.x, hpY, Math.max(0, barW * (z.hp / z.max_hp)), barH);
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1;
        ctx.strokeRect(z.x, hpY, barW, barH);

        // Armor Bar (Below HP)
        if (z.armor > 0 && z.max_armor > 0) {
            const armorY = z.y + 7;
            ctx.fillStyle = 'rgba(0,0,0,0.7)'; // Background
            ctx.fillRect(z.x, armorY, barW, barH);
            ctx.fillStyle = '#bdc3c7'; // Armor Color
            ctx.fillRect(z.x, armorY, Math.max(0, barW * (z.armor / z.max_armor)), barH);
            ctx.strokeRect(z.x, armorY, barW, barH);
        }

        // Stun effect (Butter)
        if (z.is_stunned) {
            ctx.save();
            ctx.fillStyle = '#FFEB3B';
            ctx.fillRect(z.x + Config.ZOMBIE_W/2 - 10, z.y, 20, 15);
            ctx.strokeStyle = '#FBC02D';
            ctx.lineWidth = 2;
            ctx.strokeRect(z.x + Config.ZOMBIE_W/2 - 10, z.y, 20, 15);
            ctx.restore();
        }
    }

    drawBullet(b) {
        const ctx = this.ctx;
        const x = b.x;
        const y = b.y;
        const w = b.w || Config.BULLET_W;
        const h = b.h || Config.BULLET_H;
        const radius = w / 2;
        const kind = b.type; 
        const isFire = b.is_fire;

        ctx.save();
        
        if(kind === 'watermelon'){
            ctx.fillStyle = '#2e8b57';
            ctx.beginPath(); ctx.arc(x + radius, y + radius, radius, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#fff'; ctx.font='10px Arial'; ctx.fillText('W', x, y+10);
        }
        else if(kind === 'grape'){
            // 一串葡萄（主弹）
            ctx.save();
            ctx.translate(x + radius, y + radius);
            // 叶子
            ctx.beginPath();
            ctx.ellipse(10, -18, 10, 5, Math.PI/6, 0, 2*Math.PI);
            ctx.fillStyle = '#43A047';
            ctx.globalAlpha = 0.7;
            ctx.fill();
            ctx.globalAlpha = 1.0;
            // 葡萄粒
            ctx.beginPath(); ctx.arc(-8, 0, radius/2, 0, Math.PI*2); ctx.fillStyle = '#8E24AA'; ctx.fill();
            ctx.beginPath(); ctx.arc(0, 0, radius/1.2, 0, Math.PI*2); ctx.fillStyle = '#7B1FA2'; ctx.fill();
            ctx.beginPath(); ctx.arc(8, 0, radius/2, 0, Math.PI*2); ctx.fillStyle = '#8E24AA'; ctx.fill();
            ctx.beginPath(); ctx.arc(0, 10, radius/2, 0, Math.PI*2); ctx.fillStyle = '#9C27B0'; ctx.fill();
            // 高光
            ctx.beginPath(); ctx.arc(-3, -3, 2, 0, Math.PI*2); ctx.fillStyle = '#fff'; ctx.globalAlpha = 0.4; ctx.fill();
            ctx.globalAlpha = 1.0;
            ctx.restore();
        }
        else if(kind === 'grape_small'){
            // 单颗葡萄粒
            ctx.save();
            ctx.translate(x + radius, y + radius);
            ctx.beginPath(); ctx.arc(0, 0, radius/2, 0, Math.PI*2); ctx.fillStyle = '#8E24AA'; ctx.shadowColor = '#512DA8'; ctx.shadowBlur = 3; ctx.fill();
            ctx.beginPath(); ctx.arc(-1, -1, 1, 0, Math.PI*2); ctx.fillStyle = '#fff'; ctx.globalAlpha = 0.5; ctx.fill();
            ctx.globalAlpha = 1.0;
            ctx.restore();
        }
        else if(kind === 'bomb'){
            ctx.fillStyle = '#c0392b';
            ctx.beginPath(); ctx.arc(x + radius, y + radius, radius, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#fff'; ctx.font='10px Arial'; ctx.fillText('X', x, y+10);
        }
        else if(kind === 'citron_plasma'){
            ctx.fillStyle = '#00FFFF';
            if(radius >= 20) ctx.fillStyle = '#FF0066';
            ctx.shadowBlur = 10;
            ctx.shadowColor = ctx.fillStyle;
            ctx.beginPath(); ctx.arc(x + radius, y + radius, radius, 0, Math.PI*2); ctx.fill();
            ctx.shadowBlur = 0;
        }
        else if(kind === 'acid_juice'){
            ctx.save();
            ctx.translate(x + radius, y + radius);
            
            // Draw liquid drop shape
            ctx.fillStyle = '#DFFF00'; // Acid yellow-green
            ctx.shadowBlur = 5;
            ctx.shadowColor = '#ADFF2F';
            
            ctx.beginPath();
            // Teardrop shape
            ctx.moveTo(0, -radius);
            ctx.bezierCurveTo(radius, -radius, radius, radius, 0, radius);
            ctx.bezierCurveTo(-radius, radius, -radius, -radius, 0, -radius);
            ctx.fill();
            
            // Inner highlight
            ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            ctx.beginPath();
            ctx.ellipse(-radius*0.3, -radius*0.3, radius*0.2, radius*0.4, Math.PI/4, 0, Math.PI*2);
            ctx.fill();
            
            ctx.restore();
        }
        else if(kind === 'corn'){
            if(isFire){
                ctx.fillStyle = '#FFF';
                ctx.beginPath(); 
                for(let i=0; i<5; i++){
                    const angle = i * Math.PI * 2 / 5;
                    const r = 8;
                    ctx.arc(x + radius + Math.cos(angle)*5, y + radius + Math.sin(angle)*5, r, 0, Math.PI*2);
                }
                ctx.fill();
            } else {
                ctx.fillStyle = '#FFEB3B';
                ctx.beginPath(); ctx.arc(x + radius, y + radius, 5, 0, Math.PI*2); ctx.fill();
            }
        }
        else if(kind === 'butter'){
            ctx.fillStyle = '#FFEB3B';
            ctx.fillRect(x, y, 16, 12);
            ctx.strokeStyle = '#FBC02D';
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, 16, 12);
        }
        else if(kind === 'branch'){
            ctx.save();
            ctx.translate(x + w/2, y + h/2);
            if (b.angle !== undefined) ctx.rotate(b.angle);
            
            ctx.fillStyle = isFire ? '#ff6b00' : '#8B4513';
            ctx.fillRect(-10, -2, 20, 4);
            // Draw a small leaf
            ctx.fillStyle = isFire ? '#ff4500' : '#228B22';
            ctx.beginPath();
            ctx.arc(5, 0, 4, 0, Math.PI*2);
            ctx.fill();
            ctx.restore();
        }
        else if(kind === 'needle'){
            const len = 26;
            const half = len/2;
            ctx.save();
            ctx.translate(x + w/2, y + h/2);
            ctx.fillStyle = isFire ? '#ff6b00' : '#2e8b57';
            ctx.beginPath();
            if(ctx.roundRect) {
                ctx.roundRect(-half, -2, len, 4, 2);
            } else {
                ctx.fillRect(-half, -2, len, 4);
            }
            ctx.fill();
            ctx.restore();
        }
        else if(kind === 'arrow'){
            ctx.save();
            ctx.translate(x + w/2, y + h/2);
            if (b.angle !== undefined) {
                ctx.rotate(b.angle);
            }
            
            // Magic Archer Effect: Glowing gradient shaft
            const headColor = '#ffffff';
            const tailColor = '#00ffff';
            const glowColor = '#0088ff';

            ctx.shadowBlur = 15;
            ctx.shadowColor = glowColor;

            // Gradient for the trail/shaft
            const grad = ctx.createLinearGradient(-w/2, 0, w/2, 0);
            grad.addColorStop(0, 'rgba(0,0,0,0)'); // Fade out tail
            grad.addColorStop(0.3, tailColor);
            grad.addColorStop(1, headColor);

            ctx.fillStyle = grad;
            
            // Draw sleek aerodynamic shape
            ctx.beginPath();
            ctx.moveTo(-w/2, 0);
            ctx.lineTo(w/4, -h/2); // Wing/Fin
            ctx.lineTo(w/2, 0);    // Tip
            ctx.lineTo(w/4, h/2);  // Wing/Fin
            ctx.closePath();
            ctx.fill();

            // Bright core line for intensity
            ctx.fillStyle = '#ffffff';
            ctx.globalAlpha = 0.8;
            ctx.beginPath();
            ctx.moveTo(-w/4, -1);
            ctx.lineTo(w/2, 0);
            ctx.lineTo(-w/4, 1);
            ctx.fill();
            ctx.globalAlpha = 1.0;
            
            ctx.restore();
        }
        else if(kind === 'grape_spawner'){
            // do nothting
        }
        else {
            // default pea etc
            ctx.fillStyle = isFire ? '#ff6b00' : '#33cc33';
            ctx.beginPath(); ctx.arc(x + radius, y + radius, radius, 0, Math.PI*2); ctx.fill();
        }

        ctx.restore();
    }

    drawPlantOverlay(ctx, p, gameState) {
        const cx = p.x + Config.PLANT_W/2;
        const cy = p.y + Config.PLANT_H/2;

        // Sunflower / GoldBloom / Mimic / TimeMachine Progress Ring
        let progress = 0;
        let color = '';
        
        if(p.type === 'sunflower' && p.shoot_interval){
            progress = (p.shoot_timer || 0) / p.shoot_interval;
            color = 'rgba(255, 200, 50, 0.9)';
        } else if(p.type === 'gold_bloom' && p.life_timer !== undefined){
            progress = p.life_timer / 8.0; // 8 seconds
            color = 'rgba(255, 215, 0, 0.9)';
        } else if(p.type === 'mimic' && p.mimic_timer !== undefined){
            progress = 1 - (p.mimic_timer / 3.0); // 3 seconds
            color = 'rgba(150, 150, 150, 0.9)';
        } else if(p.type === 'time_machine' && p.float_timer !== undefined){
            progress = 1 - (p.float_timer / 3.0);
            color = 'rgba(155, 231, 255, 0.9)';
        }

        if(progress > 0 && progress < 1){
            ctx.save();
            ctx.translate(cx, cy);
            const r = Config.PLANT_W/2 - 10;
            ctx.beginPath();
            ctx.arc(0,0,r, -Math.PI/2, -Math.PI/2 + (Math.PI*2*progress), false);
            ctx.strokeStyle = color;
            ctx.lineWidth = 5;
            ctx.lineCap = 'round';
            ctx.stroke();
            ctx.restore();
        }

        // Citron Charge Bar
        if(p.type === 'citron' && p.charge_time !== undefined){
            const barW = Config.PLANT_W - 16;
            const x = p.x + 8;
            const y = p.y + Config.PLANT_H + 2;
            const barH = 6;
            const maxCharge = 20.0;
            const ratio = Math.min(1, p.charge_time / maxCharge);
            
            ctx.fillStyle = 'rgba(0,0,0,0.5)';
            ctx.fillRect(x, y, barW, barH);

            let c = '#00FFFF';
            if(p.charge_time >= 20) c = '#FF0066';
            else if(p.charge_time >= 10) c = '#FF00FF';

            ctx.fillStyle = c;
            ctx.fillRect(x+1, y+1, Math.max(0, (barW-2) * ratio), barH-2);
        }

        // Laser Shroom
        if (p.type === 'laser_shroom' && p.laser_active_time > 0) {
            ctx.save();
            ctx.strokeStyle = `rgba(255, 0, 255, ${p.laser_active_time * 5})`; 
            ctx.lineWidth = 4;
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#FF00FF';
            
            const directions = [
                [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]
            ];
            
            directions.forEach(dir => {
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.lineTo(cx + dir[0] * Config.CELL_W * 2.5, cy + dir[1] * Config.CELL_H * 2.5);
                ctx.stroke();
            });
            ctx.restore();
        }

        // Electrode Cherry
        if (p.type === 'electrode_cherry' && p.paired_id) {
            const partner = gameState.plants[p.paired_id];
            if (partner) {
                const px = partner.x + Config.PLANT_W/2;
                const py = partner.y + Config.PLANT_H/2;
                
                ctx.save();
                ctx.strokeStyle = '#00FFFF';
                ctx.lineWidth = 3;
                ctx.shadowBlur = 10;
                ctx.shadowColor = '#00FFFF';
                
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                
                const dist = Math.sqrt((px-cx)**2 + (py-cy)**2);
                const steps = Math.floor(dist / 10);
                
                for(let i=1; i<steps; i++) {
                    const t = i / steps;
                    const tx = cx + (px - cx) * t;
                    const ty = cy + (py - cy) * t;
                    ctx.lineTo(tx + (Math.random()-0.5)*10, ty + (Math.random()-0.5)*10);
                }
                
                ctx.lineTo(px, py);
                ctx.stroke();
                ctx.restore();
            }
        }
    }
}
