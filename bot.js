"use strict";

const Discord = require('discord.js');

const config = require('./config.json');
const setup = require('./setup.js');

const bot = new Discord.Client();
bot.commands = new Discord.Collection();
bot.command_modules = new Discord.Collection();

setup(bot, config);

bot.login(config.discord_token);

//self notes
//return await redundant except in try/catch blocks ?