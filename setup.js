"use strict";

const load_commands = function(bot, command_list) {
    for (const command in command_list) {
        bot.commands.set(command_list[command].name, command_list[command].execute)
    }
}

const commands = function(bot, config) {
    
    const main = require('./commands.js')(bot, config);
    const showdown = require('./showdown.js')(bot, config);

    bot.command_modules.set('main', main);
    bot.command_modules.set('showdown', showdown);
    
    for (const module of bot.command_modules.values()) {
        load_commands(bot, module.command_list);
    }
    
    bot.on('ready', () => {
        console.log('bot is ready!');
    });
    
    bot.on('message', (message) => {
        if (!message.content.startsWith(config.command_prefix) || message.author.bot) { return; }
        
        const args = message.content.slice(config.command_prefix.length).split(/ +/);
        const commandName = args.shift().toLowerCase();
        
        if (!bot.commands.has(commandName)) { return; }
        
        const command = bot.commands.get(commandName);
        try {
            return command(message, args);
        } finally {
            //do something
        }
    });
    
}

module.exports = commands;