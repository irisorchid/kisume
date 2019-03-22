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
    
    async def connect():
        print('connect')
        
    async def login(r):
        login_predicate = '|/trn ' + self.id + ',0,'
        
        async with aiohttp.ClientSession() as session:
            url = 'http://play.pokemonshowdown.com/action.php'
            data = {}
            data['act'] = 'login'
            data['name'] = self.id
            data['pass'] = self.pw
            data['challstr'] = 'implementme'
            
            async with session.post(url, data=data) as resp:
                r = json.loads((await resp.text())[1:])
                login_predicate += r['assertion']
            
        
    #how to implement callbacks maybe?
    async def handle_response(ws, r):
        action = r[1]
        switch = {}
        #switch on action?
        
            
    async def run_timeout_instance():
        await with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as ws:
            async for response in ws:
                #handle r
                await handle_response(ws, response.split('|'))
        