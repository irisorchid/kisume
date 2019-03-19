import os
import asyncio

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(verbose=True)
discord_token = os.getenv('discord_token')

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('Hello World')
    
#@bot.event
#async def on_message():
    #do nothing
    
@bot.command()
async def hello(ctx):
    await ctx.send('Hello World')
    
bot.run(discord_token)