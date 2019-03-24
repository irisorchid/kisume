import os
import asyncio
import json

import aiohttp
import websockets

from dotenv import load_dotenv

#load_dotenv(verbose=True)

#lets try class based approach
#eventually change this into async class instead of 1 function does all maybe

#not very "thread safe or exception safe" yet xd

class Showdown:

    #timeout = logoff after X seconds?
    #ai = if true make bot play, if false users play
    def __init__(self, id, pw, timeout=3600, ai=False):
        self.id = id
        self.pw = pw
        self.timeout = timeout
        self.ai = ai
    
    async def test(self, ctx):
        await ctx.send('test2')
        
    async def pick_avatar(self, ws):
        await ws.send('|/avatar 27')
        
    async def login(self, r):
        login_predicate = '|/trn ' + self.id + ',0,'
        
        async with aiohttp.ClientSession() as session:
            url = 'http://play.pokemonshowdown.com/action.php'
            data = {}
            data['act'] = 'login'
            data['name'] = self.id
            data['pass'] = self.pw
            data['challstr'] = r[2] + '|' + r[3]
            
            #assume no errors here (bad idea)
            #login fails if nametaken with bad password->bad challstr
            async with session.post(url, data=data) as resp:
                r = json.loads((await resp.text())[1:])
                login_predicate += r['assertion']
        
        return login_predicate
        
    async def handle_challenge(self, r):
        for user, format in json.loads(r[2]):
            if user == 'pSikh0':
                print('accept')
        
    async def handle_response(self, ws, r):
        response_type = r[1]
        #switch = {}
        
        #TODO: only accepts challenges from user pSikh0
        
        #make this better later
        if response_type == 'challstr':
            #assume not logged on yet
            msg = await self.login(r)
            await ws.send(msg)
            await self.pick_avatar(ws)
        elif response_type == 'updatechallenges':
            self.handle_challenge(r)
            #print(r[2])
            #print(json.loads(r[2])['challengesFrom'])
        else:
            return
            
    async def run_timeout_instance(self, ctx):
        async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as ws:
            #might raise connectionclosed error
            async for response in ws:
                print(response)
                await self.handle_response(ws, response.split('|'))
                #await ctx.send('xd')
        