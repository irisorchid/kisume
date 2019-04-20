"use strict";

const load_commands = function(bot, module) {
    for (const command in module) {
        bot.commands.set(module[command].name, module[command].execute)
    }
}

const commands = function(bot, config) {
    
    const command_list = require('./commands.js')(bot, config);
    //TODO: showdown module here
    //initialize modules?
    
    for (const command in command_list) {
        bot.commands.set(command_list[command].name, command_list[command].execute)
    }
    
    // design doc
    // for (const v of bot.command_modules) {
        // v.load_commands
    // }
    
    bot.on('ready', async () => {
        console.log('bot is ready!');
    });
    
    bot.on('message', async (message) => {
        if (!message.content.startsWith(config.command_prefix) || message.author.bot) { return; }
        
        const args = message.content.slice(config.command_prefix.length).split(/ +/);
        const commandName = args.shift().toLowerCase();
        
        if (!bot.commands.has(commandName)) { return; }
        
        const command = bot.commands.get(commandName);
        try {
            return await command(message, args);
        } finally {
            //do something
        }
    });
    
}

module.exports = commands;