"use strict";

//temp
const module_list = {
    main: './commands.js',
    showdown: './showdown.js',
};

const load_commands = function(bot, command_list) {
    for (const command in command_list) {
        bot.commands.set(command_list[command].name, command_list[command].execute)
    }
};


const load_modules = function(bot, config) {
    for (const module_name in module_list) {
        const module = require(module_list[module_name])(bot, config);
        bot.command_modules.set(module_name, module);
        load_commands(bot, module.command_list);
    }
};

const setup = function(bot, config) {
    
    load_modules(bot, config);
    
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
    
};

module.exports = setup;