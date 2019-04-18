"use strict";

const commands = function(bot, command_prefix) {
    
    const command_list = require('./commands.js')(bot, command_prefix);
    
    for (const command in command_list) {
        bot.commands.set(command_list[command].name, command_list[command].execute)
    }
    
    bot.on('ready', async () => {
        console.log('bot is ready!');
    });
    
    bot.on('message', async (message) => {
        if (!message.content.startsWith(command_prefix) || message.author.bot) { return; }
        
        const args = message.content.slice(command_prefix.length).split(/ +/);
        const commandName = args.shift().toLowerCase();
        
        if (!bot.commands.has(commandName)) { return; }
        
        const command = bot.commands.get(commandName);
        try {
            return await command(message, args);
        } finally {
            //do something
        }
    });
    
    return null;
}

module.exports = commands