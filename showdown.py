import os
import asyncio
import json

import aiohttp
import websockets

from dotenv import load_dotenv

#load_dotenv(verbose=True)

#lets try class based approach
#eventually change this into async class instead of 1 function does all

#not very "thread safe or exception safe" yet xd

#async for message in websocket: ?

class Showdown:
    
    #get username + password from env from main
    #timeout = logoff after X seconds?
    def __init__(self, id, pw, timeout=3600):
        self.id = id
        self.pw = pw
        self.timeout = timeout
    
    async def test(self, ctx):
        await ctx.send('test2')
    
    async def connect(self):
        print('connect')
        
    async def login(self, r):
        login_predicate = '|/trn ' + self.id + ',0,'
        
        async with aiohttp.ClientSession() as session:
            url = 'http://play.pokemonshowdown.com/action.php'
            data = {}
            data['act'] = 'login'
            data['name'] = self.id
            data['pass'] = self.pw
            data['challstr'] = r[2] + '|' + r[3]
            
            async with session.post(url, data=data) as resp:
                r = json.loads((await resp.text())[1:])
                login_predicate += r['assertion']
        
        return login_predicate
        
    #how to implement callbacks maybe?
    async def handle_response(self, ws, r):
        response_type = r[1]
        #switch = {}
        #TODO: switch on response -> function mapping?
        if response_type == 'challstr':
            #assume not logged on yet
            msg = await self.login(r)
            await ws.send(msg)
        
            
    async def run_timeout_instance(self, ctx):
        async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as ws:
            async for response in ws:
                await self.handle_response(ws, response.split('|'))
                print(response)
                await ctx.send('xd')
        