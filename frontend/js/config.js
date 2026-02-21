export const PLANT_CONFIGS = {
    peashooter: { name: '豌豆射手', cost: 100, cooldown: 7, hp: 200, category: 'normal', img: 'assets/png/peashooter.png', desc: '发射豌豆攻击僵尸。' },
    acid_lemon: { name: '强酸柠檬', cost: 125, cooldown: 7, hp: 200, category: 'normal', img: 'assets/png/acid_lemon.png', desc: '发射柠檬汁攻击僵尸，可以腐蚀铁质护甲。' },
    sunflower: { name: '向日葵', cost: 50, cooldown: 7, hp: 200, category: 'normal', img: 'assets/png/sunflower.png', desc: '生产阳光。' },
    grape_pult: { name: '葡萄投手', cost: 225, cooldown: 7, hp: 200, category: 'normal', img: 'assets/svg/grape_pult.svg', desc: '投掷葡萄弹，命中后分裂成小葡萄攻击周围僵尸。' },
    pod_peashooter: { name: '豌豆荚', cost: 225, cooldown: 7, hp: 200, category: 'normal', img: 'assets/png/peasecod.png', desc: '同时散射5发豌豆，火力更猛。' },
    bomber: { name: '石榴投掷器', cost: 200, cooldown: 7, hp: 200, category: 'normal', img: 'assets/svg/bomber.svg', desc: '投掷石榴籽，可攻击3行的最多6个目标。' },
    torchwood: { name: '火炬树桩', cost: 175, cooldown: 7, hp: 500, category: 'normal', img: 'assets/png/torchwood.png', desc: '点燃穿过的豌豆，使其造成双倍伤害并溅射。也可以制作爆米花。' },
    watermelon: { name: '西瓜投手', cost: 300, cooldown: 7, hp: 200, category: 'normal', img: 'assets/png/watermelon.png', desc: '投掷西瓜，造成大范围溅射伤害。' },
    iced_coconut: { name: '冰镇椰子', cost: 175, cooldown: 50, hp: 200, category: 'floating', img: 'assets/png/iced-coconut.png', desc: '滚动冰椰子，击退路径上的僵尸，到达终点后爆炸并减速僵尸。' },
    trumpet: { name: '喇叭花', cost: 50, cooldown: 30, hp: 200, category: 'normal', img: 'assets/svg/trumpet.svg', desc: '吸引3×3范围内的子弹到本行。' },
    pine_shooter: { name: '松针射手', cost: 150, cooldown: 7, hp: 200, category: 'normal', img: 'assets/svg/pine-shooter.svg', desc: '发射松针攻击，可穿透僵尸，可被点燃。' },
    gold_bloom: { name: '黄金蓓蕾', cost: 150, cooldown: 50, hp: 200, category: 'normal', img: 'assets/png/gold-blooms.png', desc: '种植一段时间后产生大量阳光，然后消失。' },
    spiky_pumpkin: { name: '尖刺南瓜', cost: 150, cooldown: 50, hp: 2000, category: 'carrier', img: 'assets/svg/spiky-pumpkin.svg', desc: '可叠加在其他植物上提供保护。' },
    jalapeno_pair: { name: '火爆双椒', cost: 225, cooldown: 50, hp: 10000, category: 'normal', img: 'assets/svg/jalapeno-pair.svg', desc: '对一行一列的僵尸造成爆炸伤害。' },
    mimic: { name: '模仿者', cost: 325, cooldown: 30, hp: 200, category: 'normal', img: 'assets/png/mimic.png', desc: '变形为上一次种下的植物。' },
    reshaper: { name: '分解菌落', cost: 50, cooldown: 30, hp: 200, category: 'floating', img: 'assets/svg/reshaper.svg', desc: '分解本格植物，返还全部阳光并重置其冷却。' },
    time_machine: { name: '时光机', cost: 125, cooldown: 50, hp: 200, category: 'floating', img: 'assets/svg/time-machine.svg', desc: '重置本格植物的冷却时间。' },
    laser_shroom: { name: '激光菇', cost: 300, cooldown: 15, hp: 200, category: 'normal', img: 'assets/svg/laser-shroom.svg', desc: '向8个方向发射穿透激光。' },
    windmill: { name: '风车草', cost: 250, cooldown: 30, hp: 200, category: 'normal', img: 'assets/svg/windmill.svg', desc: '提升右侧的投掷类植物的伤害。' },
    vine_trap: { name: '藤蔓陷阱', cost: 125, cooldown: 30, hp: 500, category: 'normal', img: 'assets/svg/vine-trap.svg', desc: '减速3×3范围内僵尸，持续15秒。' },
    electrode_cherry: { name: '电极樱桃', cost: 175, cooldown: 15, hp: 200, category: 'normal', img: 'assets/svg/electrode-cherry.svg', desc: '两株电极樱桃之间会产生电流，穿过电流的僵尸会持续受到伤害。' },
    wild_gatling: { name: '狂野机枪射手', cost: 450, cooldown: 30, hp: 200, category: 'normal', img: 'assets/png/wild-gatling.png', desc: '向前方3个方向扫射，每个方向发射4颗豌豆。' },
    ninja_nut: { name: '忍者坚果', cost: 100, cooldown: 50, hp: 2000, category: 'normal', img: 'assets/png/ninja-nut.png', desc: '种下后会在周围召唤两个血量较少的分身。' },
    citron: { name: '充能柚子', cost: 200, cooldown: 7, hp: 200, category: 'normal', img: 'assets/png/citron.png', desc: '鼠标点击发射能量球。能量球的大小，伤害，穿透性都会随蓄力时间增加而增加。' },
    corn_homing: { name: '玉米追踪炮', cost: 375, cooldown: 7, hp: 200, category: 'normal', img: 'assets/svg/corn-homing.svg', desc: '发射追踪玉米粒，小概率发射能够定身僵尸的黄油块。' },
    corn_gatling: { name: '玉米机枪', cost: 275, cooldown: 7, hp: 200, category: 'normal', img: 'assets/svg/corn-gatling.svg', desc: '攻速随攻击时间增加而提升，小概率发射黄油定身敌人。' },
    jelly: { name: '蓝莓果冻', cost: 125, cooldown: 7, hp: 500, category: 'normal', img: 'assets/svg/jelly.svg', desc: '反弹直线型子弹。' },
    binary_tree: { name: '二叉树', cost: 175, cooldown: 7, hp: 200, category: 'normal', img: 'assets/svg/binary_tree.svg', desc: '发射分叉树枝，树枝命中后会继续分裂。最喜欢的单词是log。' },
    maguey: { name: '龙舌兰', cost: 300, cooldown: 15, hp: 200, category: 'normal', img: 'assets/png/maguey.png', desc: '向最近的僵尸发射穿透魔法箭矢。' },
    christmas_nut: { name: '圣诞坚果', cost: 50, cooldown: 50, hp: 2000, category: 'normal', img: 'assets/png/christmas-nut.png', desc: '死亡时爆炸，造成3×3范围伤害。' },
    sword_gourd: { name: '养剑葫', cost: 250, cooldown: 30, hp: 200, category: 'normal', img: 'assets/png/sword-gourd.png', desc: '发射飞剑，可跟随鼠标移动攻击僵尸。' },
    coffee_bean: { name: '咖啡豆', cost: 75, cooldown: 7, hp: 100, category: 'floating', img: 'assets/png/coffee-bean.png', desc: '唤醒本格植物，并使其攻速翻倍，持续15秒。' },
    bowling_nut: { name: '坚果保龄球', cost: 50, cooldown: 7, hp: 200, category: 'floating', img: 'assets/gif/bowling-nut.gif', desc: '碰撞僵尸造成伤害并弹跳，碰到边界反弹。' },
};

