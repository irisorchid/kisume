"use strict";

const load_commands = function(bot, module) {
    for (const command in module) {
        bot.commands.set(module[command].name, module[command].execute)
    }
}

const commands = function(bot, config) {
    
    const main = require('./commands.js');
    //const showdown = require('./showdown.js');

    bot.command_modules.set('main', main(bot, config));
    //bot.command_modules.set('showdown', showdown(bot, config));
    
    for (const module of bot.command_modules.values()) {
        load_commands(bot, module);
    }
    
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