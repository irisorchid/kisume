"use strict";

const Discord = require('discord.js');

const config = require('./config.json');
const load_commands = require('./load_commands.js');

const bot = new Discord.Client();
bot.commands = new Discord.Collection();

load_commands(bot, '!');

bot.login(config.discord_token);

//self notes
//return await redundant except in try/catch blocks ?