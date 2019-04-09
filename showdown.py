import asyncio
import json
import time

import aiohttp
import websockets

import showdown_commands

class Showdown:

    def __init__(self, bot, id, pw, channel_id, ai=False, timeout=3600):
        self.bot = bot
        self.id = id
        self.pw = pw
        self.channel_id = channel_id
        self.ai = ai
        self.timeout = timeout
        
        self.ws = None
        self.timer = self.timeout
        self.bot_time = 0
        self.ctx = None
        self.rooms = {} #channel_id : room
        
        showdown_commands.load_commands(self.bot, self)
    
    def reset_time(self):
        self.timer = self.timeout
        
    async def sendprint(self, msg):
        await self.ws.send(msg)
        
    async def check_timeout(self):
        while True:
            await asyncio.sleep(self.timer)
            self.timer = time.time() - self.bot_time
            if self.timer >= self.timeout:
                pass #timeout occurred #should return here
            else:
                self.timer = self.timeout - self.timer
    
    async def test(self, ctx):
        await ctx.send('test2')
        
    async def login(self, r):
        login_msg = '|/trn ' + self.id + ',0,'
        
        async with aiohttp.ClientSession() as session:
            url = 'http://play.pokemonshowdown.com/action.php'
            data = {}
            data['act'] = 'login'
            data['name'] = self.id
            data['pass'] = self.pw
            data['challstr'] = r[2] + '|' + r[3]
            
            #assume no errors here (bad idea)
            #login fails if nametaken with bad password, or bad challstr
            async with session.post(url, data=data) as response:
                s = json.loads((await response.text())[1:])
                login_msg += s['assertion']
        
        await self.ws.send(login_msg)
        await self.ws.send('|/avatar 27')
        
    async def handle_challenge(self, r):
        # self.rooms[self.ctx.channel.id] = room
        dict = json.loads(r[2])
        for user, format in dict['challengesFrom'].items():
            if user == 'psikh0':
                await self.ws.send('|/utm ' + 'null')
                await self.ws.send('|/accept psikh0')
        return        
    
    async def switch(self, room, target):
        await self.ws.send(room + '|/choose switch ' + target)
    
    async def choice(self, choice, *args): pass
    
    #TODO: differentiate between battle messages and others
    
    #room responses always start with >ROOMID\n
    async def handle_room_response(self, response):
        room = response.split('|')[0][1:].rstrip()
        
        #if enter, bind channel to room
    
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
        
        # elif response_type == 'turn':
            # await ws.send(room + '|/choose move 1')
    
    #architecture problem: should create instance bound to channel
    async def run_timeout_instance(self, ctx):
        if self.ws is not None:
            return
        
        self.ctx = ctx
        async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as self.ws:
            #TODO maybe: await asyncio.wait_for(ws.recv(), timeout=X)
            async for response in self.ws:
                print(response + ' ENDRESPONSE')
                await self.handle_response(response)

            print("CONNECTION CLOSED 1")            
        print("CONNECTION CLOSED 2")
        return
               
    async def close(self):
        if self.ws is not None:
            await self.ws.close()
        
    