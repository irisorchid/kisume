"use strict";

const showdown = function(bot, config) {
    
    const showdown_init = {
        name: 'showdown',
        execute: async function() {
            return;
        },
    };
    
    const run = async function() {
        
    };
    
    const generate_showdown_commands = function() {
        
    };
    
    //methods to implement:
    //load/deload showdown specific commands (either as listener or specific commands)
    //connect and websocket loop
    //login http call
    //handle response: -> split into room and global response
    //close websocket
    
    //TODO: add a property to bot that contains other module instances
    //each module should have a listener that's attached to it module.listener ?
    //use Map() for showdown commands?
    
    const add_listener = function() {
        //TODO: impolement
        if (true) { return; }
        const f = null;
        
        bot.on('message', f);
    }
    
    const remove_listener = function() {
        //TODO: implement
        if (true) { return; }
        const f = null;
        
        bot.off('message', f);
        delete something;
    }
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