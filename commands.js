"use strict";

const command_list = function(bot, config) {
    
    const hello = {
        name: 'hello',
        execute: async function(message, args) {
            return message.channel.send('Hello World!');
        },
    }
    
    const echo = {
        name: 'echo',
        execute: async function(message, args) {
            return message.channel.send(message.content.slice(config.command_prefix.length + 4).trim());
        },
    }
    
    const choose = {
        name: 'choose',
        execute: async function(message, args) {
            const choice = Math.floor(Math.random() * args.length);
            return message.channel.send(args[choice]);
        },
    }
    
    const kusoge = {
        name: 'kusoge',
        execute: async function(message, args) {
            return bot.destroy();
        },
    }
    
    const unravel = {
        name: 'unravel',
        execute: async function(message, args) {
            return null;
        },
    }
    
    return {
        hello: hello,
        echo: echo,
        choose: choose,
        kusoge: kusoge,
        unravel: unravel,
    }
}

module.exports = command_list;