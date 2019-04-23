"use strict";

const axios = require('axios');
const WebSocket = require('ws');

class ShowdownInstance {
    
    constructor(bot, config) {
        this.ws = null;
        this.bot = bot;
        this.name = config.showdown_username;
        this.pw = config.showdown_password;
        
        this.listeners = {}; //channel id : event_handler
        this.rooms = {}; // channel id: room
        this.channels = {}; // room : channel id
        this.queue = {}; //on game search, place channel in queue, on game found, shift and assign channel to game room
    }
    
    choose(room, action, target, op='') {
        this.ws.send(room + '|/choose ' + action + ' ' + target + op);
    }
    
    async login(m) {
        const data = {};
        data.act = 'login';
        data.name = this.name;
        data.pass = this.pw;
        data.challstr = m[2] + '|' + m[3];
        
        //assume post request does not fail for now;
        const res = await axios.post(ShowdownInstance.action_url, data);
        const info = JSON.parse(res.data.slice(1));
        const login_msg = '|/trn ' + this.name + ',0,' + info.assertion;
        this.ws.send (login_msg)
        this.ws.send('|/avatar 27');
    }
    
    handle_room_response(msg) {
        
    }
    
    handle_global_response(msg) {
        //TODO: cleanup variable names
        const r = msg.split('\n');
        
        for (const l of r) {
            const m = l.split('|');
            if (m.length <= 1) { continue; }
            
            const t = m[1];
            if (t === 'challstr') {
                this.login(m); //TODO: handle promise rejection?
            } else if (t === 'updatechallenges') {
                //for testing purposes
                const d = JSON.parse(m[2]);
                for (const u in d['challengesFrom']) {
                    if (u === 'psikh0') {
                        this.ws.send('|/utm ' + 'null');
                        this.ws.send('|/accept pSikh0');
                    }
                }
            }
        }
    }
    
    handle_response(msg) {
        if (msg[0] === '>') {
            this.handle_room_response(msg);
        } else {
            this.handle_global_response(msg);
        }
    }
    
    connect(channel) {
        if (this.ws !== null) { return; }
        
        this.ws = new WebSocket(ShowdownInstance.url);
        
        this.ws.on('open', () => {
            console.log('connected to showdown!');
        });
        this.ws.on('error', (error) => {
            console.log('ERROR');
            this.cleanup(channel);
        });
        this.ws.on('close', (code, reason) => {
            console.log('CLOSE');
            this.cleanup(channel);
        });
        this.ws.on('message', (message) => {
            console.log(message); //assert msg is string ?
            this.handle_response(message)
        });
    }
    
    run(channel) {
        if (this.ws !== null) { return; } //temporary
        
        if (this.ws === null) { this.connect(channel); }
        this.add_listener(channel.id);
    }
    
    stop() {
        this.ws.terminate(); //emits close
    }
    
    cleanup(channel) {
        this.remove_listener(channel.id);
        this.ws = null;
    }

    generate_commands(channel_id) { 
        const commands = (message) => {
            if (message.channel.id !== channel_id) { return; }
            if (!message.content.startsWith('~') || message.author.bot) { return; }
            
            const args = message.content.slice(1).toLowerCase().split(/ +/);
            const action = args.shift();
            
            const room = this.rooms[channel_id];
            if (room === undefined) { return; } //unless command is to queue
            
            if (args.length < 1) { return; }
            const target = args[0];
            if (action === 'switch') {
                return this.choose(room, action, target);
            }
            if (action === 'move') {
                const op = (args[1] === 'mega' || args[1] === 'zmove') ? ' ' + args[1] :'';
                return this.choose(room, action, target, op);
            }
        };
        return commands;
    }
    
    add_listener(channel_id) {
        if (channel_id in this.listeners) { return; }
        const commands = this.generate_commands(channel_id);
        this.listeners[channel_id] = commands;
        this.bot.on('message', commands);
    }
    
    remove_listener(channel_id) {
        const commands = this.listeners[channel_id];
        if (commands === undefined) { return; }
        this.bot.off('message', commands);
        delete this.listeners[channel_id];
    }
}

ShowdownInstance.url = 'ws://sim.smogon.com:8000/showdown/websocket';
ShowdownInstance.action_url = 'https://play.pokemonshowdown.com/action.php';

const showdown_commands = function(bot, config) {
    
    const pokemon = new ShowdownInstance(bot, config);
    
    const showdown = {
        name: 'showdown',
        execute: function(message, args) {
            if (message.channel.id !== config.discord_channel_id) { return; } //block calls from other channels for now
            pokemon.run(message.channel);
        },
    };
    
    const command_list = {
        showdown: showdown,
    };
    
    const stop = () => {
        pokemon.stop();
    }
    
    return {
        command_list: command_list,
        stop: stop,
    };
}

module.exports = showdown_commands;