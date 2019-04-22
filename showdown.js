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
    
    async login(msg) {
        const data = {};
        data.act = 'login';
        data.name = this.name;
        data.pass = this.pw;
        data.challstr = 'something'; //msg[2] + '|' + msg[3]
        
        //assume post request does not fail for now;
        const res = await axios.post(ShowdownInstance.action_url, data);
        const info = JSON.parse(res.data.slice(1));
        const login_msg = '|/trn ' + id + ',0,' + info.assertion;
        this.ws.send (login_msg)
        this.ws.send('|/avatar 27');
    }
    
    handle_room_response(msg) {
        
    }
    
    handle_global_response(msg) {
        
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
        
        this.ws.on('open', function(){
            console.log('connected to showdown!');
        });
        this.ws.on('error', function(error){
            console.log('ERROR');
            this.cleanup(channel);
        });
        this.ws.on('close', function(code, reason){
            console.log('CLOSE'); //ws.terminate() forcibly closes socket not sure if this still gets called
            this.cleanup(channel);
        });
        this.ws.on('message', function(message){
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
        this.ws.terminate();
        //this.cleanup(channel); //need this if terminate does not emit close
    }
    
    cleanup(channel) {
        this.remove_listener(channel.id);
        this.ws = null;
    }

    generate_commands(channel_id) { 
        const commands = function(message) {
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
        const commands = generate_commands(channel_id);
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

ShowdownInstance.url = 'wss://sim.smogon.com/showdown/websocket';
ShowdownInstance.action_url = 'https://play.pokemonshowdown.com/action.php';

const showdown_commands = function(bot, config) {
    
    const pokemon = new ShowdownInstance();
    
    const showdown = {
        name: 'showdown',
        execute: async function(message, args) {
            if (message.channel.id !== config.discord_channel_id) { return; } //block calls from other channels for now
            pokemon.run(message.channel);
        },
    };
    
    return {
        showdown: showdown,
    };
}

module.exports = showdown_commands;