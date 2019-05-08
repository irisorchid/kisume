"use strict";

const main_commands = function(bot, config) {
    
    const hello = {
        name: 'hello',
        execute: function(message, args) {
            return message.channel.send('Hello World!');
        },
    };
    
    const echo = {
        name: 'echo',
        execute: function(message, args) {
            return message.channel.send(message.content.slice(config.command_prefix.length + 4).trim());
        },
    };
    
    const choose = {
        name: 'choose',
        execute: function(message, args) {
            const choice = Math.floor(Math.random() * args.length);
            return message.channel.send(args[choice]);
        },
    };
    
    const kusoge = {
        name: 'kusoge',
        execute: function(message, args) {
            //TODO: generalize this
            bot.command_modules.get('showdown').stop();
            return bot.destroy();
        },
    };
    
    const unravel = {
        name: 'unravel',
        execute: function(message, args) {
            console.log(message.channel.id);
            console.log(typeof message.channel.id);
        },
    };
    
    const join = {
        name: 'join',
        execute: function(message, args) {
            let voiceChannel = bot.channels.get(config.discord_voice_channel_id);
            try {
                voiceChannel.join();
            } finally {
                //do something
            }
        },
    };
    
    const leave = {
        name: 'leave',
        execute: function(message, args) {
            let voiceChannel = bot.channels.get(config.discord_voice_channel_id);
            voiceChannel.leave();
        },
    };
    
    const command_list = {
        hello: hello,
        echo: echo,
        choose: choose,
        kusoge: kusoge,
        unravel: unravel,
        join: join,
        leave: leave,
    };
    
    const stop = () => {};
    
    return {
        command_list: command_list,
        stop: stop,
    };
};

module.exports = main_commands;