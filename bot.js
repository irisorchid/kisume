"use strict";

const config = require('./config.json');
const Discord = require('discord.js');
const bot = new Discord.Client();

const command_prefix = '!';

bot.on('ready', async () => {
    console.log('bot is ready!');
});

bot.on('message', async (message) => {
    
    if (!message.content.startsWith(command_prefix) || message.author.bot) { return; }
    
    const args = message.content.slice(command_prefix.length).split(/ +/);
    const command = args.shift().toLowerCase();
    
    if (command === 'hello') {
        return message.channel.send('Hello World!');
    }
    
    if (command === 'echo') {
        return message.content.slice(command_prefix.length + 4).trim();
    }
    
    if (command === 'choose') {
        const choice = Math.floor(Math.random() * args.length);
        return message.channel.send(args[choice]);
    }
    
    if (command === 'kusoge') {
        
    }
    
    if (command === 'unravel') {
        
    }
    
});

bot.login(config.discord_token);