export const ZOMBIE_CONFIGS = {
    normal: { name: '普通僵尸', cost: 50, cooldown: 1, hp: 200, img: 'assets/png/zombie.png', desc: '最普通的僵尸。' },
    buckethead: { name: '铁桶僵尸', cost: 200, cooldown: 1, hp: 200, armor: 1000, img: 'assets/png/bucket-zombie.png', desc: '头上的铁桶能吸收5倍于自身血量的伤害。' },
    exploder: { name: '爆破僵尸', cost: 150, cooldown: 1, hp: 200, img: 'assets/svg/exploder-zombie.svg', desc: '接触植物时自爆，对3×3范围造成大量伤害。' },
    fisher: { name: '渔夫僵尸', cost: 200, cooldown: 1, hp: 400, img: 'assets/svg/fisher-zombie.svg', desc: '使用鱼线将远处的植物拉向自己。' },
    football: { name: '橄榄球僵尸', cost: 400, cooldown: 1, hp: 200, armor: 1600, img: 'assets/png/rugby-zombie.png', desc: '移动速度快，装备的护具能吸收8倍于自身血量的伤害。' },
    football_forward: { name: '橄榄球前锋僵尸', cost: 600, cooldown: 1, hp: 200, armor: 2400, img: 'assets/png/football-forward.png', desc: '速度极快，装备更强的护具，会将前方的植物推开，无法推动时才进行攻击。' },
    gargantuar: { name: '巨人僵尸', cost: 900, cooldown: 1, hp: 4500, img: 'assets/png/gargantuar.png', desc: '体型巨大，生命值极高，会砸扁阻拦的植物。' },
    priest: { name: '僵尸牧师', cost: 200, cooldown: 1, hp: 600, img: 'assets/svg/priest-zombie.svg', desc: '为附近的受伤僵尸回复生命值。' },
    siren: { name: '海妖僵尸', cost: 500, cooldown: 1, hp: 400, img: 'assets/png/siren.png', desc: '吹响海螺，使本行植物陷入睡眠。' },
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
