import os
import asyncio
import random
import time

import discord
import websockets

from discord.ext import commands
from dotenv import load_dotenv

import showdown
import main_commands

load_dotenv(verbose=True)
discord_token = os.getenv('discord_token')
discord_channel_id = os.getenv('discord_channel_id') #for channel specific stuff

#TODO:
def dynamic_prefix(bot, message):
    return '!'

bot = commands.Bot(command_prefix='!')

instance = showdown.Showdown(bot, os.getenv('showdown_username'), os.getenv('showdown_password'))

#make modules struct with all the modules and pass to main commands

@bot.event
async def on_ready():
    print('Hello World')

"""
@bot.event
async def on_message(message):
    if message.content.startswith('!echo'):
        print('ldkasfhkjhfjkas')
"""
@bot.command(name='showdown')
async def pokemon(ctx):
    food.bot_time = time.time()
    #bot.loop.create_task(back())
    await instance.run_timeout_instance(ctx)
    #await here shouldn't run until instance times out
    print('showdown end test')
    await ctx.send('showdown end test')
    
@bot.command()
async def switch(ctx, *, content:str):
    food.bot_time = time.time()
    await instance.switch(content)
    
main_commands.load_commands(bot)
    
bot.run(discord_token)