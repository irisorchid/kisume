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
    
    choose(room, command, target, op='') {
        this.ws.send(room + '|/choose ' + command + ' ' + target + op);
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
        return;
        //this.ws.send (login_msg)
        //this.ws.send('|/avatar 27');
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
        this.add_listener(channel);
    }
    
    stop() {
        this.ws.terminate();
        //this.cleanup(channel); //need this if terminate does not emit close
    }
    
    cleanup(channel) {
        this.remove_listener(channel);
        this.ws = null;
    }

    generate_commands() { 
        const commands = function(message) {
            return;
        };
        return commands;
    }
    
    add_listener(channel) {
        if (channel.id in this.listeners) { return; }
        const commands = generate_commands();
        this.listeners[channel.id] = commands;
        this.bot.on('message', commands);
    }
    
    remove_listener(channel) {
        const commands = this.listeners[channel.id];
        if (commands === undefined) { return; }
        this.bot.off('message', commands);
        delete this.listeners[channel.id];
    }
}

ShowdownInstance.url = 'wss://sim.smogon.com/showdown/websocket';
ShowdownInstance.action_url = 'https://play.pokemonshowdown.com/action.php';

const showdown_commands = function(bot, config) {
    
    const pokemon = new ShowdownInstance();
    
    const showdown = {
        name: 'showdown',
        execute: async function(message, args) {
            //block calls except from config.discord_channel_id for now
            if (message.channel.id !== config.discord_channel_id) { return; }
            return;
        },
    };
    
    return {
        showdown: showdown,
    };
}

module.exports = showdown_commands;