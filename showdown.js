"use strict";

const axios = require('axios');
const WebSocket = require('ws');

class ShowdownManager {
    
    constructor(bot, config) {
        this.ws = null;
        this.bot = bot;
        this.name = config.showdown_username;
        this.pw = config.showdown_password;
        
        this.listeners = {}; //channel id : event_handler
        this.rooms = {}; // channel id: room
        this.channels = {}; // room : channel id
    }
    
    choose(room, command, target, op='') {
        this.ws.send(room + '|/choose ' + command + ' ' + target + op);
    }
    
    login() {
        const data = {};
        data.act = 'login';
        data.name = id;
        data.pass = pw;
        data.challstr = 'something'; //msg[2] + '|' + msg[3]
        
        //assume post does not fail for now;
        const res = await axios.post(ShowdownManager.action_url, data);
        const info = JSON.parse(res.data.slice(1));
        const login_msg = '|/trn ' + id + ',0,' + info.assertion;
        return;
        //ws.send (login_msg)
        //ws.send('|/avatar 27');
    }
    
    handle_response(msg) {
        if (msg[0] === '>') {
            
        } else {
            
        }
    }
    
    run() {
        if (this.ws != null) { return; }
        
        this.ws = new WebSocket(ShowdownManager.url);
        
        this.ws.on('open', function(){
            console.log('connected to showdown!');
            //load commmands here ?
        });
        this.ws.on('error', function(error){ console.log('error'); });
        this.ws.on('close', function(code, reason){
            //do some cleanup stuff here?
            //ws.terminate() forcibly closes socket not sure if this still gets called
        });
        this.ws.on('message', function(data){
            console.log(data);
            //assert typeof data is string ?
            //handleresponse data
        });
        
    }
    
    stop() {
        this.ws.terminate();
        this.cleanup();
    }
    
    cleanup() {
        this.ws = null;
    }
}

ShowdownManager.url = 'wss://sim.smogon.com/showdown/websocket';
ShowdownManager.action_url = 'https://play.pokemonshowdown.com/action.php';

const showdown = function(bot, config) {
    
    const pokemon = new ShowdownManager();
    
    const showdown_command = {
        name: 'showdown',
        execute: async function(message, args) {
            //has access to showdown variable
            return;
        },
    };
    //add this command to bot
    
    const generate_showdown_commands = function() {
        
    };
    
    //methods to implement:
    //load/deload showdown specific commands (either as listener or specific commands)
    //handle response: -> split into room and global response
    //close websocket?
    
    //TODO: add a property to bot that contains other module instances
    //each module should have a listener that's attached to it module.listener ?
    //use Map() for showdown commands?
    
    const add_listener = function() {
        //TODO: implement
        if (true) { return; }
        const f = null;
        
        bot.on('message', f);
    };
    
    const remove_listener = function() {
        //TODO: implement
        if (true) { return; }
        const f = null;
        
        bot.off('message', f);
        delete something;
    };
    
    return {};
}

module.exports = showdown;

/* python generate func skeleton
def load_showdown_commands(bot, showdown, ctx):
    if ctx.channel.id in showdown.listener: return
    showdown_commands = generate_showdown_commands(bot, showdown, ctx)
    showdown.listener[ctx.channel.id] = showdown_commands
    bot.add_listener(showdown_commands, 'on_message')

def unload_showdown_commands(bot, showdown, ctx):
    showdown_commands = showdown.listener.pop(ctx.channel.id, None)
    if showdown_commands is not None:
        bot.remove_listener(showdown_commands, 'on_message')
*/