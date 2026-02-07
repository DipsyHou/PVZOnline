export class Network {
    constructor(roomId, username, callbacks) {
        this.roomId = roomId;
        this.username = username;
        this.callbacks = callbacks; // { onStartGame, onGameState, onOpen }
        this.ws = null;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${protocol}://${window.location.host}/ws/room/${this.roomId}?username=${this.username}`;
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log("Connected to Game Server");
            if(this.callbacks.onOpen) this.callbacks.onOpen();
        };

        this.ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.type === 'start_game' && msg.config) {
                if(this.callbacks.onStartGame) this.callbacks.onStartGame(msg.config, msg.decks);
            } else if(msg.type === 'game_state') {
                if(this.callbacks.onGameState) this.callbacks.onGameState(msg);
            }
        };
        
        this.ws.onclose = () => {
            console.log("Disconnected from Game Server");
        };
    }

    sendPlacePlant(col, row, plantType) {
        if(this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'place_plant', 
                col: col, 
                row: row,
                plant_type: plantType
            }));
        }
    }

    sendShovel(col, row, isBottom) {
        if(this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'shovel', 
                col: col, 
                row: row,
                is_bottom: isBottom
            }));
        }
    }

    sendSpawnZombie(row, zombieType) {
        if(this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'spawn_zombie', 
                row: row, 
                zombie_type: zombieType
            }));
        }
    }

    sendActivatePlant(col, row) {
        if(this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'activate_plant', 
                col: col, 
                row: row
            }));
        }
    }

    sendMousePosition(col, row, mouse_x, mouse_y) {
        if(this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'mouse_position',
                col: col,
                row: row,
                mouse_x: mouse_x,
                mouse_y: mouse_y
            }));
        }
    }

    close() {
        if(this.ws) this.ws.close();
    }
}
