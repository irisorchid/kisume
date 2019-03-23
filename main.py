import os
import asyncio

import discord
import websockets

from discord.ext import commands
from dotenv import load_dotenv

import showdown

load_dotenv(verbose=True)
discord_token = os.getenv('discord_token')
discord_channel_id = os.getenv('discord_channel_id') #for channel specific stuff

#TODO:
def dynamic_prefix(bot, message):
    return '!'

bot = commands.Bot(command_prefix='!')
instance = showdown.Showdown(os.getenv('showdown_username'), os.getenv('showdown_password'))

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

"""
async def lel():
    greeting = ''
    async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as websocket:
        await websocket.send('hello')
        greeting = await websocket.recv()
        
    return greeting
"""

@bot.command(name='showdown')
async def pokemon(ctx):
    await instance.run_timeout_instance(ctx)
    #await here shouldn't run until instance times out
    
@bot.command()
async def test2(ctx):
    await instance.test(ctx)
    
bot.run(discord_token)