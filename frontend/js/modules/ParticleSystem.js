export class ParticleSystem {
    constructor() {
        this.particles = [];
    }

    spawn(x, y, color, count, opts){
        const style = (opts && opts.style) ? opts.style : 'smoke';
        for(let i=0;i<count;i++){
            const angle = Math.random() * Math.PI * 2;
            let vx, vy, life, size, gravity;
            
            if(style === 'spark'){
                // Old spark/debris style
                const speed = 60 + Math.random()*240;
                vx = Math.cos(angle)*speed;
                vy = Math.sin(angle)*speed - 120; // slight upward
                life = 600;
                size = 2 + Math.random()*4;
                gravity = 1200;
            } else if(style === 'dust'){
                // Dust: small, falls slowly
                const speed = 10 + Math.random()*30;
                vx = Math.cos(angle)*speed;
                vy = Math.sin(angle)*speed;
                life = 400 + Math.random()*300;
                size = 2 + Math.random()*3;
                gravity = 50;
            } else if(style === 'ring'){
                // Ring: expands outward, no gravity
                const speed = 100 + Math.random()*50;
                vx = Math.cos(angle)*speed;
                vy = Math.sin(angle)*speed;
                life = 400;
                size = 3 + Math.random()*2;
                gravity = 0;
            } else if(style === 'splash'){
                // Splash: fast outward, gravity
                const speed = 50 + Math.random()*150;
                vx = Math.cos(angle)*speed;
                vy = Math.sin(angle)*speed - 50;
                life = 400;
                size = 3 + Math.random()*4;
                gravity = 800;
            } else if(style === 'fire'){
                // Fire: moves upward, chaotic
                const speed = 20 + Math.random()*60;
                const a = -Math.PI/2 + (Math.random()-0.5)*1.0; // Upward cone
                vx = Math.cos(a)*speed;
                vy = Math.sin(a)*speed;
                life = 300 + Math.random()*300;
                size = 20 + Math.random()*15;
                gravity = -100; // Float up
            } else {
                // Smoke style (default)
                const speed = 10 + Math.random() * 80;
                vx = Math.cos(angle) * speed * (0.5 + Math.random() * 0.8);
                vy = Math.sin(angle) * speed * 0.3 - (10 + Math.random() * 40);
                life = 300 + Math.random() * 500;
                size = 6 + Math.random() * 24;
                gravity = (opts && typeof opts.gravity === 'number') ? opts.gravity : (-10 - Math.random() * 60);
            }

            const col = color || 'rgba(200,200,200,0.6)';
            // slight jitter in spawn position
            const px = x + (Math.random() - 0.5) * 12;
            const py = y + (Math.random() - 0.5) * 8;
            this.particles.push({x: px, y: py, vx: vx, vy: vy, life: life, maxLife: life, color: col, size: size, gravity: gravity});
        }
    }

    update(dt) {
        const dtSec = dt / 1000;
        for(let i=this.particles.length-1;i>=0;i--){
            const p = this.particles[i];
            p.life -= dt;
            if(p.life <= 0){
                this.particles.splice(i,1);
                continue;
            }
            
            p.x += p.vx * dtSec;
            p.y += p.vy * dtSec;
            p.vy += p.gravity * dtSec;
            
            // Shrink
            if(p.life < 200) {
                p.size *= 0.95;
            }
        }
    }

    draw(ctx) {
        for(const p of this.particles){
            const alpha = Math.max(0, p.life / p.maxLife);
            ctx.fillStyle = p.color || '#ffb36b';
            ctx.globalAlpha = alpha;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI*2); ctx.fill();
            ctx.globalAlpha = 1;
        }
    }
}
