export const PLANT_CONFIGS = {
    peashooter: { name: '豌豆', cost: 100, cooldown: 7, img: 'assets/png/peashooter.png' },
    sunflower: { name: '向日葵', cost: 50, cooldown: 7, img: 'assets/png/sunflower.png' },
    grape_pult: { name: '葡萄投手', cost: 225, cooldown: 7, img: 'assets/svg/grape_pult.svg' },
    pod_peashooter: { name: '豆荚', cost: 225, cooldown: 7, img: 'assets/png/peasecod.png' },
    bomber: { name: '石榴', cost: 200, cooldown: 7, img: 'assets/svg/bomber.svg' },
    torchwood: { name: '火炬', cost: 175, cooldown: 7, img: 'assets/png/torchwood.png' },
    watermelon: { name: '西瓜', cost: 300, cooldown: 7, img: 'assets/png/watermelon.png' },
    iced_coconut: { name: '冰椰', cost: 175, cooldown: 30, img: 'assets/png/iced-coconut.png' },
    trumpet: { name: '喇叭花', cost: 50, cooldown: 30, img: 'assets/svg/trumpet.svg' },
    pine_shooter: { name: '松针射手', cost: 150, cooldown: 7, img: 'assets/svg/pine-shooter.svg' },
    gold_bloom: { name: '黄金蓓蕾', cost: 150, cooldown: 50, img: 'assets/png/gold-blooms.png' },
    spiky_pumpkin: { name: '尖刺南瓜', cost: 150, cooldown: 30, img: 'assets/svg/spiky-pumpkin.svg' },
    jalapeno_pair: { name: '火爆双椒', cost: 225, cooldown: 30, img: 'assets/svg/jalapeno-pair.svg' },
    mimic: { name: '模仿者', cost: 325, cooldown: 30, img: 'assets/png/mimic.png' },
    reshaper: { name: '分解菌落', cost: 50, cooldown: 30, img: 'assets/svg/reshaper.svg' },
    time_machine: { name: '时光机', cost: 125, cooldown: 50, img: 'assets/svg/time-machine.svg' },
    laser_shroom: { name: '激光菇', cost: 300, cooldown: 15, img: 'assets/svg/laser-shroom.svg' },
    windmill: { name: '风车草', cost: 250, cooldown: 30, img: 'assets/svg/windmill.svg' },
    vine_trap: { name: '藤蔓陷阱', cost: 125, cooldown: 30, img: 'assets/svg/vine-trap.svg' },
    electrode_cherry: { name: '电极樱桃', cost: 175, cooldown: 15, img: 'assets/svg/electrode-cherry.svg' },
    wild_gatling: { name: '狂野机枪', cost: 450, cooldown: 30, img: 'assets/png/wild-gatling.png' },
    ninja_nut: { name: '忍者坚果', cost: 100, cooldown: 30, img: 'assets/png/ninja-nut.png' },
    citron: { name: '充能柚子', cost: 200, cooldown: 7, img: 'assets/png/citron.png' },
    corn_homing: { name: '玉米追踪', cost: 375, cooldown: 7, img: 'assets/svg/corn-homing.svg' },
    corn_gatling: { name: '玉米机枪', cost: 275, cooldown: 7, img: 'assets/svg/corn-gatling.svg' },
    jelly: { name: '果冻', cost: 125, cooldown: 7, img: 'assets/svg/jelly.svg' },
    binary_tree: { name: '二叉树', cost: 175, cooldown: 7, img: 'assets/svg/binary_tree.svg' },
    maguey: { name: '龙舌兰', cost: 300, cooldown: 15, img: 'assets/png/maguey.png' },
    christmas_nut: { name: '圣诞坚果', cost: 50, cooldown: 30, img: 'assets/png/christmas-nut.png' },
};

export const ZOMBIE_CONFIGS = {
    normal: { name: '普通', cost: 50, cooldown: 1, img: 'assets/png/zombie.png' },
    buckethead: { name: '铁桶', cost: 200, cooldown: 1, img: 'assets/png/bucket-zombie.png' },
    exploder: { name: '爆破', cost: 150, cooldown: 1, img: 'assets/svg/exploder-zombie.svg' },
    fisher: { name: '渔夫', cost: 200, cooldown: 1, img: 'assets/svg/fisher-zombie.svg' },
    football: { name: '橄榄球', cost: 400, cooldown: 1, img: 'assets/png/rugby-zombie.png' },
    football_forward: { name: '前锋', cost: 600, cooldown: 1, img: 'assets/png/football-forward.png' },
    gargantuar: { name: '巨人', cost: 900, cooldown: 1, img: 'assets/png/gargantuar.png' },
    priest: { name: '牧师', cost: 200, cooldown: 1, img: 'assets/svg/priest-zombie.svg' },
};

export const Config = {
    CELL_W: 100,
    CELL_H: 100,
    ROWS: 7,
    COLS: 11,
    SCREEN_WIDTH: 1100,
    SCREEN_HEIGHT: 700,
    PLANT_W: 60,
    PLANT_H: 60,
    ZOMBIE_W: 60,
    ZOMBIE_H: 80,
    BULLET_W: 20,
    BULLET_H: 20,
    
    PLANT_CONFIGS,
    ZOMBIE_CONFIGS,

    update(newConfig) {
        Object.assign(this, newConfig);
    }
};
