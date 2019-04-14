import asyncio
import json
import time

import aiohttp
import websockets

import showdown_commands

class Showdown:

    def __init__(self, bot, id, pw, channel_id, voice_id, timeout=3600, ai=False):
        self.bot = bot
        self.id = id
        self.pw = pw
        self.channel_id = channel_id
        self.voice_id = voice_id
        self.timeout = timeout
        self.ai = ai

        self.ws = None
        self.timer = self.timeout
        self.bot_time = 0
        self.running = False
        
        self.listener = {} #channel id : on_message function
        self.rooms = {} #channel id : active room
        self.channels = {} #active room : channel id
        
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
        
    async def login(self, msg):
        login_msg = '|/trn ' + self.id + ',0,'
        
        async with aiohttp.ClientSession() as session:
            url = 'http://play.pokemonshowdown.com/action.php'
            data = {}
            data['act'] = 'login'
            data['name'] = self.id
            data['pass'] = self.pw
            data['challstr'] = msg[2] + '|' + msg[3]
            
            #assume no errors here (bad idea); login fails if nametaken with bad password, or bad challstr
            async with session.post(url, data=data) as response:
                s = json.loads((await response.text())[1:])
                login_msg += s['assertion']
        
        await self.ws.send(login_msg)
        await self.ws.send('|/avatar 27')
        
    async def handle_challenge(self, msg):
        dict = json.loads(msg[2])
        for user, format in dict['challengesFrom'].items():
            if user == 'psikh0':
                await self.ws.send('|/utm ' + 'null')
                await self.ws.send('|/accept psikh0')
        return
    
    #Q Up
    async def queue(self): pass
    
    #let showdown handle target legality
    async def choose(self, room, command, target, option=''):
        await self.ws.send(room + '|/choose ' + command + ' ' + target + option)
    
    #room responses always start with >ROOMID\n
    async def handle_room_response(self, response):
        r = response.split('\n')
        room_id = r[0][1:].rstrip()
        
        for line in r[1:]:
            msg = line.split('|')
            if len(msg) <= 1: continue
            
            response_type = msg[1]
            if response_type == 'init':
                if msg[2] == 'battle':
                    #only use this channel for now
                    self.rooms[self.channel_id] = room_id
                    self.channels[room_id] = self.channel_id
                    pass
                elif msg[2] == 'chat': pass
            else:
                pass
            
        return
    
    async def handle_global_response(self, response):
        r = response.split('\n')  
        for line in r:
            msg = line.split('|')
            if len(msg) <= 1: continue
            
            response_type = msg[1]
            if response_type == 'challstr':
                await self.login(msg) #TODO: if not logged in
            elif response_type == 'updatechallenges':
                await self.handle_challenge(msg)
            elif response_type == 'updatesearch':
                #games = json.loads(msg[2])['games']
                #games can just be a json 'null'
                #bind room / channel
                continue
            else:
                continue
        return
    
    async def handle_response(self, response):
        if response[0] == '>':
            return await self.handle_room_response(response)
        else:
            return await self.handle_global_response(response)
    
    async def connect_with_timeout(self, ctx):
        if self.ws is not None: return
        #TODO maybe: await asyncio.wait_for(ws.recv(), timeout=X)
        try:
            async with websockets.connect('ws://sim.smogon.com:8000/showdown/websocket') as self.ws:
                showdown_commands.load_showdown_commands(self.bot, self, ctx)
                async for response in self.ws:
                    print(response + ' ENDRESPONSE')
                    await self.handle_response(response)
        finally:
            self.ws = None
            showdown_commands.unload_showdown_commands(self.bot, self, ctx)
    
    async def close(self):
        if self.ws is None: return
        ws_temp, self.ws = self.ws, None
        await ws_temp.close()