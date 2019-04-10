import asyncio
import json
import time

import aiohttp
import websockets

import showdown_commands

#maybe cache some of the ws responses

class Showdown:

    def __init__(self, bot, id, pw, channel_id, timeout=3600):
        self.bot = bot
        self.id = id
        self.pw = pw
        self.channel_id = channel_id
        self.timeout = timeout

        self.ws = None
        self.connected_started = False
        self.timer = self.timeout
        self.bot_time = 0
        
        self.listener = {}
        self.rooms = {}
        self.ws_lock = asyncio.Lock()
        
        showdown_commands.load_commands(self.bot, self)
    
    def reset_time(self):
        self.timer = self.timeout
            
    async def sendprint(self, msg):
        print(msg)
        await self.ws.send(msg)
        
    async def check_timeout(self):
        while True:
            await asyncio.sleep(self.timer)
            self.timer = time.time() - self.bot_time
            if self.timer >= self.timeout:
                pass #timeout occurred #should return here
            else:
                self.timer = self.timeout - self.timer
        
    async def login(self, r):
        login_msg = '|/trn ' + self.id + ',0,'
        
        async with aiohttp.ClientSession() as session:
            url = 'http://play.pokemonshowdown.com/action.php'
            data = {}
            data['act'] = 'login'
            data['name'] = self.id
            data['pass'] = self.pw
            data['challstr'] = r[2] + '|' + r[3]
            
            #assume no errors here (bad idea); login fails if nametaken with bad password, or bad challstr
            async with session.post(url, data=data) as response:
                s = json.loads((await response.text())[1:])
                login_msg += s['assertion']
        
        await self.ws.send(login_msg)
        await self.ws.send('|/avatar 27')
        
    async def handle_challenge(self, r):
        dict = json.loads(r[2])
        for user, format in dict['challengesFrom'].items():
            if user == 'psikh0':
                await self.ws.send('|/utm ' + 'null')
                await self.ws.send('|/accept psikh0')
        return
    
    async def choose(self, room, command, target, option=''):
        await self.ws.send(room + '|/choose ' + command + ' ' + target + option)
    
    #room responses always start with >ROOMID\n
    async def handle_room_response(self, response):
        room = response.split('|')[0][1:].rstrip()
        
        # elif response_type == 'turn':
            # await ws.send(room + '|/choose move 1')
    
    #lobby / global responses
    async def handle_global_response(self, response):
        r = response.split('|')
        if len(r) == 1: return
        
        if r[1] == 'challstr':
            await self.login(r)
        elif r[1] == 'updatechallenges':
            await self.handle_challenge(r)
        elif r[1] == 'updatesearch':
            return
        else:
            return
    
    async def handle_response(self, response):
        if response[0] == '>':
            await self.handle_room_response(response)
        else:
            await self.handle_global_response(response)
    
    async def connect_with_timeout(self, ctx):
        #TODO: lock here ? 
        if self.ws is not None:
            return
        
        #TODO maybe: await asyncio.wait_for(ws.recv(), timeout=X)
        async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as self.ws:
            try:
                showdown_commands.load_showdown_commands(self.bot, self, ctx)
                async for response in self.ws:
                    print(response + ' ENDRESPONSE')
                    await self.handle_response(response)
            finally:
                showdown_commands.unload_showdown_commands(self.bot, self, ctx)
                
            print("CONNECTION CLOSED 1")            
        print("CONNECTION CLOSED 2")
    
    async def close(self):
        #TODO: lock here too
        if self.ws is not None:
            await self.ws.close()
