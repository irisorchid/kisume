import os
import asyncio

import discord

from discord.ext import commands
from dotenv import load_dotenv

import showdown
import main_commands

load_dotenv(verbose=True)
discord_token = os.getenv('discord_token')
discord_channel_id = int(os.getenv('discord_channel_id'))

bot = commands.Bot(command_prefix='!')

#js like object ?
class container: pass
modules = container()

modules.instance = showdown.Showdown(bot, os.getenv('showdown_username'), os.getenv('showdown_password'), discord_channel_id)

main_commands.load_commands(bot, modules)

@bot.event
async def on_ready():
    print('bot is running!')
    
bot.run(discord_token)