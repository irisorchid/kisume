import os
import asyncio

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(verbose=True)
discord_token = os.getenv('discord_token')
discord_channel_id = os.getenv('discord_channel_id') #for channel specific stuff

#TODO:
def prefix(bot, message):
    return '!'

bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('Hello World')
    
#@bot.event
#async def on_message():
    #do nothing
    
@bot.command()
async def hello(ctx):
    #print(ctx.message.channel.id)
    await ctx.send('Hello World')
    
@bot.command(name='foo')
async def _foo(ctx):
    await ctx.send('foobar')
    
bot.run(discord_token)